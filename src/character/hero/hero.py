from .hero_base import Hero_Base
import pygame
import math
import os
from ..bullets.Hero_Bullets.hero_bullet_A import Hero_Bullet_A
from path_config import ASSET_DIR


class Hero(Hero_Base):
    def __init__(self, map_width, map_height):
        self.animation_path = os.path.join(ASSET_DIR, "Hero", "death_normal_down.png")
        super().__init__(
            self.animation_path,
            48,
            64,
            (0, 0, 0),
            50,
            5,
            3,
            map_width,
            map_height,
            speed=5,
        )
        self.level = 1
        self.level_bar = 0
        self.exp = 0
        self.bullet = Hero_Bullet_A(owner=self)

    def handle_input(self, keys, obstacle_list=None):
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]

        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx_normalized = dx / length
            dy_normalized = dy / length
            self.move(dx_normalized, dy_normalized, obstacle_list)
        else:
            self.move(0, 0, obstacle_list)

    def handle_mouse_input(self, x, y):
        self.bullet.shoot(x, y)

    def move(self, dx, dy, obstacle_list=None):
        MAP_WIDTH = 10000
        MAP_HEIGHT = 10000

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        new_x %= MAP_WIDTH
        new_y %= MAP_HEIGHT

        old_x = self.x
        old_y = self.y

        self.x = new_x
        self.y = new_y
        if obstacle_list:
            for obstacle in obstacle_list:
                if obstacle.obstacle_collision(self):
                    self.x = old_x
                    self.y = old_y
                    break
