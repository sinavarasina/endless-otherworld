import pygame


class ImageCache:
    def __init__(self):
        self.cache = {}

    def load(self, path):
        if path not in self.cache:
            self.cache[path] = pygame.image.load(path).convert_alpha()
        return self.cache[path]
