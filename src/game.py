import pygame
import sys
import os
from .character.hero import Hero
from .character.enemy import Enemy
from .maps.map import Map
from .components.sound.bgm import BGM
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

        # Clock
        self.clock = pygame.time.Clock()
        self.running = True
        self.pressed_keys = set()

        self.hero_WASD_animation_now = None

        # initialize music
        self.bgm = BGM()

        # main menu logic
        self.main_menu_screen = MainMenu(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.main_menu = True

        # enemy object list
        self.enemies = []
        # time logic (in second)
        self.tick = 0
        self.second = 0

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

                # WASD keyboard input detection
                Detect_WASD(self, ASSET_DIR)

                # mouse button down detection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down_position_x, mouse_down_position_y = event.pos  # click position
                    mouse_button_down = event.button  # mouse button: 1=left, 2=middle, 3=right

                    world_mouse_x = mouse_down_position_x + camera_x
                    world_mouse_y = mouse_down_position_y + camera_y
                    self.hero.handle_mouse_input(world_mouse_x, world_mouse_y)

            # main menu looping
            if self.main_menu:
                self.main_menu_screen.draw()
                self.map_obj.draw(self.screen)
                self.hero.draw(self.screen, camera_x, camera_y)
                self.hero.update()
                self.bgm.volume = 0.2
                self.bgm.play()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    self.main_menu = False
                    self.bgm.volume = 1
                if keys[pygame.K_ESCAPE]:
                    self.running = False
                self.clock.tick(60)
                continue  # Skip game logic

            self.tick += 1
            keys = pygame.key.get_pressed()

            # Move Hero + collision check
            self.hero.handle_input(keys, obstacle_list=self.map_obj.get_obstacles())
            self.hero.update()
          
            # Draw everything
            self.screen.fill((0, 0, 0))
            self.map_obj.draw(self.screen)
            self.hero.draw(self.screen, camera_x, camera_y)

            # Spawn enemies periodically
            if self.tick % 180 == 0:
                self.enemies.append(Enemy(*self.map_obj.get_map_size(), self.hero.x, self.hero.y))
            
            # Update and draw all enemies
            for enemy in self.enemies[:]:  
                enemy.update()
                enemy.updated(self.hero.x, self.hero.y, obstacle_list=self.map_obj.get_obstacles())
                enemy.draw(self.screen, camera_x, camera_y)
                enemy.bullet.draw(self.screen, camera_x, camera_y)

                # Check enemy bullet collision with hero
                if enemy.bullet.active and enemy.bullet.check_collision(self.hero):
                    #print("Hero hit!") #debug thingy
                    enemy.bullet.active = False
                    self.hero.hp -= 1

                # fuckin' off hp 0's enemies
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
                            #print("Enemy hit!") #it is debug thingy, dont turn on unless u know what u do, lmao
                            self.hero.bullet.active = False
                            enemy.hp -= 1
                            break

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
