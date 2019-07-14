import pygame
import sys
import MapGenerator
import Entities

FPS = 30
window_size = (800,600)
map_size = (800,600)
player_start = (100,100)
colours = {'White': (255, 255, 255),
           'Black': (0, 0, 0)}


def reset_screen(map):
    window.fill(colours['Black'])
    # for tile in map.tile_map:
    #     window.blit(pygame.image.load(tile[1]), tile[0])
    Camera.Move()
    background = Camera.Active_tiles()
    for tile in background:
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
                    Player.accelerate(1)
                if event.key == pygame.K_DOWN:
                    Player.accelerate(-1)
                if event.key == pygame.K_LEFT:
                    Player.rotate(-1)
                if event.key == pygame.K_RIGHT:
                    Player.rotate(1)
                if event.key == pygame.K_ESCAPE:
                    close_program()

        Player.move()
        reset_screen(map)
        player_sprite = pygame.transform.rotate(Player.sprite, Player.angle * -1)
        window.blit(player_sprite, (Player.x, Player.y))
        pygame.display.update()
        FPS_clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()
    FPS_clock = pygame.time.Clock()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Fighter game')
    pygame.key.set_repeat(10) # Enables direction button to be held
    map = MapGenerator.map(map_size)
    Player = Entities.Player((int(window_size[0]/2),int(window_size[1]/2),90))
    Camera = Entities.Camera(Player, window_size, map)
    game_loop()
