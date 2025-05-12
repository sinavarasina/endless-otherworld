import pygame
import sys
import os
from .character.hero.hero import Hero
from .maps.map import Map
from .components.sound.bgm import BGM
from path_config import ASSET_DIR
from src.logic.hero_input import Detect_WASD
from src.main_menu.main_menu import MainMenu
from src.logic.enemy_generator import EnemyGenerator

# main_menu
from src.main_menu.main_menu_looping_check import Main_Menu_Looping_Check

# HUD
from src.HUD.time_HUD import Time_HUD


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

        # enemy object list
        self.enemies = []

        self.enemy_generator = EnemyGenerator(self.map_obj, self.hero, self.enemies)

        # Clock
        self.clock = pygame.time.Clock()
        self.running = True
        self.pressed_keys = set()

        self.hero_WASD_animation_now = None

        # initialize music
        self.bgm = BGM()

        # main menu logic
        self.main_menu_screen = MainMenu(
            self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )
        self.main_menu = True

        # time logic (in second)
        self.tick = 0
        self.second = 0

    def start(self):
        self.bgm.play()
        # Font for second display
        font = pygame.font.SysFont(None, 36)

        while self.running:
            # Update camera based on Hero
            self.map_obj.update_camera(self.hero.x, self.hero.y)
            camera_x, camera_y = self.map_obj.get_camera_offset()
            camera_x += 50
            camera_y += 50

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # WASD keyboard input detection
                Detect_WASD(self, ASSET_DIR)

                # mouse button down detection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down_position_x, mouse_down_position_y = (
                        event.pos
                    )  # click position
                    mouse_button_down = (
                        event.button
                    )  # mouse button: 1=left, 2=middle, 3=right

                    world_mouse_x = mouse_down_position_x + camera_x
                    world_mouse_y = mouse_down_position_y + camera_y
                    self.hero.handle_mouse_input(world_mouse_x, world_mouse_y)

            #####################
            # main menu looping #
            #####################
            if Main_Menu_Looping_Check(self, camera_x, camera_y):
                continue
            ####################

            self.tick += 1
            keys = pygame.key.get_pressed()

            # Move Hero + collision check
            self.hero.handle_input(keys, obstacle_list=self.map_obj.get_obstacles())
            self.hero.update()

            # Draw everything
            self.screen.fill((0, 0, 0))
            self.map_obj.draw(self.screen)
            self.hero.draw(self.screen, camera_x, camera_y)

            self.enemy_generator.update()

            # Update and draw all enemies
            for enemy in self.enemies[:]:
                enemy.update_animation()
                enemy.update(
                    self.hero.x, self.hero.y, obstacle_list=self.map_obj.get_obstacles()
                )
                enemy.draw(self.screen, camera_x, camera_y)
                enemy.bullet.draw(self.screen, camera_x, camera_y)

                # Check enemy bullet collision with hero
                if enemy.bullet.active and enemy.bullet.check_collision(self.hero):
                    # print("Hero hit!") #debug thingy
                    enemy.bullet.active = False
                    self.hero.hp -= 1

                # fuckin' off hp 0's enemies. #from faiq: lol this comment is hillarious
                if enemy.hp <= 0:
                    self.enemies.remove(enemy)

            # Update hero bullet
            if self.hero.bullet.active:
                self.hero.bullet.update()
                self.hero.bullet.draw(self.screen, camera_x, camera_y)

                # Check hero bullet collision with enemies
                if self.hero.bullet.active:
                    for enemy in self.enemies[:]:
                        if self.hero.bullet.check_collision(enemy):
                            # print("Enemy hit!") #it is debug thingy, dont turn on unless u know what u do, lmao #from someone: calm down bro its just print lol
                            self.hero.bullet.active = False
                            enemy.hp -= 1
                            break

            ###########
            #   HUD   #
            ###########
            # Render time in right bottom
            Time_HUD(self, font)
            ###########

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
