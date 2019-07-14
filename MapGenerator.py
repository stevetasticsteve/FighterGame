import os
import random

class map:
    def __init__(self, map_size):
        self.tile_size = 64
        self.map_width = map_size[0]
        self.map_height = map_size[1]
        self.tiles = ['Assets/Tiles/' + x for x in os.listdir('Assets/Tiles') if x.endswith('.png')]

        self.tile_map = []
        for column in range(0,self.map_width, self.tile_size):
            for row in range(0, self.map_height, self.tile_size):
                tile_coordinate = (column, row)
                tile = self.select_tile()
                self.tile_map.append((tile_coordinate, tile))

    def select_tile(self):
        tile = random.choice(self.tiles)
        return tile