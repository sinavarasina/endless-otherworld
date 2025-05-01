import pygame
import os
import math
from src.components.get_image import SpriteSheet
from path_config import ASSET_DIR

class Hero_Bullet_A:
    def __init__(self, owner, Screen_Width, Screen_Height):
        self.owner = owner

        #bullet logic variable
        self.Base_x = Screen_Width/2
        self.Base_y = Screen_Height/2
        self.x = Screen_Width/2
        self.y = Screen_Height/2
        self.speed = 8
        self.timeout = 0
        self.vx = 0
        self.vy = 0
        self.active = False

        #animation
        self.frame_width = 32
        self.frame_height = 24
        self.color_key = (0, 0, 0)
        self.frame_delay = 50
        self.current_frame = 0
        self.frame_timer = 0
        self.animation_speed = 8
        self.scale = 2

        bullet_animation_path = os.path.join(ASSET_DIR, "Bullet", "BlueShurikenAnimation.png")
        sprite_sheet_image = pygame.image.load(bullet_animation_path).convert_alpha()
        self.sprite_sheet = SpriteSheet(sprite_sheet_image)

        self.frames = [self.sprite_sheet.get_image(i, self.frame_width, self.frame_height, self.scale, self.color_key)
                       for i in range(6)]

        #collition detection
        self.mask = pygame.mask.from_surface(self.frames[0])
        self.bullet_screen_x = None
        self.bullet_screen_y = None


    def Shoot(self, x, y):
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

        self.timeout += 1

        if self.timeout > 40:
            self.x = self.Base_x
            self.y = self.Base_y
            self.active = False
            self.timeout = 0 

        #animation
        self.frame_timer += self.animation_speed
        if self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

        self.mask = pygame.mask.from_surface(self.frames[self.current_frame])

    def draw(self, screen, camera_x=0, camera_y=0):
        self.bullet_screen_x = self.x - camera_x
        self.bullet_screen_y = self.y - camera_y
        if self.active:
            screen.blit(self.frames[self.current_frame], (self.bullet_screen_x, self.bullet_screen_y))