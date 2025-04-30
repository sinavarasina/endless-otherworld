import pygame
import sys
import os
from .character.hero import Hero
from .character.enemy import Enemy
from .maps.map import Map


class Game:
    def __init__(self):
        pygame.init()

        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1080
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Endless Otherworld")

        # Load Map
        self.map_obj = Map(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Load Hero and Enemy
        self.hero = Hero(*self.map_obj.get_map_size(), self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.enemy = Enemy(*self.map_obj.get_map_size())

        # Clock
        self.clock = pygame.time.Clock()
        self.running = True

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # mouse detection
                if event.type == pygame.MOUSEMOTION:
                    mouse_now_x = event.pos[0] # x mouse position now
                    mouse_now_y = event.pos[1] # y mouse position now
                    rel = event.rel      # position change (dx, dy)

                # mouse button down detection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down_position_x, mouse_down_position_y = event.pos  # click position
                    mouse_button_down = event.button  # mouse button: 1=left, 2=middle, 3=right, 4=upscroll, 5=downscroll
                    print(f"Mouse diklik di posisi ({mouse_down_position_x}, {mouse_down_position_y}) dengan tombol {mouse_button_down}")
                    self.hero.handle_mouse_input(mouse_down_position_x, mouse_down_position_y)

            # dt = self.clock.tick(60)

            keys = pygame.key.get_pressed()

            # Move Hero + collision check
            self.hero.handle_input(keys, obstacle_list=self.map_obj.get_obstacles())

            # Enemy update (chase Hero)
            self.enemy.update(
                self.hero.x, self.hero.y, obstacle_list=self.map_obj.get_obstacles()
            )

            # Update camera based on Hero
            self.map_obj.update_camera(self.hero.x, self.hero.y)
            camera_x, camera_y = self.map_obj.get_camera_offset()

            # Draw everything
            self.screen.fill((0, 0, 0))
            self.map_obj.draw(self.screen)

            self.hero.draw(self.screen, camera_x, camera_y)
            self.enemy.draw(self.screen, camera_x, camera_y)

            self.hero.bullet.update()
            self.hero.bullet.draw(self.screen)
            self.enemy.bullet.draw(self.screen, camera_x, camera_y)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
