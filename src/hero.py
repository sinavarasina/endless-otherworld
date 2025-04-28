import pygame

class Hero():
    def __init__(self, map_width, map_height):
        self.PLAYER_SIZE = 40
        self.player_image = pygame.Surface((self.PLAYER_SIZE, self.PLAYER_SIZE))
        self.player_image.fill((0, 255, 0))
        self.player_width, self.player_height = self.player_image.get_size()
        self.PLAYER_SPEED = 5
        self.player_x = map_width // 2
        self.player_y = map_height // 2

    def move_x(self, keys):
        move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.PLAYER_SPEED
        return move_x
    
    def move_y(self, keys):
        move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.PLAYER_SPEED
        return move_y