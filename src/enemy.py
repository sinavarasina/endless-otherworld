import pygame
import os
import math


class Enemy:
    def __init__(self, map_width, map_height):
        self.ENEMY_SIZE = 40
        self.enemy_image = pygame.Surface((self.ENEMY_SIZE, self.ENEMY_SIZE))
        self.enemy_image.fill((255, 0, 0))
        self.enemy_width, self.enemy_height = self.enemy_image.get_size()
        self.ENEMY_SPEED = 5
        self.enemy_x = map_width // 2 + 300
        self.enemy_y = map_height // 2 + 300

        self.bullet_image = 0
        self.bullet_x = self.enemy_x
        self.bullet_y = self.enemy_y
        self.bullet_speed = 5
        self.bullet_dx = 0
        self.bullet_dy = 0
        self.bullet_timeout = 0

    def bullet(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(current_dir, "..", "assets", "images")
        bullet_image_path = os.path.join(asset_dir, "purplebullet.png")
        self.bullet_image = pygame.image.load(bullet_image_path).convert_alpha()

    def update_bullet(self, target_x, target_y):
        self.bullet_timeout += 1
        if self.bullet_timeout == 300:
            self.bullet_timeout = 0
            self.bullet_x = self.enemy_x
            self.bullet_y = self.enemy_y

        dx = target_x - self.bullet_x
        dy = target_y - self.bullet_y
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.bullet_dx = dx / distance
            self.bullet_dy = dy / distance

        self.bullet_x += self.bullet_dx * self.bullet_speed
        self.bullet_y += self.bullet_dy * self.bullet_speed

