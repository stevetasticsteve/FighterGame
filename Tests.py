import unittest
import Entities
import os


class TestEntities(unittest.TestCase):
    def setUp(self):
        self.player = Entities.Player((100,100,0))
        self.enemy = Entities.Enemy((110,110,0))

    def test_player_attributes(self):
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 100)
        self.assertEqual(self.player.angle, 0)
        self.assertEqual(self.player.speed, 2)
        self.player.move()
        self.assertEqual(self.player.x, 100)
        self.assertEqual(self.player.y, 100 - self.player.speed)
        self.assertEqual(self.player.angle, 0)
        self.assertEqual(self.player.speed, 2)


    def test_player_angle(self):
        # self.assertEqual(self.enemy.player_angle(self.player), 315)

        def new_angle(x,y,ans):
            self.enemy.x, self.enemy.y = x, y
            self.assertEqual(self.enemy.player_angle(self.player), ans)

        new_angle(100,110,0)
        new_angle(90,110,45)
        new_angle(90,100,90)
        new_angle(90,90,135)
        new_angle(100,90,180)
        new_angle(110,90,225)
        new_angle(110,100,270)
        new_angle(100,100,0)

        self.player.x = 0
        self.player.y = 0
        new_angle(0, 0, 0)
        new_angle(-1, -1, 135) # NW
        new_angle(0, -1, 180) # N
        new_angle(1, -1, 225) # NE
        new_angle(1, 0, 270) # E
        new_angle(1, 1, 315) # SE
        new_angle(0, 1, 0) # S
        new_angle(-1, 1, 45) # SW
        new_angle(-1, 0, 90) # W



class TestMainGame(unittest.TestCase):
    def test_screen_coordinate_converter(self):
        pass


if __name__ == '__main__':
    unittest.main()