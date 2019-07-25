import pygame
import sys
import MapGenerator
import Entities
import random
import os

FPS = 30
window_size = (800,600)
map_size = (1000,800)
player_start = (100,100)
colours = {'White': (255, 255, 255),
           'Black': (0, 0, 0)}
debug_mode = True
enemy_behaviour_time = 1.5
number_of_enemies = 20
game_font = 'Arial'


def reset_screen(map):
    window.fill(colours['Black'])
    Camera.Move()
    background = Camera.Active_tiles()
    for tile in background:
        # Need to turn game coordinates into screen coordinates relative to the player
        screen_coord = convert_to_screen_coordinates((tile[0][0],tile[0][1]))
        window.blit(tile[1], screen_coord)

def create_entities():
    entities = []
    for i in range(number_of_enemies):
        x = random.randint(0,map_size[0])
        y = random.randint(0, map_size[1])
        angle = random.randint(0, 359)
        entities.append(Entities.Enemy((x, y, angle),map_size))
    return entities


def convert_to_screen_coordinates(coord):
    # takes game coordinates and converts it to screen (pixel) coordinates for blitting
    screen_x = coord[0] - Camera.rect[0]
    screen_y = coord[1] - Camera.rect[1]
    return (screen_x, screen_y)


def debug_window(content):
    box_size = (200,100)
    debug_box = pygame.Surface(box_size, flags=pygame.SRCALPHA)
    debug_box.fill((255,255,255,150))
    debug_font = pygame.font.SysFont(game_font, size=18)
    text_surf = debug_font.render(content, False, (0,0,0))
    debug_box.blit(text_surf, (10,10))
    window.blit(debug_box, (window_size[0]-box_size[0], window_size[1]-box_size[1]))


#TODO create a loading screen so the long pause at the start as images load to memory isn't though of as a bug

def close_program():
    pygame.quit()
    sys.exit()

def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_program()

            # Key bindings
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    close_program()

        background = pygame.Surface(window_size)
        background.fill((0, 0, 0))
        game_over_font = pygame.font.SysFont(game_font, size=30)
        text_surf = game_over_font.render('Game over!',
                                          False, (255, 255, 255))
        background.blit(text_surf, (window_size[0] / 2 - 100, window_size[1] / 2))
        text_surf = game_over_font.render('Press r to restart or escape to exit!',
                                          False, (255, 255, 255))
        background.blit(text_surf, (window_size[0] / 2 - 150, window_size[1] / 2 + 50))
        window.blit(background, (0,0))

        pygame.display.update()
        FPS_clock.tick(FPS)


def game_loop():
    game_over = False
    while True:
        if game_over:
            game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_program()

            # Key bindings
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Player.accelerate(1)
                if event.key == pygame.K_DOWN:
                    Player.accelerate(-1)
                if event.key == pygame.K_LEFT:
                    Player.rotate(-1)
                if event.key == pygame.K_RIGHT:
                    Player.rotate(1)
                if event.key == pygame.K_ESCAPE:
                    close_program()
                if event.key == pygame.K_SPACE:
                    projectiles.append(Player.shoot_missile())
                    random.choice(shooting_sfx).play()

        # Player update
        Player.move()
        reset_screen(map)
        player_sprite = pygame.transform.rotate(Player.sprite, Player.angle * -1)
        window.blit(player_sprite, (int(window_size[0] / 2), int(window_size[1] / 2)))

        # Enemy updates
        for entity in entities:
            if entity.last_behaviour_time > FPS * enemy_behaviour_time:
                entity.choose_behaviour(Player)
                entity.last_behaviour_time = 0
            else:
                entity.behaviour(player=Player)
                entity.move()
            shoot = entity.check_sights(Player)
            if shoot:
                projectiles.append(shoot)
                random.choice(shooting_sfx).play()


            # Draw enemies
            if entity.within_active_area(Camera):
                enemy_sprite = pygame.transform.rotate(entity.sprite, entity.angle * -1)
                window.blit(enemy_sprite, (convert_to_screen_coordinates((entity.blit_x, entity.blit_y))))


        # Projectile updates
        for projectile in projectiles:
            if projectile.time_alive > projectile.fuse:
                del projectile
                continue
            projectile.move()
        # Check player hits
            if projectile.check_hits(Player):
                if projectile.shooter != str(Player):
                    death_sfx.play()
                    game_over = True
                    # print('Player hit by ' + str(projectile))
        # Check enemy hits
            for entity in entities:
                if projectile.check_hits(entity):
                    if projectile.shooter == str(Player): # only allow player to hit enemies
                        entity.hit = True
                        random.choice(enemy_kill_sfx).play()
                        # print(str(entity) + ' hit by ' + str(projectile))
            if projectile.within_active_area(Camera):
                window.blit(projectile.surface, (convert_to_screen_coordinates((projectile.x, projectile.y))))

        # delete hit enemies
        entities[:] = [entity for entity in entities if not entity.hit]

        #UI
        if debug_mode:
            debug_window('Player x = ' + str(Player.x) + '   '
                         'Player y = ' +str(Player.y))

        # Game update
        pygame.display.update()
        FPS_clock.tick(FPS)


if __name__ == '__main__':
    x,y = 400, 50 # coordinates window is drawn at
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    enemy_kill_sfx = [pygame.mixer.Sound('Assets/Sound effects/ogg/Explosion 1.ogg'),
                      pygame.mixer.Sound('Assets/Sound effects/ogg/Explosion 2.ogg'),
                      pygame.mixer.Sound('Assets/Sound effects/ogg/Explosion 3.ogg')]
    shooting_sfx = [pygame.mixer.Sound('Assets/Sound effects/ogg/Shooting 1.ogg'),
                    pygame.mixer.Sound('Assets/Sound effects/ogg/Shooting 2.ogg'),
                    pygame.mixer.Sound('Assets/Sound effects/ogg/Shooting 3.ogg')]
    death_sfx = pygame.mixer.Sound('Assets/Sound effects/ogg/Player death.ogg')
    FPS_clock = pygame.time.Clock()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Flyover')
    pygame.key.set_repeat(10) # Enables direction button to be held
    map = MapGenerator.map(map_size)
    Player = Entities.Player((int(window_size[0]/2), int(window_size[1]/2), 180), map_size)
    entities = create_entities()
    projectiles = []
    Camera = Entities.Camera(Player, window_size, map)
    game_loop()
