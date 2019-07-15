import pygame
import sys
import MapGenerator
import Entities
import random

FPS = 30
window_size = (800,600)
map_size = (1000,800)
player_start = (100,100)
colours = {'White': (255, 255, 255),
           'Black': (0, 0, 0)}
debug_mode = True
enemy_behaviour_time = 1.5


def reset_screen(map):
    window.fill(colours['Black'])
    Camera.Move()
    background = Camera.Active_tiles()
    for tile in background:
        # Need to turn game coordinates into screen coordinates relative to the player
        screen_coord = convert_to_screen_coordinates((tile[0][0],tile[0][1]))
        window.blit(tile[1], screen_coord)


def convert_to_screen_coordinates(coord):
    # takes game coordinates and converts it to screen (pixel) coordinates for blitting
    screen_x = coord[0] - Camera.rect[0]
    screen_y = coord[1] - Camera.rect[1]
    return (screen_x, screen_y)

#TODO create a loading screen so the long pause at the start as images load to memory isn't though of as a bug

def close_program():
    pygame.quit()
    sys.exit()


def game_loop():
    while True:
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

        # Player update
        Player.move()
        if debug_mode:
            Player.Status()
        reset_screen(map)
        player_sprite = pygame.transform.rotate(Player.sprite, Player.angle * -1)
        window.blit(player_sprite, (int(window_size[0] / 2), int(window_size[1] / 2)))

        # Enemy updates
        if Enemy.last_behaviour_time > FPS * enemy_behaviour_time:
            Enemy.choose_behaviour(Player)
            Enemy.last_behaviour_time = 0
        else:
            Enemy.behaviour(player=Player)
        Enemy.move()

        # Draw enemies
        if Enemy.within_active_area(Camera):
            enemy_sprite = pygame.transform.rotate(Enemy.sprite, Enemy.angle * -1)
            window.blit(enemy_sprite, (convert_to_screen_coordinates((Enemy.x, Enemy.y))))
        # Game update
        pygame.display.update()
        FPS_clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()
    FPS_clock = pygame.time.Clock()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Flyover')
    pygame.key.set_repeat(10) # Enables direction button to be held
    map = MapGenerator.map(map_size)
    Player = Entities.Player((int(window_size[0]/2),int(window_size[1]/2),90))
    Enemy = Entities.Enemy((Player.x,Player.y,90))
    Camera = Entities.Camera(Player, window_size, map)
    game_loop()
