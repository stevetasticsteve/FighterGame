import pygame
import sys
import MapGenerator
import Entities
import random
import os

class GameEngine:
    def __init__(self, settings):
        self.settings = settings
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.settings['window_position'][0],
                                                        self.settings['window_position'][1])
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.enemy_kill_sfx = [pygame.mixer.Sound('Assets/Sound effects/ogg/Explosion 1.ogg'),
                               pygame.mixer.Sound('Assets/Sound effects/ogg/Explosion 2.ogg'),
                               pygame.mixer.Sound('Assets/Sound effects/ogg/Explosion 3.ogg')]
        self.shooting_sfx = [pygame.mixer.Sound('Assets/Sound effects/ogg/Shooting 1.ogg'),
                             pygame.mixer.Sound('Assets/Sound effects/ogg/Shooting 2.ogg'),
                             pygame.mixer.Sound('Assets/Sound effects/ogg/Shooting 3.ogg')]
        self.death_sfx = pygame.mixer.Sound('Assets/Sound effects/ogg/Player death.ogg')
        self.FPS_clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(self.settings['window_size'])
        pygame.display.set_caption('Flyover')
        pygame.key.set_repeat(10)  # Enables direction button to be held

    def start_game(self):
        self.map = MapGenerator.map(self.settings['map_size'])
        self.Player = Entities.Player((int(self.settings['window_size'][0] / 2),
                                       int(self.settings['window_size'][1] / 2),
                                       180),
                                      self.settings['map_size'])
        self.entities = self.create_entities()
        self.projectiles = []
        self.Camera = Entities.Camera(self.Player, self.settings['window_size'],
                                      self.map)
        self.game_loop()

    def game_loop(self):
        game_over = False
        while True:
            if game_over:
                self.game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_program()

                # Key bindings
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.Player.accelerate(1)
                    if event.key == pygame.K_DOWN:
                        self.Player.accelerate(-1)
                    if event.key == pygame.K_LEFT:
                        self.Player.rotate(-1)
                    if event.key == pygame.K_RIGHT:
                        self.Player.rotate(1)
                    if event.key == pygame.K_ESCAPE:
                        self.close_program()
                    if event.key == pygame.K_SPACE:
                        self.projectiles.append(self.Player.shoot_missile())
                        random.choice(self.shooting_sfx).play()

            # Player update
            self.Player.move()
            self.reset_screen(self.map)
            player_sprite = pygame.transform.rotate(self.Player.sprite, self.Player.angle * -1)
            self.window.blit(player_sprite, (int(self.settings['window_size'][0] / 2),
                                             int(self.settings['window_size'][1] / 2)))

            # Enemy updates
            for entity in self.entities:
                if entity.last_behaviour_time > self.settings['FPS'] * self.settings['enemy_behaviour_time']:
                    entity.choose_behaviour(self.Player)
                    entity.last_behaviour_time = 0
                else:
                    entity.behaviour(player=self.Player)
                    entity.move()
                shoot = entity.check_sights(self.Player)
                if shoot:
                    self.projectiles.append(shoot)
                    random.choice(self.shooting_sfx).play()

                # Draw enemies
                if entity.within_active_area(self.Camera):
                    enemy_sprite = pygame.transform.rotate(entity.sprite, entity.angle * -1)
                    self.window.blit(enemy_sprite, (self.convert_to_screen_coordinates
                                                    ((entity.blit_x, entity.blit_y))))

            # Projectile updates
            for projectile in self.projectiles:
                if projectile.time_alive > projectile.fuse:
                    del projectile
                    continue
                projectile.move()
                # Check player hits
                if projectile.check_hits(self.Player):
                    if projectile.shooter != str(self.Player):
                        self.death_sfx.play()
                        game_over = True
                        # print('Player hit by ' + str(projectile))
                # Check enemy hits
                for entity in self.entities:
                    if projectile.check_hits(entity):
                        if projectile.shooter == str(self.Player):  # only allow player to hit enemies
                            entity.hit = True
                            random.choice(self.enemy_kill_sfx).play()
                            # print(str(entity) + ' hit by ' + str(projectile))
                if projectile.within_active_area(self.Camera):
                    self.window.blit(projectile.surface,
                                (self.convert_to_screen_coordinates((projectile.x, projectile.y))))

            # delete hit enemies
                    self.entities[:] = [entity for entity in self.entities if not entity.hit]

            # UI
            if self.settings['debug_mode']:
                self.debug_window('Player x = ' + str(self.Player.x) + '   '
                                  'Player y = ' + str(self.Player.y))

            # Game update
            pygame.display.update()
            self.FPS_clock.tick(self.settings['FPS'])

    def game_over_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_program()

                # Key bindings
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.start_game()
                    if event.key == pygame.K_ESCAPE:
                        self.close_program()

            background = pygame.Surface(self.settings['window_size'])
            background.fill((0, 0, 0))
            game_over_font = pygame.font.SysFont(self.settings['game_font'], size=30)
            text_surf = game_over_font.render('Game over!',
                                              False, (255, 255, 255))
            background.blit(text_surf, (self.settings['window_size'][0] / 2 - 100,
                                        self.settings['window_size'][1] / 2))
            text_surf = game_over_font.render('Press r to restart or escape to exit!',
                                              False, (255, 255, 255))
            background.blit(text_surf, (self.settings['window_size'][0] / 2 - 150,
                                        self.settings['window_size'][1] / 2 + 50))
            self.window.blit(background, (0, 0))

            pygame.display.update()
            self.FPS_clock.tick(self.settings['FPS'])

    def close_program(self):
        pygame.quit()
        sys.exit()

    def reset_screen(self, map):
        self.window.fill((0,0,0))
        self.Camera.Move()
        background = self.Camera.Active_tiles()
        for tile in background:
            # Need to turn game coordinates into screen coordinates relative to the player
            screen_coord = self.convert_to_screen_coordinates((tile[0][0], tile[0][1]))
            self.window.blit(tile[1], screen_coord)

    def create_entities(self):
        entities = []
        for i in range(self.settings['number_of_enemies']):
            x = random.randint(0, self.settings['map_size'][0])
            y = random.randint(0, self.settings['map_size'][1])
            angle = random.randint(0, 359)
            entities.append(Entities.Enemy((x, y, angle), self.settings['map_size']))
        return entities

    def convert_to_screen_coordinates(self, coord):
        # takes game coordinates and converts it to screen (pixel) coordinates for blitting
        screen_x = coord[0] - self.Camera.rect[0]
        screen_y = coord[1] - self.Camera.rect[1]
        return (screen_x, screen_y)

    def debug_window(self, content):
        box_size = (200, 100)
        debug_box = pygame.Surface(box_size, flags=pygame.SRCALPHA)
        debug_box.fill((255, 255, 255, 150))
        debug_font = pygame.font.SysFont(self.settings['game_font'], size=18)
        text_surf = debug_font.render(content, False, (0, 0, 0))
        debug_box.blit(text_surf, (10, 10))
        self.window.blit(debug_box, (self.settings['window_size'][0] - box_size[0],
                                     self.settings['window_size'][1] - box_size[1]))


if __name__ == '__main__':

    settings = {'FPS': 30,
                'window_size': (800,600),
                'window_position' : (400,50),
                'map_size': (1000,800),
                'player_start': (100,100),
                'debug_mode': False,
                'enemy_behaviour_time': 1.5,
                'number_of_enemies': 20,
                'game_font': 'Arial'}
    game = GameEngine(settings)
    game.start_game()
