import pygame
import os


def Detect_WASD(self, ASSET_DIR):
    keys = pygame.key.get_pressed()

    new_animation = None

    if keys[pygame.K_w] and keys[pygame.K_a]:
        new_animation = "walk_left_up.png"
    elif keys[pygame.K_a] and keys[pygame.K_s]:
        new_animation = "walk_left_down.png"
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        new_animation = "walk_right_down.png"
    elif keys[pygame.K_d] and keys[pygame.K_w]:
        new_animation = "walk_right_up.png"
    elif keys[pygame.K_w]:
        new_animation = "walk_up.png"
    elif keys[pygame.K_a]:
        new_animation = "walk_left_down.png"
    elif keys[pygame.K_s]:
        new_animation = "walk_down.png"
    elif keys[pygame.K_d]:
        new_animation = "walk_right_down.png"
    else:
        new_animation = "idle_down.png"

    full_path = os.path.join(ASSET_DIR, "Hero", new_animation)

    if self.hero_WASD_animation_now != full_path:
        self.hero_WASD_animation_now = full_path
        self.hero.set_animation(full_path)
