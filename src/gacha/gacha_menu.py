import pygame
import os
import json
from path_config import JSON_DIR

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
        self.item_images = []
        for item in self.gacha_data:
            key = list(item.keys())[0]  # e.g., 'items1'
            image_name = item[key] + ".png"
            image_path = os.path.join(JSON_DIR, "GachaItems", image_name)
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, self.item_size)
            self.item_images.append(image)

    def draw(self):
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 128))  # Transparan hitam
        self.screen.blit(overlay, (0, 0))

        font_title = pygame.font.SysFont(None, 80)
        font_subtitle = pygame.font.SysFont(None, 40)

        title = font_title.render("Choose your faith!", True, (255, 255, 255))
        subtitle2 = font_subtitle.render(
            "Press 1 or 2 or 3 to select the item", True, (200, 200, 200)
        )

        title_rect = title.get_rect(center=(self.screen_width // 2, 100))
        subtitle2_rect = subtitle2.get_rect(center=(self.screen_width // 2, self.screen_height - 100))

        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle2, subtitle2_rect)

        
        box_width, box_height = self.item_size
        spacing = 100
        total_width = 3 * box_width + 2 * spacing
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height // 2 - box_height // 2

        
        for i in range(3):
            x = start_x + i * (box_width + spacing)

            border = pygame.Surface((box_width + 10, box_height + 10), pygame.SRCALPHA)
            border.fill((255, 255, 255, 0))  # transparan putih
            self.screen.blit(border, (x - 5, y - 5))

            self.screen.blit(self.item_images[i], (x, y))

            # number in the top of items image
            font_number = pygame.font.SysFont(None, 50)
            number_text = font_number.render(str(i + 1), True, (255, 255, 255))
            number_rect = number_text.get_rect(center=(x + box_width // 2, y + box_height + 30))
            self.screen.blit(number_text, number_rect)

            # description
            # font_number = pygame.font.SysFont(None, 50)
            # number_text = font_number.render(str(i + 1), True, (255, 255, 255))
            # number_rect = number_text.get_rect(center=(x + box_width // 2, y + box_height - 250))
            # self.screen.blit(number_text, number_rect)

            # description dari JSON
            font_desc = pygame.font.SysFont(None, 30)
            description = self.gacha_data[i]["Description"]
            desc_text = font_desc.render(description, True, (255, 255, 255))
            desc_rect = desc_text.get_rect(center=(x + box_width // 2, y + box_height - 250))
            self.screen.blit(desc_text, desc_rect)

        pygame.display.flip()

    def update(self, game, camera_x, camera_y):
        if game.main_menu:
            self.draw()
            game.map_obj.draw(game.screen)
            game.hero.draw(game.screen, camera_x, camera_y)
            game.hero.update()
            game.bgm.volume = 0.2
            game.bgm.play()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                game.main_menu = False
                game.bgm.volume = 1
                game.bgm.play()
                game.hero.hp = 100
            if keys[pygame.K_ESCAPE]:
                game.running = False
            game.clock.tick(60)
            return True
        return False
