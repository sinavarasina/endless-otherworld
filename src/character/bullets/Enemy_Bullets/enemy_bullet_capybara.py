from typing import override
import pygame
import os
import math
from path_config import ASSET_DIR
from src.character.bullets.bullet import Bullet
from src.logic.collition_logic import CollitionLogic
from src.components.get_image import SpriteSheet
from src.character.bullets.bullet_animation import BulletAnimation


class EnemyBulletCapybara(Bullet):
    def __init__(self, owner):
        super().__init__(owner)
        self.speed = 15
        self.timeout = 1

        bullet_image_path = os.path.join(ASSET_DIR, "Bullet", "bluetornadobullet.png")
        sprite_sheet = SpriteSheet(pygame.image.load(bullet_image_path).convert_alpha())

        self.animation = BulletAnimation(
            sprite_sheet=sprite_sheet,
            frame_width=32,
            frame_height=32,
            scale=2,
            color_key=(0, 0, 0),
            frame_count=4,
            frame_delay=10,
        )

    @override  # even python override it by default, but yeah we just define it, for reports
    def update(self, target_x=None, target_y=None):
        if target_x is None or target_y is None:
            return super().update()

        target_x += 24
        target_y += 32

        if self.timeout == 150:
            self.reset_bullet()

        dx = target_x - self.x
        dy = target_y - self.y
        length = math.hypot(dx, dy)

        if self.timeout == 0 and length != 0:
            self.vx = (dx / length) * self.speed
            self.vy = (dy / length) * self.speed
            self.active = True

        if self.active:
            self.x += self.vx
            self.y += self.vy

        self.timeout += 1
        if self.animation:
            self.animation.update()

    def reset_bullet(self):
        self.timeout = 0
        self.x = self.owner.x
        self.y = self.owner.y
        self.vx = 0
        self.vy = 0
        self.active = False
