import pygame

def Hero_HP_HUD(self, font):
    bar_position = (10, 10)
    bar_width = 200
    bar_height = 20 
    border_color = (255, 255, 255)
    fill_color = (0, 255, 0)

    hp_percentage = max(0, min(self.hero.hp, 100))
    current_width = int((hp_percentage / 100) * bar_width)

    pygame.draw.rect(self.screen, border_color, (*bar_position, bar_width, bar_height), 2)
    pygame.draw.rect(self.screen, fill_color, (*bar_position, current_width, bar_height))

    font = pygame.font.Font(None, 24)
    hp_text = font.render(f"HP: {self.hero.hp}", True, (255, 255, 255))
    self.screen.blit(hp_text, (10, 35))  # Di bawah bar
