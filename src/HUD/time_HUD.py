def Time_HUD(self, font):
    time_text = font.render(f"Time: {self.second}s", True, (255, 255, 255))
    text_rect = time_text.get_rect()
    text_rect.bottomright = (self.SCREEN_WIDTH - 10, self.SCREEN_HEIGHT - 10)
    self.screen.blit(time_text, text_rect)
