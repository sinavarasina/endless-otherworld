import pygame
from .game_over_menu import GameOverMenu


class MainMenu:
    def __init__(self, screen, screen_width, screen_height, game):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game = game
        self.gameover = GameOverMenu(game)

    def draw(self):
        overlay = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 128))  # Transparan hitam
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 80)
        title = font.render("Endless Otherworld", True, (255, 255, 255))
        subtitle = pygame.font.SysFont(None, 40).render(
            "Press Enter to Start", True, (200, 200, 200)
        )
        subtitle2 = pygame.font.SysFont(None, 40).render(
            "Esc to Quit", True, (200, 200, 200)
        )

        title_rect = title.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 300)
        )
        subtitle_rect = subtitle.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 300)
        )
        subtitle2_rect = subtitle2.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 350)
        )
        self.game.hud.draw_for_menu()
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        self.screen.blit(subtitle2, subtitle2_rect)
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
