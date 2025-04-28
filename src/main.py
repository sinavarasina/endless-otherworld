# src/main.py

import pygame
import sys
import os
from hero import Hero
from enemy import Enemy
from maps.map import Map

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Scrolling Map Game - Moving!")

# --- Load Map
map_obj = Map(SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Load Hero
hero = Hero(*map_obj.get_map_size())
enemy = Enemy(*map_obj.get_map_size())
enemy.bullet()

# --- Main Loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Move Hero + collision check
    hero.move(keys, obstacle_list=map_obj.get_obstacles())

    # Update camera
    map_obj.update_camera(hero.player_x, hero.player_y)

    # Draw
    screen.fill((0, 0, 0))
    map_obj.draw(screen)

    # Draw Hero
    camera_x, camera_y = map_obj.get_camera_offset()
    player_screen_x = hero.player_x - camera_x
    player_screen_y = hero.player_y - camera_y
    screen.blit(hero.player_image, (player_screen_x, player_screen_y))

    # Draw Enemy
    enemy_screen_x = enemy.enemy_x - camera_x
    enemy_screen_y = enemy.enemy_y - camera_y
    screen.blit(enemy.enemy_image, (enemy_screen_x, enemy_screen_y))

    enemy_screen_x = enemy.enemy_x - camera_x - 30
    enemy_screen_y = enemy.enemy_y - camera_y + 30
    screen.blit(enemy.bullet_image, (enemy_screen_x, enemy_screen_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
