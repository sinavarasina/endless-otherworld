import pygame
import os
import sys
import json
from src.maps.obstacle.obstacle import Obstacle
from src.logic.image_cache import ImageCache


class Map:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load map image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        asset_dir = os.path.join(current_dir, "..", "..", "assets", "images")
        map_image_path = os.path.join(asset_dir, "Map", "Ground", "maptile.png")

        try:
            self.big_map_image = pygame.image.load(map_image_path).convert()
            self.map_width, self.map_height = self.big_map_image.get_size()
        except pygame.error as e:
            print(f"Error loading map image: {e}")
            pygame.quit()
            sys.exit()

        # Camera
        self.camera_x = 0
        self.camera_y = 0

        # Image cache
        self.image_cache = ImageCache()

        # Load obstacle data from JSON
        self.obstacles = []
        config_path = os.path.join(current_dir, "..", "config", "obstacle.json")
        try:
            with open(config_path, "r") as f:
                obstacle_data = json.load(f)
        except Exception as e:
            print(f"Error loading obstacle config: {e}")
            obstacle_data = []

        for entry in obstacle_data:
            image_rel_path = entry["image"]
            position = tuple(entry["position"])
            image_path = os.path.join(asset_dir, image_rel_path)
            try:
                image_surface = self.image_cache.load(image_path)
                obstacle = Obstacle(image_surface, position)
                self.obstacles.append(obstacle)
            except Exception as e:
                print(f"Failed loading image {image_path}: {e}")

    def update_camera(self, target_x, target_y):
        self.camera_x = max(
            0,
            min(target_x - self.screen_width // 2, self.map_width - self.screen_width),
        )
        self.camera_y = max(
            0,
            min(
                target_y - self.screen_height // 2, self.map_height - self.screen_height
            ),
        )

    def draw(self, screen):
        visible_area = pygame.Rect(
            self.camera_x, self.camera_y, self.screen_width, self.screen_height
        )
        screen.blit(self.big_map_image, (0, 0), visible_area)

        for obstacle in self.obstacles:
            screen_x = obstacle.obstacle_position[0] - self.camera_x
            screen_y = obstacle.obstacle_position[1] - self.camera_y
            screen.blit(obstacle.obstacle_image, (screen_x, screen_y))

    def get_map_size(self):
        return self.map_width, self.map_height

    def get_camera_offset(self):
        return self.camera_x, self.camera_y

    def get_obstacles(self):
        return self.obstacles
