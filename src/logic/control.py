import pygame
import os


class Control:
    def __init__(self, game, asset_dir):
        self.game = game
        self.asset_dir = asset_dir
        self.hero_WASD_animation_now = None

    def detect_WASD(self):
        if self.game.main_menu:
            return

        keys = pygame.key.get_pressed()
        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        s = keys[pygame.K_s]
        d = keys[pygame.K_d]

        new_animation = None

        horizontal_neutral = a and d
        vertical_neutral = w and s

        if (
            (horizontal_neutral and vertical_neutral)
            or (a and d and not (w or s))
            or (w and s and not (a or d))
        ):
            new_animation = "idle_down.png"
        elif w and a and d:
            new_animation = "walk_up.png"
        elif s and a and d:
            new_animation = "walk_down.png"
        elif w and s and a:
            new_animation = "walk_left_down.png"
        elif w and s and d:
            new_animation = "walk_right_down.png"
        elif w and a:
            new_animation = "walk_left_up.png"
        elif w and d:
            new_animation = "walk_right_up.png"
        elif s and a:
            new_animation = "walk_left_down.png"
        elif s and d:
            new_animation = "walk_right_down.png"
        elif w:
            new_animation = "walk_up.png"
        elif a:
            new_animation = "walk_left_down.png"
        elif s:
            new_animation = "walk_down.png"
        elif d:
            new_animation = "walk_right_down.png"
        else:
            new_animation = "idle_down.png"

        full_path = os.path.join(self.asset_dir, "Hero", new_animation)

        if self.hero_WASD_animation_now != full_path:
            self.hero_WASD_animation_now = full_path
            self.game.hero.set_animation(full_path)

    def handle_mouse_input(self, event, camera_x, camera_y):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            mouse_x, mouse_y = event.pos
            world_x = mouse_x + camera_x
            world_y = mouse_y + camera_y
            self.game.hero.handle_mouse_input(world_x, world_y)
