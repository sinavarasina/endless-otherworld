import pygame
import os
import math

class Hero_Bullet_A:
    def __init__(self, owner, Screen_Width, Screen_Height):
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
        
        self.Base_x = Screen_Width/2
        self.Base_y = Screen_Height/2

        self.x = Screen_Width/2
        self.y = Screen_Height/2
        self.speed = 50
        self.timeout = 0

        self.vx = 0
        self.vy = 0

        self.active = False

    def Shoot(self, Screen_Width, Screen_Height, x, y):
        if not self.active:
            self.x = self.Base_x
            self.y = self.Base_y

            dx = x - self.x
            dy = y - self.y

            length = math.hypot(dx, dy)
            if length == 0:
                self.vx = 0
                self.vy = 0
            else:
                self.vx = (dx / length) * self.speed
                self.vy = (dy / length) * self.speed

            self.active = True
            self.timeout = 0

        

    def update(self):
        if self.active:
            self.x += self.vx
            self.y += self.vy
        
        self.timeout += 1  # ✔️ timeout dihitung per frame

        if self.timeout > 20:
            self.x = self.Base_x
            self.y = self.Base_y
            self.active = False
            self.timeout = 0  # reset timeout jika peluru dimatikan

    def draw(self, screen, camera_x=0, camera_y=0):
        bullet_screen_x = self.x - camera_x
        bullet_screen_y = self.y - camera_y
        screen.blit(self.image, (bullet_screen_x, bullet_screen_y))