import pygame
import os
import math
from src.components.get_image import SpriteSheet
from path_config import ASSET_DIR
from .bullet_animation import BulletAnimation


class Bullet:
    def __init__(self, owner):
        self.owner = owner

        # bullet logic variable
        self.x = 0
        self.y = 0
        self.speed = 8
        self.timeout = 0
        self.vx = 0
        self.vy = 0
        self.active = False

        # animation
        bullet_animation_path = os.path.join(
            ASSET_DIR, "Bullet", "BlueShurikenAnimation.png"
        )
        sprite_sheet_image = pygame.image.load(bullet_animation_path).convert_alpha()
        sprite_sheet = SpriteSheet(sprite_sheet_image)

        self.animation = BulletAnimation(
            sprite_sheet=sprite_sheet,
            frame_width=32,
            frame_height=24,
            scale=2,
            color_key=(0, 0, 0),
            frame_count=6,
            frame_delay=50,
        )

        self.bullet_screen_x = None
        self.bullet_screen_y = None

    def shoot(self, target_x, target_y):
        if not self.active:
            self.x = self.owner.x + (self.owner.frame_width * self.owner.scale) // 2
            self.y = self.owner.y + (self.owner.frame_height * self.owner.scale) // 2
            print(f"{self.owner.x}, {self.owner.y}")
            print(f"{self.x}, {self.y}")

            dx = target_x - self.x
            dy = target_y - self.y

            length = math.hypot(dx, dy)
            if length != 0:
                self.vx = (dx / length) * self.speed
                self.vy = (dy / length) * self.speed
            else:
                self.vx = 0
                self.vy = 0

            self.active = True
            self.timeout = 0

    def update(self):
        if self.active:
            self.x += self.vx
            self.y += self.vy

        self.timeout += 1

        if self.timeout > 40:
            self.active = False
            self.timeout = 0

        self.animation.update()

    def draw(self, screen, camera_x=0, camera_y=0):
        self.bullet_screen_x = self.x - camera_x
        self.bullet_screen_y = self.y - camera_y
        if self.active:
            screen.blit(
                self.animation.get_current_frame(),
                (self.bullet_screen_x, self.bullet_screen_y),
            )

    @property
    def mask(self):
        return self.animation.get_mask()
