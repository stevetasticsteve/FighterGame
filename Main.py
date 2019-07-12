import pygame
import sys

FPS = 30
Window_width = 640
Window_height = 480
x_center = int(Window_width/2)
y_center = int(Window_height/2)

player_start_x = x_center
player_start_y = y_center

colours = {'White' : (255,255,255),
           'Black' : (0,0,0)}

pygame.init()
FPS_clock = pygame.time.Clock()
window = pygame.display.set_mode((Window_width, Window_height))
pygame.display.set_caption('Fighter game')
pygame.key.set_repeat(10)
plane = pygame.image.load('Assets/Sprites/Plane.png')


class player:
    def __init__(self):
        self.player_size = 10
        self.player_colour = colours['White']
        self.x = player_start_x
        self.y = player_start_y
        self.speed = 10

    def draw(self):
        # pygame.draw.circle(window, self.player_colour, (self.x, self.y), self.player_size)
        window.blit(plane, (self.x, self.y))

    def move(self,x ,y):
        self.x += x * self.speed
        self.y += y * self.speed

def reset_screen():
    window.fill(colours['Black'])

def close_program():
    pygame.quit()
    sys.exit()

player = player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_program()

        # Key bindings
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0,-1)
            if event.key == pygame.K_DOWN:
                player.move(0,1)
            if event.key == pygame.K_LEFT:
                player.move(-1,0)
            if event.key == pygame.K_RIGHT:
                player.move(1,0)
            if event.key == pygame.K_ESCAPE:
                close_program()

    reset_screen()
    player.draw()
    pygame.display.update()
    FPS_clock.tick(FPS)


