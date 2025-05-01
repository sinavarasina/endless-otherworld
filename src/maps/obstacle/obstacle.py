import pygame


class Obstacle:
    def __init__(self, image_dir, pos):
        self.obstacle_image = pygame.image.load(image_dir).convert_alpha()
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_image)
        self.obstacle_position = pos

    def obstacle_collision(self, char_obj):
        offset = (
            (char_obj.x - 50) - self.obstacle_position[0],
            (char_obj.y - 50) - self.obstacle_position[1],
        )
        return self.obstacle_mask.overlap(char_obj.mask, offset) is not None

    def draw(self, screen):
        screen.blit(self.obstacle_image, self.obstacle_position)
