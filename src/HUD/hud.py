# src/HUD/hud.py
import pygame


class HUD:
    def __init__(self, game):
        self.game = game
        self.small_font = pygame.font.Font(None, 24)
        self.medium_font = pygame.font.Font(None, 36)

    def draw(self):
        self._draw_hero_hp()
        self._draw_time()
        self._draw_exp()
        self._draw_leveling_bar()

    # i think ist time to use some protected shit
    def _draw_hero_hp(self):
        # hp bar conf
        bar_position = (10, 10)
        bar_width = 200
        bar_height = 20
        border_color = (255, 255, 255)
        fill_color = (0, 255, 0)

        hp_percentage = max(0, min(self.game.hero.hp, 100))
        current_width = int((hp_percentage / 100) * bar_width)

        # Draw HP bar
        pygame.draw.rect(
            self.game.screen, border_color, (*bar_position, bar_width, bar_height), 2
        )
        pygame.draw.rect(
            self.game.screen, fill_color, (*bar_position, current_width, bar_height)
        )

        # Draw HP text
        hp_text = self.small_font.render(
            f"HP: {self.game.hero.hp}", True, (255, 255, 255)
        )
        self.game.screen.blit(hp_text, (10, 35))

    def _draw_time(self):
        # Draw time
        time_text = self.medium_font.render(
            f"Time: {self.game.second}s", True, (255, 255, 255)
        )
        text_rect = time_text.get_rect()
        text_rect.bottomright = (
            self.game.SCREEN_WIDTH - 10,
            self.game.SCREEN_HEIGHT - 10,
        )
        self.game.screen.blit(time_text, text_rect)

    # def _draw_exp(self):
    #    # Draw EXP (now accessed through hero)
    #    exp_text = self.medium_font.render(
    #        f"EXP: {self.game.hero.exp}", True, (255, 255, 255)
    #    )
    #    text_rect = exp_text.get_rect()
    #    text_rect.bottomright = (
    #        self.game.SCREEN_WIDTH - 10,
    #        self.game.SCREEN_HEIGHT - 50,
    #    )
    #    self.game.screen.blit(exp_text, text_rect)
    #
    # def _draw_leveling_bar(self):
    #    # Leveling Bar settings
    #    bar_position = (640, 1000)
    #    bar_width = 700
    #    bar_height = 20
    #    border_color = (255, 255, 255)
    #    fill_color = (0, 255, 0)
    #
    #    level_percentage = max(0, min(self.game.hero.level_bar, self.game.hero.level * 20))
    #    current_width = int((level_percentage / (self.game.hero.level * 20)) * bar_width)
    #
    #    # Draw leveling bar
    #    pygame.draw.rect(
    #        self.game.screen, border_color, (*bar_position, bar_width, bar_height), 2
    #    )
    #    pygame.draw.rect(
    #        self.game.screen, fill_color, (*bar_position, current_width, bar_height)
    #    )
    #
    #    # Draw level text
    #    level_text = self.small_font.render(
    #        f"Level: {self.game.hero.level}", True, (255, 255, 255)
    #    )
    #    self.game.screen.blit(level_text, (640, 1030))  # Below the bar
    #
    #
    #    I THINK TO BE BETTER LIKE BELLOW BUT IF YOU A FE (FLAT EARTHER) THINK THAT WHAT I DO IS HORRIBLE, JUST UNCOMMENT IT
    #    I THINK CLEARER is better

    def _draw_exp(self):
        # Draw EXP text aligned with level text
        exp_text = self.medium_font.render(
            f"EXP: {self.game.hero.exp}", True, (255, 255, 255)
        )

        # Get level text dimensions first
        level_text = self.medium_font.render(
            f"Level: {self.game.hero.level}", True, (255, 255, 255)
        )
        level_text_width = level_text.get_width()

        text_y = self.game.SCREEN_HEIGHT - 30
        # Draw level text (left-aligned)
        self.game.screen.blit(level_text, (30, text_y))

        # Draw EXP text (right after level text with padding)
        self.game.screen.blit(exp_text, (30 + level_text_width + 15, text_y))

    def _draw_leveling_bar(self):
        # Progress bar config (2px height)
        bar_height = 2
        bar_position = (0, self.game.SCREEN_HEIGHT - bar_height)
        bar_width = self.game.SCREEN_WIDTH
        fill_color = (0, 255, 0)  # Green progress
        bg_color = (50, 50, 50)  # Dark background

        level_percentage = max(
            0, min(self.game.hero.level_bar, self.game.hero.level * 20)
        )
        current_width = int(
            (level_percentage / (self.game.hero.level * 20)) * bar_width
        )

        # Draw background and progress
        pygame.draw.rect(
            self.game.screen, bg_color, (*bar_position, bar_width, bar_height)
        )
        pygame.draw.rect(
            self.game.screen, fill_color, (*bar_position, current_width, bar_height)
        )
