import pygame

from src.logic.collition_logic import CollitionLogic


class Obstacle:
    def __init__(self, image_dir, pos):
        self.obstacle_image = pygame.image.load(image_dir).convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obstacle_position = pos
        self.collision_detector = CollitionLogic()

    def obstacle_collision(self, char_obj):
        char_pos = (char_obj.x - 50, char_obj.y - 50)
        return self.collision_detector.collision_check(
            char_pos, char_obj.mask, self.obstacle_position, self.obstacle_mask
        )

    def draw(self, screen):
        screen.blit(self.obstacle_image, self.obstacle_position)
