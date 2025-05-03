from .character import Character
import pygame
import math
import os
from .bullets.Hero_Bullets.hero_bullet_A import Hero_Bullet_A
from src.components.get_image import SpriteSheet
from path_config import ASSET_DIR


class Hero(Character):
    def __init__(self, map_width, map_height, Screen_Width, Screen_Height):
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

        self.bullet = Hero_Bullet_A(owner=self)

    def handle_input(self, keys, obstacle_list=None):
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.move(dx, dy, obstacle_list)

    def handle_mouse_input(self, x, y):
        self.bullet.shoot(x, y)
