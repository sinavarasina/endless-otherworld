import pygame
import os
import math
from path_config import ASSET_DIR

class Bullet:
    def __init__(self, owner):
        self.owner = owner
        bullet_image_path = os.path.join(ASSET_DIR, "Bullet", "purplebullet.png")
        self.image = pygame.image.load(bullet_image_path).convert_alpha()

        self.x = owner.x
        self.y = owner.y
        self.speed = 15
        self.dx = 0
        self.dy = 0
        self.timeout = 1
        self.vx = 0
        self.vy = 0
        self.active = False

    def update(self, target_x, target_y):
        target_x += 24
        target_y += 32
        print(f"hero x: {target_x}, hero y: {target_y}")
        print(f"enemy x: {self.owner.x}, enemy y: {self.owner.y}")
        if self.timeout == 150:
            self.timeout = 0
            self.x = self.owner.x
            self.y = self.owner.y
            self.vx = 0
            self.vy = 0
            self.active = False

        dx = target_x - self.x
        dy = target_y - self.y

        length = math.hypot(dx, dy)
        if self.timeout == 0:
            self.vx = (dx / length) * self.speed
            self.vy = (dy / length) * self.speed
            self.active = True

        self.x += self.vx
        self.y += self.vy
        self.timeout += 1

    def draw(self, screen, camera_x=0, camera_y=0):
        if self.active:
            bullet_screen_x = self.x - camera_x
            bullet_screen_y = self.y - camera_y
            screen.blit(self.image, (bullet_screen_x, bullet_screen_y))
