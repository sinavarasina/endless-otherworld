# i think this ui is good enough, if you wanna change the ui, please tell me first

import pygame
import os
import json
import random
from path_config import ASSET_DIR
from path_config import FONT_DIR

class GachaMenu:
    @staticmethod
    def load_gacha_data(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data['gacha_items'] 

    def __init__(self, screen, screen_width, screen_height, json_path):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.item_size = (200, 200)

        self.gacha_data = GachaMenu.load_gacha_data(json_path)

        # Shuffle data dan ambil 3 item pertama
        random.shuffle(self.gacha_data)
        self.gacha_data = self.gacha_data[:3]

        self.item_images = []
        self.font = os.path.join(FONT_DIR, "bloodcrow.ttf")
        
        # looping for every image
        for item in self.gacha_data:
            key = list(item.keys())[1]
            image_name = item[key]
            image_path = os.path.join(ASSET_DIR, "GachaItems", image_name)
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, self.item_size)
            self.item_images.append(image)

    # to draw the image from path that in json
    def draw(self):
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        font_title = pygame.font.Font(self.font, 80)
        font_subtitle = pygame.font.Font(self.font, 40)

        title = font_title.render("Choose your faith!", True, (255, 255, 255))
        subtitle2 = font_subtitle.render(
            "Press 1 or 2 or 3 to select the item", True, (200, 200, 200)
        )
        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        subtitle2_rect = subtitle2.get_rect(center=(self.screen_width // 2, self.screen_height - 100))

        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle2, subtitle2_rect)
        
        box_width, box_height = self.item_size
        spacing = 300
        total_width = 3 * box_width + 2 * spacing
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height // 2 - box_height // 2

        
        for i in range(3):
            x = start_x + i * (box_width + spacing)

            # shaking animation to image
            # you wanna got a shake huh >w<
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)

            border = pygame.Surface((box_width + 10, box_height + 10), pygame.SRCALPHA)
            border.fill((255, 255, 255, 0))
            self.screen.blit(border, (x - 5 + offset_x, y - 5 + offset_y))
            self.screen.blit(self.item_images[i], (x + offset_x, y + offset_y))

            # number in the top of items image
            font_number = pygame.font.Font(self.font, 50)
            number_text = font_number.render(str(i + 1), True, (255, 255, 255))
            number_rect = number_text.get_rect(center=(x + box_width // 2, y + box_height - 250))
            self.screen.blit(number_text, number_rect)

            # description from JSON
            font_desc = pygame.font.Font(self.font, 30)
            description = self.gacha_data[i]["Description"]
            desc_text = font_desc.render(description, True, (255, 255, 255))
            desc_rect = desc_text.get_rect(center=(x + box_width // 2, y + box_height + 30))
            self.screen.blit(desc_text, desc_rect)

        pygame.display.flip()
    
    # to update this menu in the game loop and checking to key interrupt
    def update(self, game):
        if game.hero.level != game.hero.level_old:
            self.draw()
            game.bgm.volume = 0.2
            game.bgm.play()

            keys = pygame.key.get_pressed()
            # chose one of the 3 items
            if keys[pygame.K_1]:
                game.main_menu = False
                game.bgm.volume = 1
                game.bgm.play()
                
                # take the effect in json
                item_effect = self.gacha_data[0]["Effect"]
                if item_effect:
                    exec(item_effect)  # execute the python code in json
                            
                game.hero.level_old = game.hero.level

            elif keys[pygame.K_2]:
                game.main_menu = False
                game.bgm.volume = 1
                game.bgm.play()

                # take the effect in json
                item_effect = self.gacha_data[1]["Effect"]
                if item_effect:
                    exec(item_effect)  # execute the python code in json


                game.hero.level_old = game.hero.level
            elif keys[pygame.K_3]:
                game.main_menu = False
                game.bgm.volume = 1
                game.bgm.play()

                # take the effect in json
                item_effect = self.gacha_data[2]["Effect"]
                if item_effect:
                    exec(item_effect)  # execute the python code in json


                game.hero.level_old = game.hero.level
            game.clock.tick(60)
            return True
        return False
