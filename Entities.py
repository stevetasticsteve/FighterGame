import pygame
import math

class Jet():
    def __init__(self, starting_coordinates):
        self.x = starting_coordinates[0]
        self.y = starting_coordinates[1]
        self.angle = starting_coordinates[2]
        # angle defined as 0 degrees North, 90 deg East etc.
    speed = 10
    acceleration = 2
    rotation_speed = 10
    maximum_speed = 20
    minimum_speed = 2


class Player(Jet):
    def __init__(self, starting_coordinates):
        Jet.__init__(self, starting_coordinates)
        self.sprite = pygame.image.load('Assets/Sprites/Plane.png')

    def move(self):
        self.y -= self.speed * math.cos(math.radians(self.angle))
        self.x += self.speed * math.sin(math.radians(self.angle))

    def rotate(self, direction):
        self.angle += direction * self.rotation_speed

    def accelerate(self, direction):
        self.speed += direction * self.acceleration