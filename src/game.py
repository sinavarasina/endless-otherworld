import pygame
import sys
import os
from .character.hero import Hero
from .character.enemy import Enemy
from .maps.map import Map
from path_config import ASSET_DIR
from src.logic.hero_input import Detect_WASD
from src.main_menu.main_menu import MainMenu


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
        self.hero = Hero(
            *self.map_obj.get_map_size(), self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )
        self.enemy = Enemy(*self.map_obj.get_map_size())

        # Clock
        self.clock = pygame.time.Clock()
        self.running = True
        self.pressed_keys = set()

        # Set
        self.hero_WASD_animation_now = None

        # main menu logic
        # self.background_run_one_time = 0
        self.main_menu_screen = MainMenu(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.main_menu = True

    def start(self):
        while self.running:
            # Update camera based on Hero
            self.map_obj.update_camera(self.hero.x, self.hero.y)
            camera_x, camera_y = self.map_obj.get_camera_offset()
            camera_x += 50
            camera_y += 50

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # mouse detection
                # if event.type == pygame.MOUSEMOTION:
                #     mouse_now_x = event.pos[0]  # x mouse position now
                #     mouse_now_y = event.pos[1]  # y mouse position now
                #     rel = event.rel  # position change (dx, dy)

                # WASD keyboard input detection
                Detect_WASD(self, ASSET_DIR)

                # mouse button down detection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down_position_x, mouse_down_position_y = (
                        event.pos
                    )  # click position
                    mouse_button_down = event.button  # mouse button: 1=left, 2=middle, 3=right, 4=upscroll, 5=downscroll

                    ################
                    # debug thingy #
                    ################

                    # print(
                    #    f"Mouse diklik di posisi ({mouse_down_position_x}, {mouse_down_position_y}) dengan tombol {mouse_button_down}"
                    # )

                    world_mouse_x = mouse_down_position_x + camera_x
                    world_mouse_y = mouse_down_position_y + camera_y
                    self.hero.handle_mouse_input(world_mouse_x, world_mouse_y)

            # main menu looping
            if self.main_menu == True:
                self.main_menu_screen.draw()
                self.map_obj.draw(self.screen)
                self.hero.draw(self.screen, camera_x, camera_y)
                self.hero.update()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.main_menu = False
                if keys[pygame.K_ESCAPE]:
                    self.running = False
                self.clock.tick(60)
                continue  # Skip game logic

            keys = pygame.key.get_pressed()

            # Move Hero + collision check
            self.hero.handle_input(keys, obstacle_list=self.map_obj.get_obstacles())
            self.hero.update()

            self.enemy.update()

            # Enemy update (chase Hero)
            self.enemy.updated(
                self.hero.x, self.hero.y, obstacle_list=self.map_obj.get_obstacles()
            )
            # Draw everything
            self.screen.fill((0, 0, 0))
            self.map_obj.draw(self.screen)

            self.hero.draw(self.screen, camera_x, camera_y)
            self.enemy.draw(self.screen, camera_x, camera_y)

            self.hero.bullet.update()
            self.hero.bullet.draw(self.screen, camera_x, camera_y)
            self.enemy.bullet.draw(self.screen, camera_x, camera_y)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()
