import pygame
import math
import random

class Camera:
    #TODO figure out how to handle map edges and decide on reasonable map size
    def __init__(self, player, window_size, map):
        self.camera_width = window_size[0]
        self.camera_height = window_size[1]
        self.player = player
        self.map = map
        self.Move()


    def Move(self):
        self.rect = (self.player.x - int(self.camera_width/2), self.player.y - int(self.camera_height/2),
                     self.player.x + int(self.camera_width/2), self.player.y + int(self.camera_height/2))

    def Active_tiles(self):
        # returns a list of tile tuples(x,y,img) that are currently around the player
        # and within the range of the camera
        active_tiles = []
        for tile in self.map.tile_map:
            if tile[0][0] in range(self.rect[0]-64, self.rect[2]+64):
                if tile[0][1]in range(self.rect[1]-64, self.rect[3]+64):
                    active_tiles.append(tile)
        return active_tiles


class Jet:
    speed = 10
    acceleration = 2
    rotation_speed = 10
    maximum_speed = 20
    minimum_speed = 2

    def __init__(self, starting_coordinates):
        self.x = starting_coordinates[0]
        self.y = starting_coordinates[1]
        self.angle = starting_coordinates[2]
        # angle defined as 0 degrees North, 90 deg East etc.


    def move(self):
        self.y -= int(self.speed * math.cos(math.radians(self.angle)))
        self.x += int(self.speed * math.sin(math.radians(self.angle)))

    def rotate(self, direction):
        self.angle += direction * self.rotation_speed

    def accelerate(self, direction):
        if self.speed == self.maximum_speed:
            if direction == -1:
                self.speed += direction * self.acceleration
        elif self.speed == self.minimum_speed:
            if direction == 1:
                self.speed += direction * self.acceleration
        else:
            self.speed += direction * self.acceleration



class Player(Jet):
    def __init__(self, starting_coordinates):
        Jet.__init__(self, starting_coordinates)
        self.sprite = pygame.image.load('Assets/Sprites/Plane.png')

    def Status(self):
        print('Speed = ' + str(self.speed))
        print('Direction = ' + str(self.angle) + ' degrees')


class Enemy(Jet):
    def __init__(self, starting_coordinates):
        Jet.__init__(self, starting_coordinates)
        self.sprite = pygame.image.load('Assets/Sprites/Plane.png')
        self.behaviours = (self.turn_left,self.turn_right, self.do_nothing)
        self.speed = 2
        self.behaviour = self.do_nothing
        self.last_behaviour = self.do_nothing
        self.last_behaviour_time = 0

    def move(self):
        super().move()
        self.last_behaviour_time += 1

    def choose_behaviour(self):
        if self.last_behaviour == self.turn_left:
            self.behaviour = self.do_nothing
        elif self.last_behaviour == self.turn_right:
            self.behaviour = self.do_nothing
        else:
            self.behaviour = random.choice(self.behaviours)
            self.behaviour_duration = random.randint(5,30)
        self.behaviour()
        self.last_behaviour = self.behaviour

    def turn_left(self):
        if self.last_behaviour_time < self.behaviour_duration:
            self.rotate(-1)

    def turn_right(self):
        if self.last_behaviour_time < self.behaviour_duration:
            self.rotate(1)

    def do_nothing(self):
        pass

    def within_active_area(self, Camera):
        if self.x in range (Camera.rect[0], Camera.rect[2]):
            if self.y in range(Camera.rect[1], Camera.rect[3]):
                return True