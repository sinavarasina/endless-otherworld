from .character import Character
from .bullets.Enemy_Bullets.bullet import Bullet
import math
from path_config import ASSET_DIR
import os

class Enemy(Character):
    def __init__(self, map_width, map_height):
        animation_path = os.path.join(ASSET_DIR, "Enemies", "CasperSprites.png")

        super().__init__(animation_path, 48, 48, (0, 0, 0), 50, 30, 3, map_width, map_height)
        self.speed = 3
        self.bullet = Bullet(owner=self)

    def updated(self, target_x, target_y, obstacle_list=None):
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
