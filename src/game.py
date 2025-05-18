import pygame
import sys
from .character.hero.hero import Hero
from .maps.map import Map
from .components.sound.bgm import BGM
from path_config import ASSET_DIR
from src.main_menu.main_menu import MainMenu
from src.main_menu.game_over_menu import GameOverMenu

from src.logic.enemy_generator import EnemyGenerator
from src.logic.control import Control
from src.HUD.time_HUD import Time_HUD
from src.HUD.hero_hp_HUD import Hero_HP_HUD
from src.HUD.xp_HUD import Xp_HUD
from src.HUD.leveling_bar_HUD import Leveling_Bar_HUD


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
            *self.map_obj.get_map_size()
        )

        # enemy object list
        self.enemies = []

        self.enemy_generator = EnemyGenerator(self.map_obj, self.hero, self.enemies)

        # Clock
        self.clock = pygame.time.Clock()
        self.running = True
        self.pressed_keys = set()

        self.control = Control(self, ASSET_DIR)

        # initialize music
        self.bgm = BGM()

        # main menu logic
        self.main_menu_screen = MainMenu(
            self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )
        self.main_menu = True

        self.game_over_menu = GameOverMenu(self)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu = True

                self.control.detect_WASD()
                self.control.handle_mouse_input(event, camera_x, camera_y)
            
            # main menu
            if self.main_menu_screen.update(self, camera_x, camera_y):
                continue

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
                    self.hero.hp -= 10

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
                            # self.hero.bullet.active = False
                            enemy.hp -= 25
                            self.hero.xp += 1
                            break

            ###########
            #   HUD   #
            ###########
            # Render time in right bottom
            Time_HUD(self, font)
            Hero_HP_HUD(self, font)
            Xp_HUD(self, font)
            Leveling_Bar_HUD(self, font)
            ###########

            # if hero die/hp < 1
            if self.hero.hp < 1:
                self.game_over_menu.reboot_game()

            if self.tick % 60 == 0:
                self.second += 1
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
