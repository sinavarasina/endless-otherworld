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

        bullet_image_path = os.path.join(ASSET_DIR, "Bullet", "BlueShurikenAnimation.png")
        sprite_sheet = SpriteSheet(pygame.image.load(bullet_image_path).convert_alpha())

        self.animation = BulletAnimation(
            sprite_sheet=sprite_sheet,
            frame_width=32,
            frame_height=32,
            scale=2,
            color_key=(0, 0, 0),
            frame_count=4,
            frame_delay=8
        )

