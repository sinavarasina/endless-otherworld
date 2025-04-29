from .character import Character
import pygame
import math
from .bullets.hero_bullet_A import Hero_Bullet_A


class Hero(Character):
    def __init__(self, map_width, map_height, Screen_Width, Screen_Height):
        super().__init__(map_width, map_height, size=40, color=(0, 255, 0), speed=5)
        self.bullet = Hero_Bullet_A(owner=self, Screen_Width=Screen_Width, Screen_Height=Screen_Height)

    def handle_input(self, keys, obstacle_list=None):
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.move(dx, dy, obstacle_list)

    def handle_mouse_input(self,Screen, Screen_Width, Screen_Height, x, y):
        self.bullet.Shoot(Screen_Width, Screen_Height, x, y)
        