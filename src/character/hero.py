from .character import Character
import pygame


class Hero(Character):
    def __init__(self, map_width, map_height):
        super().__init__(map_width, map_height, size=40, color=(0, 255, 0), speed=5)

    def handle_input(self, keys, obstacle_list=None):
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.move(dx, dy, obstacle_list)
