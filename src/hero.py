import pygame
import sys
import os

# current_dir = os.path.dirname(os.path.abspath(__file__))
# asset_dir = os.path.join(current_dir, '..', 'assets', 'images')
# map_image_path = os.path.join(asset_dir, 'grasspattern.png')
# try:
#     big_map_image = pygame.image.load(map_image_path).convert()
#     map_width, map_height = big_map_image.get_size()
# except pygame.error as e:
#     print(f"Error loading map image: {e}")
#     print(f"Attempted to load from: {map_image_path}")
#     pygame.quit()
#     sys.exit()

class Hero():
    def __init__(self, map_width, map_height):
        self.PLAYER_SIZE = 40
        self.player_image = pygame.Surface((self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_image.fill((0, 255, 0))
        self.player_width, self.player_height = self.player_image.get_size()
        self.PLAYER_SPEED = 5
        self.player_x = map_width // 2
        self.player_y = map_height // 2