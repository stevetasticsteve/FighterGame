import unittest
import Entities
import pygame

test_map_size = (1000,1000)

class TestEntities(unittest.TestCase):
    def setUp(self):
        self.player = Entities.Player((100, 100, 0), test_map_size)
        self.enemy = Entities.Enemy((110, 110, 0), test_map_size)

    def test_move(self):
        self.player.move()
	# Assume purely vertical motion
	# Check y coordinate
        self.assertEqual(self.player.y, 100 - self.player.speed)
        # Check collision box coordinates

        last_pos = (self.player.x, self.player.y)
        self.player.angle = 45
        self.player.move()
        self.assertEqual(self.player.x, last_pos[0] + self.player.speed / 2)
        self.assertEqual(self.player.y, last_pos[1] - self.player.speed / 2)

    def test_accelerate(self):
        original_speed = self.player.speed
        self.player.accelerate(1)
        # speed up
        self.assertEqual(self.player.speed, original_speed + self.player.acceleration)
        # slow down
        self.player.accelerate(-1)
        self.assertEqual(self.player.speed, original_speed)
        # can't go below minimum speed
        for i in range(50):
            self.player.accelerate(-1)
        self.assertEqual(self.player.speed, self.player.minimum_speed)
        # can't go above maximum speed
        for i in range(50):
            self.player.accelerate(1)
        self.assertEqual(self.player.speed, self.player.maximum_speed)

    def test_normalize_angle(self):
        self.assertEqual(self.player.normalize_angle(27), 27)
        self.assertEqual(self.player.normalize_angle(-90), 270)
        self.assertEqual(self.player.normalize_angle(-91.5), 268)
        self.assertEqual(self.player.normalize_angle(1.9), 1)
        self.assertEqual(self.player.normalize_angle(181), 181)

    def test_player_angle(self):
        def new_angle(x, y, ans):
            self.enemy.x, self.enemy.y = x, y
            self.assertEqual(self.enemy.player_angle(self.player), ans)

        self.assertEqual(self.enemy.player_angle(self.player), 315)
        new_angle(100, 110, 0)  # S
        new_angle(90, 110, 44)  # SW
        new_angle(90, 100, 90)  # W
        new_angle(90, 90, 135)  # NW
        new_angle(100, 90, 180)  # N
        new_angle(110, 90, 225)  # NE
        new_angle(110, 100, 270)  # E
        new_angle(100, 100, self.player.angle)  # @player

        self.player.x = 0
        self.player.y = 0
        new_angle(0, 0, 0)
        new_angle(-1, -1, 135)  # NW
        new_angle(0, -1, 180)  # N
        new_angle(1, -1, 225)  # NE
        new_angle(1, 0, 270)  # E
        new_angle(1, 1, 315)  # SE
        new_angle(0, 1, 0)  # S
        new_angle(-1, 1, 44)  # SW
        new_angle(-1, 0, 90)  # W

        new_angle(314, -92, 253)  # NE
        new_angle(-70, -206, 161)  # NW
        new_angle(-20, 73, 15)  # SW
        new_angle(123, 54, 293)  # SE


class TestMainGame(unittest.TestCase):
    def test_screen_coordinate_converter(self):
        pass


if __name__ == '__main__':
    unittest.main()
