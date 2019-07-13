import pygame

class Jet():
    def __init__(self, starting_coordinates):
        self.x = starting_coordinates[0]
        self.y = starting_coordinates[1]
    speed = 10


class Player(Jet):
    def __init__(self, starting_coordinates):
        Jet.__init__(self, starting_coordinates)
        self.sprite = pygame.image.load('Assets/Sprites/Plane.png')

    def move(self, x, y):
        self.x += x * self.speed
        self.y += y * self.speed