import pygame


class Character:
    def __init__(self, map_width, map_height, size=40, color=(255, 255, 255), speed=5):
        self.size = size
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.fill(color)
        self.width, self.height = self.image.get_size()
        self.speed = speed
        self.x = map_width // 2
        self.y = map_height // 2
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dx, dy, obstacle_list=None):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        old_x = self.x
        old_y = self.y

        self.x = new_x
        self.y = new_y

        if obstacle_list:
            for obstacle in obstacle_list:
                if obstacle.obstacle_collision(self):
                    self.x = old_x
                    self.y = old_y
                    break

    def draw(self, screen, camera_x=0, camera_y=0):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        screen.blit(self.image, (screen_x, screen_y))
