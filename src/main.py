# src/main.py

import pygame
import sys
import os
from character.hero import Hero
from character.enemy import Enemy
from maps.map import Map

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Otherworld")

# --- Load Map
map_obj = Map(SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Load Hero and Enemy
hero = Hero(*map_obj.get_map_size())
enemy = Enemy(*map_obj.get_map_size())

# --- Main Loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move Hero + collision check
    hero.handle_input(keys, obstacle_list=map_obj.get_obstacles())

    # Enemy update (chase Hero)
    enemy.update(hero.x, hero.y, obstacle_list=map_obj.get_obstacles())

    # Update camera based on Hero
    map_obj.update_camera(hero.x, hero.y)
    camera_x, camera_y = map_obj.get_camera_offset()

    # Draw everything
    screen.fill((0, 0, 0))
    map_obj.draw(screen)

    hero.draw(screen, camera_x, camera_y)
    enemy.draw(screen, camera_x, camera_y)
    enemy.bullet.draw(screen, camera_x, camera_y)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
