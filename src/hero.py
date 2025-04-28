import pygame


class Hero:
    def __init__(self, map_width, map_height):
        self.PLAYER_SIZE = 40
        self.player_image = pygame.Surface(
            (self.PLAYER_SIZE, self.PLAYER_SIZE)
        ).convert_alpha()
        self.player_image.fill((0, 255, 0))  # Green color
        self.player_width, self.player_height = self.player_image.get_size()
        self.PLAYER_SPEED = 5
        self.player_x = map_width // 2
        self.player_y = map_height // 2
        self.player_mask = pygame.mask.from_surface(self.player_image)

    # src/hero.py

    def move(self, keys, obstacle_list=None):
        move_x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.PLAYER_SPEED
        move_y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.PLAYER_SPEED

        new_x = self.player_x + move_x
        new_y = self.player_y + move_y

        old_x = self.player_x
        old_y = self.player_y

        self.player_x = new_x
        self.player_y = new_y

        if obstacle_list:
            for obstacle in obstacle_list:
                if obstacle.obstacle_collision(self):
                    self.player_x = old_x
                    self.player_y = old_y
                    break

    def draw(self, screen):
        screen.blit(self.player_image, (self.player_x, self.player_y))
