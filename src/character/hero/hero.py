import pygame
import math
import os
from path_config import ASSET_DIR
from src.components.get_image import SpriteSheet
from ..bullets.Hero_Bullets.hero_bullet_A import Hero_Bullet_A


class Hero:
    def __init__(self, map_width, map_height):
        # === Hero Initialization ===
        self.speed = 5
        self.x = map_width // 2
        self.y = map_height // 2
        self.hp = 100  # for testing

        self.animation_path = os.path.join(ASSET_DIR, "Hero", "death_normal_down.png")
        self.assets_path = self.animation_path

        # animation
        self.frame_width = 48
        self.frame_height = 64
        self.color_key = (0, 0, 0)
        self.frame_delay = 50
        self.current_frame = 0
        self.frame_timer = 0
        self.animation_speed = 5
        self.scale = 3

        self.set_animation(self.assets_path)
        self.mask = pygame.mask.from_surface(self.frames[0])

        # === Hero Specific Attributes ===
        self.hp_maxcap = 100
        self.hp = self.hp_maxcap
        self.attack = 20
        self.level = 1
        self.level_old = 1  # for logic cheking in gacha menu so if the hero levelup its become not same with the level
        self.lvl_up_shuffle = False
        self.level_bar = 0
        self.exp = 0
        self.bullet = Hero_Bullet_A(owner=self)

        self.xp_base = 1000
        self.xp_factor = 1.25
        self.xp_target = self._calculate_xp_target(self.level)

        self.score = 0

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

    def _calculate_xp_target(self, current_hero_level):
        if current_hero_level < 1:
            return self.xp_base
        xp_needed = self.xp_base * (self.xp_factor ** (current_hero_level - 1))
        return int(xp_needed)

    def _update_level_bar_for_hud(self):
        expected_max_for_hud = self.level * 20
        if expected_max_for_hud <= 0:
            expected_max_for_hud = 20

        if self.xp_target > 0:
            progress_fraction = self.exp / self.xp_target
            self.level_bar = progress_fraction * expected_max_for_hud
            self.level_bar = max(0, min(self.level_bar, expected_max_for_hud))
        else:
            if self.exp > 0:
                self.level_bar = expected_max_for_hud
            else:
                self.level_bar = 0
        self.level_bar = int(self.level_bar)

    def level_update(self):
        self._update_level_bar_for_hud()

        leveled_up_this_call = False
        while self.exp >= self.xp_target:
            self.exp -= self.xp_target
            self.level += 1

            # self.hp = self.hp_maxcap

            self.xp_target = self._calculate_xp_target(self.level)
            leveled_up_this_call = True

            self._update_level_bar_for_hud()

        return leveled_up_this_call

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

    #   def draw_aiming_indicator(self, screen, camera_x, camera_y):
    #       # Get mouse position in world coordinates
    #       mouse_x, mouse_y = pygame.mouse.get_pos()
    #       world_mouse_x = mouse_x + camera_x
    #       world_mouse_y = mouse_y + camera_y
    #
    #       # Calculate angle between hero and mouse
    #       dx = world_mouse_x - self.x
    #       dy = world_mouse_y - self.y
    #       angle = math.atan2(dy, dx)
    #
    #       # Calculate arrow points
    #       arrow_length = 30
    #       arrow_width = 10
    #
    #       # Base of arrow
    #       base_x = (self.x + 75) + math.cos(
    #           angle
    #       ) * 50  # i thought it +50 just as in game.py but it doesnt fit well
    #       base_y = (self.y + 75) + math.sin(
    #           angle
    #       ) * 50  # so i set it to +75 offset to get better (while not perfetcly accurate)
    #
    #       # Tip of arrow
    #       tip_x = base_x + math.cos(angle) * arrow_length
    #       tip_y = base_y + math.sin(angle) * arrow_length
    #
    #       # Side points of arrow
    #       side_angle = angle + math.pi / 2
    #       side1_x = tip_x + math.cos(side_angle) * arrow_width / 2
    #       side1_y = tip_y + math.sin(side_angle) * arrow_width / 2
    #       side2_x = tip_x - math.cos(side_angle) * arrow_width / 2
    #       side2_y = tip_y - math.sin(side_angle) * arrow_width / 2
    #
    #       # Convert to screen coordinates
    #       screen_base = (base_x - camera_x, base_y - camera_y)
    #       screen_tip = (tip_x - camera_x, tip_y - camera_y)
    #       screen_side1 = (side1_x - camera_x, side1_y - camera_y)
    #       screen_side2 = (side2_x - camera_x, side2_y - camera_y)
    #
    #       # Draw the arrow (T arrow tbh lol)
    #       pygame.draw.line(screen, (255, 255, 255), screen_base, screen_tip, 2)
    #       pygame.draw.line(screen, (255, 255, 255), screen_tip, screen_side1, 2)
    #       pygame.draw.line(screen, (255, 255, 255), screen_tip, screen_side2, 2)

    def draw(self, screen, camera_x=0, camera_y=0):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        screen.blit(self.frames[self.current_frame], (screen_x, screen_y))

    #       self.draw_aiming_indicator(
    #           screen, camera_x, camera_y
    #       )  # Draw the aiming indicator
