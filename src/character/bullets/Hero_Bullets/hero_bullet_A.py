import pygame
import os
from path_config import ASSET_DIR
from src.character.bullets.bullet import Bullet
from src.logic.collition_logic import CollitionLogic
from src.components.get_image import SpriteSheet
from src.character.bullets.bullet_animation import BulletAnimation


class Hero_Bullet_A(Bullet):
    def __init__(self, owner):
        super().__init__(owner)
        self.speed = 25

        bullet_image_path = os.path.join(
            ASSET_DIR, "Bullet", "BlueShurikenAnimation.png"
        )
        sprite_sheet = SpriteSheet(pygame.image.load(bullet_image_path).convert_alpha())

        self.animation = BulletAnimation(
            sprite_sheet=sprite_sheet,
            frame_width=32,
            frame_height=32,
            scale=2,
            color_key=(0, 0, 0),
            frame_count=4,
            frame_delay=8,
        )

        self.mouse_x = 0
        self.mouse_y = 0
        self.is_shooting = False

    def update_mouse_position(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

    def handle_shoot_input(self):
        if not self.active:
            self.shoot(self.mouse_x, self.mouse_y)
