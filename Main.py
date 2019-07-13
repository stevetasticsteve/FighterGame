import pygame
import sys
import MapGenerator

FPS = 30
Window_width = 800
Window_height = 600

class Player:
    def __init__(self):
        self.player_size = 10
        self.player_colour = colours['White']
        self.x = player_start_x
        self.y = player_start_y
        self.speed = 10

    def draw(self):
        window.blit(plane, (self.x, self.y))

    def move(self, x, y):
        self.x += x * self.speed
        self.y += y * self.speed


def reset_screen(map):
    window.fill(colours['Black'])
    tile = pygame.image.load(map.tile_map[(0,0)])
    window.blit(tile, (0,0))


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
        Player.draw()
        pygame.display.update()
        FPS_clock.tick(FPS)


if __name__ == '__main__':
    x_center = int(Window_width / 2)
    y_center = int(Window_height / 2)

    player_start_x = x_center
    player_start_y = y_center

    colours = {'White': (255, 255, 255),
               'Black': (0, 0, 0)}

    pygame.init()
    FPS_clock = pygame.time.Clock()
    window = pygame.display.set_mode((Window_width, Window_height))
    pygame.display.set_caption('Fighter game')
    pygame.key.set_repeat(10)
    plane = pygame.image.load('Assets/Sprites/Plane.png')
    map = MapGenerator.map()

    Player = Player()
    game_loop()
