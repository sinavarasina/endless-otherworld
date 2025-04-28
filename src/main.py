import pygame
import sys
import os
from hero import Hero

# --- Pygame Initialization ---
pygame.init()

# --- Screen Dimensions ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Scrolling Map Game - Moving!")

# --- Load Assets ---
# Safely handle asset path
current_dir = os.path.dirname(os.path.abspath(__file__))
asset_dir = os.path.join(current_dir, '..', 'assets', 'images')
map_image_path = os.path.join(asset_dir, 'grasspattern.png')

try:
    big_map_image = pygame.image.load(map_image_path).convert()
    map_width, map_height = big_map_image.get_size()
except pygame.error as e:
    print(f"Error loading map image: {e}")
    print(f"Attempted to load from: {map_image_path}")
    pygame.quit()
    sys.exit()


# --- Initiate Hero ---
hero = Hero(map_width, map_height)


camera_x = hero.player_x - SCREEN_WIDTH // 2
camera_y = hero.player_y - SCREEN_HEIGHT // 2

# --- Game Loop ---
clock = pygame.time.Clock()
running = True

while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Player Input and Movement ---
    keys = pygame.key.get_pressed()
    move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * hero.PLAYER_SPEED
    move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * hero.PLAYER_SPEED

    hero.player_x += move_x
    hero.player_y += move_y

    # --- Player Boundary Checking ---
    hero.player_x = max(0, min(hero.player_x, map_width - hero.player_width))
    hero.player_y = max(0, min(hero.player_y, map_height - hero.player_height))

    # --- Camera Update ---
    camera_x = hero.player_x - SCREEN_WIDTH // 2
    camera_y = hero.player_y - SCREEN_HEIGHT // 2

    camera_x = max(0, min(camera_x, map_width - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, map_height - SCREEN_HEIGHT))

    # --- Drawing ---
    screen.fill((0, 0, 0))  # Clear screen

    visible_area = pygame.Rect(camera_x, camera_y, SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.blit(big_map_image, (0, 0), visible_area)

    player_screen_x = hero.player_x - camera_x
    player_screen_y = hero.player_y - camera_y
    screen.blit(hero.player_image, (player_screen_x, player_screen_y))

    # --- Update Display ---
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

# --- Quit Pygame ---
pygame.quit()
sys.exit()
