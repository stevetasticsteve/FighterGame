import os
import random
import Main

class map:
    def __init__(self):
        tile_size = 64
        self.map_width = 800
        self.map_height = 600

        tiles = ['Assets/Tiles/' + x for x in os.listdir('Assets/Tiles') if x.endswith('.png')]
        horizontal_tiles_number = int(self.map_width/tile_size)
        vertical_tiles_number = int(self.map_height/tile_size)

        self.tile_coordinates = []

        self.tile_map = {}

        for column in range(horizontal_tiles_number):
            for row in range(vertical_tiles_number):
                tile_coordinate = (column, row)
                self.tile_map[tile_coordinate] = random.choice(tiles)