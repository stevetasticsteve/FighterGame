import os
import random
import Main

class map:
    def __init__(self):
        tile_size = 64
        map_width = Main.Window_width
        map_height = Main.Window_height

        tiles = ['Assets/Tiles/' + x for x in os.listdir('Assets/Tiles') if x.endswith('.png')]
        horizontal_tiles_number = int(map_width/tile_size)
        vertical_tiles_number = int(map_height/tile_size)

        self.tile_map = {}

        for column in range(horizontal_tiles_number):
            for row in range(vertical_tiles_number):
                self.tile_map[(column, row)] = random.choice(tiles)