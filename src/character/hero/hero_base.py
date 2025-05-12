import pygame
import os
from path_config import ASSET_DIR
from src.components.get_image import SpriteSheet


class Hero_Base:
    def __init__(
        self,
        assets_path,
        frame_width,
        frame_height,
        color_key,
        frame_delay,
        animation_speed,
        scale,
        map_width,
        map_height,
        speed=5,
    ):
        self.speed = speed
        self.x = map_width // 2
        self.y = map_height // 2
        self.hp = 100 # for testing

        self.assets_path = assets_path

        # animation
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.color_key = color_key  # (0, 0, 0)
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.frame_timer = 0
        self.animation_speed = animation_speed
        self.scale = scale

        self.set_animation(assets_path)

        self.mask = pygame.mask.from_surface(self.frames[0])

    def set_animation(self, assets_path):
        self.sprite_sheet = SpriteSheet(pygame.image.load(assets_path))
        self.frames = [
            self.sprite_sheet.get_image(
                i, self.frame_width, self.frame_height, self.scale, self.color_key
            )
            for i in range(6)
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.mask = pygame.mask.from_surface(self.frames[0])

    def update(self):
        # animation
        self.frame_timer += self.animation_speed
        if self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

        self.mask = pygame.mask.from_surface(self.frames[self.current_frame])

    def draw(self, screen, camera_x=0, camera_y=0):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        screen.blit(self.frames[self.current_frame], (screen_x, screen_y))
