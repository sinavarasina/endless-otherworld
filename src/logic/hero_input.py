import pygame
import os

def Detect_WASD(self, ASSET_DIR):
    if self.main_menu == False:
        keys = pygame.key.get_pressed()

        w = keys[pygame.K_w]
        a = keys[pygame.K_a]
        s = keys[pygame.K_s]
        d = keys[pygame.K_d]

        new_animation = None

        horizontal_neutral = a and d
        vertical_neutral = w and s

        # Semua tombol ditekan atau arah saling meniadakan
        if (horizontal_neutral and vertical_neutral) or (a and d and not (w or s)) or (w and s and not (a or d)):
            new_animation = "idle_down.png"

        # Tiga tombol ditekan
        elif w and a and d:
            new_animation = "walk_up.png"
        elif s and a and d:
            new_animation = "walk_down.png"
        elif w and s and a:
            new_animation = "walk_left_down.png"
        elif w and s and d:
            new_animation = "walk_right_down.png"

        # Dua tombol ditekan (diagonal)
        elif w and a:
            new_animation = "walk_left_up.png"
        elif w and d:
            new_animation = "walk_right_up.png"
        elif s and a:
            new_animation = "walk_left_down.png"
        elif s and d:
            new_animation = "walk_right_down.png"

        # Satu tombol ditekan
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

        full_path = os.path.join(ASSET_DIR, "Hero", new_animation)

        if self.hero_WASD_animation_now != full_path:
            self.hero_WASD_animation_now = full_path
            self.hero.set_animation(full_path)
