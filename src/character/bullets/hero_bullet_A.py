import pygame
import os
import math

class Hero_Bullet_A:
    def __init__(self, owner):
        self.owner = owner
        current_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(
            current_dir,
            "..",
            "..",
            "..",
            "assets",
            "images",
        )
        bullet_image_path = os.path.join(asset_dir, "Bullet", "purplebullet.png")
        self.image = pygame.image.load(bullet_image_path).convert_alpha()

        self.x = owner.x
        self.y = owner.y
        self.speed = 5
        self.dx = 0
        self.dy = 0
        self.timeout = 0

    def update(self, target_x, target_y):
        self.timeout += 1
        if self.timeout == 300:
            self.timeout = 0
            self.x = self.owner.x
            self.y = self.owner.y

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            self.dx = dx / distance
            self.dy = dy / distance

        self.x += self.dx * self.speed
        
    def draw(self, screen, camera_x=0, camera_y=0):
        bullet_screen_x = self.x - camera_x
        bullet_screen_y = self.y - camera_y
        screen.blit(self.image, (bullet_screen_x, bullet_screen_y))