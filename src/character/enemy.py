from character.character import Character
from character.bullet import Bullet
import math


class Enemy(Character):
    def __init__(self, map_width, map_height):
        super().__init__(map_width, map_height, size=40, color=(255, 0, 0))
        self.speed = 3
        self.bullet = Bullet(owner=self)

    def update(self, target_x, target_y, obstacle_list=None):
        old_x, old_y = self.x, self.y

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

        if obstacle_list:
            for obstacle in obstacle_list:
                if obstacle.obstacle_collision(self):
                    self.x = old_x
                    self.y = old_y
                    break

        self.bullet.update(target_x, target_y)
