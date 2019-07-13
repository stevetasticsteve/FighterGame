import pygame
import sys
import MapGenerator
import Entities

FPS = 30
Window_width = 800
Window_height = 600
x_center = int(Window_width / 2)
y_center = int(Window_height / 2)

colours = {'White': (255, 255, 255),
           'Black': (0, 0, 0)}


def reset_screen(map):
    window.fill(colours['Black'])
    for tile in map.tile_map:
        window.blit(pygame.image.load(tile[1]), tile[0])


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
                    Player.move(0, -1)
                if event.key == pygame.K_DOWN:
                    Player.move(0, 1)
                if event.key == pygame.K_LEFT:
                    Player.move(-1, 0)
                if event.key == pygame.K_RIGHT:
                    Player.move(1, 0)
                if event.key == pygame.K_ESCAPE:
                    close_program()

        reset_screen(map)
        window.blit(Player.sprite, (Player.x, Player.y))
        pygame.display.update()
        FPS_clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()
    FPS_clock = pygame.time.Clock()
    window = pygame.display.set_mode((Window_width, Window_height))
    pygame.display.set_caption('Fighter game')
    pygame.key.set_repeat(10)
    map = MapGenerator.map()

    Player = Entities.Player((100,100))
    game_loop()
