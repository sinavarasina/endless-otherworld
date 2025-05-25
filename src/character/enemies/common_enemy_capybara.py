from ..bullets.Enemy_Bullets.enemy_bullet_capybara import EnemyBulletCapybara
from .enemy_base import Enemy_Base
import math
from path_config import ASSET_DIR
import os
# import random


class Common_Enemy_Capybara(Enemy_Base):
    def __init__(self, spawn_x, spawn_y, map_width, map_height):
        animation_path = os.path.join(ASSET_DIR, "Enemies", "capybara.png")

        super().__init__(
            animation_path, 64, 70, (0, 0, 0), 50, 10, 2.5, map_width, map_height
        )
        self.speed = 2
        self.bullet = EnemyBulletCapybara(owner=self)
        self.hp = 100  # for testing, i use 1 hp
        self.killed_exp = 95
        # moved to EnemyGenerator, i kept it commented out as backup
        # if smtg fvck up happen
        # self.x = hero_x + random.randint(960, 1100) * random.choice([-1, 1])
        # self.y = hero_y + random.randint(540, 700) * random.choice([-1, 1])
        self.x = spawn_x
        self.y = spawn_y

    def update(self, target_x, target_y, obstacle_list=None):
        MAP_WIDTH = 10000
        MAP_HEIGHT = 10000

        old_x, old_y = self.x, self.y

        target_positions = [
            (target_x, target_y),
            (target_x + MAP_WIDTH, target_y),
            (target_x - MAP_WIDTH, target_y),
            (target_x, target_y + MAP_HEIGHT),
            (target_x, target_y - MAP_HEIGHT),
            (target_x + MAP_WIDTH, target_y + MAP_HEIGHT),
            (target_x + MAP_WIDTH, target_y - MAP_HEIGHT),
            (target_x - MAP_WIDTH, target_y + MAP_HEIGHT),
            (target_x - MAP_WIDTH, target_y - MAP_HEIGHT),
        ]

        closest_target = None
        min_distance = float("inf")

        for tx, ty in target_positions:
            dx = tx - self.x
            dy = ty - self.y
            distance = math.hypot(dx, dy)

            if distance < min_distance:
                min_distance = distance
                closest_target = (tx, ty)

        if closest_target:
            tx, ty = closest_target
            dx = tx - self.x
            dy = ty - self.y
            distance = math.hypot(dx, dy)

            if distance != 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed

                self.x %= MAP_WIDTH
                self.y %= MAP_HEIGHT

        if obstacle_list:
            for obstacle in obstacle_list:
                if obstacle.obstacle_collision(self):
                    self.x, self.y = old_x, old_y
                    break

        self.bullet.update(target_x, target_y)

    def draw(self, screen, camera_x=0, camera_y=0):
        super().draw(screen, camera_x, camera_y)
        self.bullet.draw(screen, camera_x, camera_y)
