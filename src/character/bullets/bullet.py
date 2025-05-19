import pygame
import os
import math
from src.components.get_image import SpriteSheet
from path_config import ASSET_DIR
from .bullet_animation import BulletAnimation
from src.logic.collition_logic import CollitionLogic


class Bullet:
    def __init__(self, owner):
        self.owner = owner
        self.collision_logic = CollitionLogic()

        # bullet logic variables
        self.x = 0
        self.y = 0
        self.speed = 20
        self.timeout = 0
        self.vx = 0
        self.vy = 0
        self.active = False
        self.animation = None  # just implememy it at child class, in order to not make this class complicated, kay?
        self.image = (
            None  # if it not animated then use image instead of animated bullet
        )

    def shoot(self, target_x, target_y):
        if not self.active:
            # adding -50 here to compensate the +50 offset cammera on game.py
            self.x = (
                self.owner.x - 50 + (self.owner.frame_width * self.owner.scale) // 2
            )
            self.y = (
                self.owner.y - 50 + (self.owner.frame_height * self.owner.scale) // 2
            )

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

        if self.animation:
            self.animation.update()

    def draw(self, screen, camera_x=0, camera_y=0):
        if self.active:
            bullet_screen_x = self.x - camera_x
            bullet_screen_y = self.y - camera_y
            if self.animation:
                screen.blit(
                    self.animation.get_current_frame(),
                    (bullet_screen_x, bullet_screen_y),
                )
            elif self.image:
                screen.blit(self.image, (bullet_screen_x, bullet_screen_y))

    def check_collision(self, target):
        if not self.active:
            return False
        return self.collision_logic.collision_check(
            (self.x, self.y),
            self.mask,
            (target.x, target.y),
            target.mask,
        )

    @property
    def mask(self):
        if self.animation:
            return self.animation.get_mask()
        elif self.image:
            return pygame.mask.from_surface(self.image)
        return None
