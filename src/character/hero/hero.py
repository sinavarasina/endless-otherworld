from .hero_base import Hero_Base
import pygame
import math
import os
from ..bullets.Hero_Bullets.hero_bullet_A import Hero_Bullet_A
from path_config import ASSET_DIR


class Hero(Hero_Base):
    def __init__(self, map_width, map_height):
        self.animation_path = os.path.join(ASSET_DIR, "Hero", "death_normal_down.png")
        super().__init__(
            self.animation_path,
            48,
            64,
            (0, 0, 0),
            50,
            5,
            3,
            map_width,
            map_height,
            speed=5,
        )
        self.level = 1
        self.level_old = 1 # for logic cheking in gacha menu so if the hero levelup its become not same with the level
        self.level_bar = 0
        self.exp = 0
        self.bullet = Hero_Bullet_A(owner=self)

    def handle_input(self, keys, obstacle_list=None):
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]

        length = math.sqrt(dx * dx + dy * dy)
        if length > 0:
            dx_normalized = dx / length
            dy_normalized = dy / length
            self.move(dx_normalized, dy_normalized, obstacle_list)
        else:
            self.move(0, 0, obstacle_list)

    def handle_mouse_input(self, x, y):
        self.bullet.shoot(x, y)

    def move(self, dx, dy, obstacle_list=None):
        MAP_WIDTH = 10000
        MAP_HEIGHT = 10000

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        new_x %= MAP_WIDTH
        new_y %= MAP_HEIGHT

        old_x = self.x
        old_y = self.y

        self.x = new_x
        self.y = new_y
        if obstacle_list:
            for obstacle in obstacle_list:
                if obstacle.obstacle_collision(self):
                    self.x = old_x
                    self.y = old_y
                    break

    def level_update(self):
        self.level_bar += 20 / self.level
        if self.level_bar > self.level * 20:
            self.level += 1
            self.level_bar = 0

    def draw_aiming_indicator(self, screen, camera_x, camera_y):
        # Get mouse position in world coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_mouse_x = mouse_x + camera_x
        world_mouse_y = mouse_y + camera_y

        # Calculate angle between hero and mouse
        dx = world_mouse_x - self.x
        dy = world_mouse_y - self.y
        angle = math.atan2(dy, dx)

        # Calculate arrow points
        arrow_length = 30
        arrow_width = 10

        # Base of arrow
        base_x = (self.x + 75) + math.cos(
            angle
        ) * 50  # i thought it +50 just as in game.py but it doesnt fit well
        base_y = (self.y + 75) + math.sin(
            angle
        ) * 50  # so i set it to +75 offset to get better (while not perfetcly accurate)

        # Tip of arrow
        tip_x = base_x + math.cos(angle) * arrow_length
        tip_y = base_y + math.sin(angle) * arrow_length

        # Side points of arrow
        side_angle = angle + math.pi / 2
        side1_x = tip_x + math.cos(side_angle) * arrow_width / 2
        side1_y = tip_y + math.sin(side_angle) * arrow_width / 2
        side2_x = tip_x - math.cos(side_angle) * arrow_width / 2
        side2_y = tip_y - math.sin(side_angle) * arrow_width / 2

        # Convert to screen coordinates
        screen_base = (base_x - camera_x, base_y - camera_y)
        screen_tip = (tip_x - camera_x, tip_y - camera_y)
        screen_side1 = (side1_x - camera_x, side1_y - camera_y)
        screen_side2 = (side2_x - camera_x, side2_y - camera_y)

        # Draw the arrow (inspired by Temple OS cursor, lol)
        pygame.draw.line(screen, (255, 255, 255), screen_base, screen_tip, 2)
        pygame.draw.line(screen, (255, 255, 255), screen_tip, screen_side1, 2)
        pygame.draw.line(screen, (255, 255, 255), screen_tip, screen_side2, 2)

    def draw(self, screen, camera_x=0, camera_y=0):
        super().draw(screen, camera_x, camera_y)
        self.draw_aiming_indicator(
            screen, camera_x, camera_y
        )  # Draw the aiming indicator
