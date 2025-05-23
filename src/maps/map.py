import pygame
import os
import sys
from .obstacle.stone import Stone


class Map:
    def __init__(self, screen_width, screen_height):
        # keep screen size
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load map image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(current_dir, "..", "..", "assets", "images")
        map_image_path = os.path.join(asset_dir, "Map", "Ground", "map_pbo2.png")

        try:
            self.big_map_image = pygame.image.load(map_image_path).convert()
            self.map_width, self.map_height = self.big_map_image.get_size()
        except pygame.error as e:
            print(f"Error loading map image: {e}")
            print(f"Attempted to load from: {map_image_path}")
            pygame.quit()
            sys.exit()

        # Camera position
        self.camera_x = 0
        self.camera_y = 0

        # --- Obstacles list ---
        self.obstacles = []

        # Load Stones
        obstacle_data = [
            ("StonesFreeWenrexa/14.png", (4000, 4000)),
            ("StonesFreeWenrexa/00.png", (6000, 2000)),
            ("StonesFreeWenrexa/12.png", (2700, 6700)),
            ("StonesFreeWenrexa/13.png", (1600, 3600)),
        ]

        for img_path, pos in obstacle_data:
            full_path = os.path.join(asset_dir, img_path)
            stone = Stone(full_path, pos)
            self.obstacles.append(stone)

    def update_camera(self, target_x, target_y):
        self.camera_x = target_x - self.screen_width // 2
        self.camera_y = target_y - self.screen_height // 2

        self.camera_x = max(0, min(self.camera_x, self.map_width - self.screen_width))
        self.camera_y = max(0, min(self.camera_y, self.map_height - self.screen_height))

    def draw(self, screen):
        visible_area = pygame.Rect(
            self.camera_x, self.camera_y, self.screen_width, self.screen_height
        )
        screen.blit(self.big_map_image, (0, 0), visible_area)

        # --- Draw all obstacles ---
        for obstacle in self.obstacles:
            obstacle_screen_x = obstacle.obstacle_position[0] - self.camera_x
            obstacle_screen_y = obstacle.obstacle_position[1] - self.camera_y
            screen.blit(obstacle.obstacle_image, (obstacle_screen_x, obstacle_screen_y))

    def get_map_size(self):
        return self.map_width, self.map_height

    def get_camera_offset(self):
        return self.camera_x, self.camera_y

    def get_obstacles(self):
        return self.obstacles
