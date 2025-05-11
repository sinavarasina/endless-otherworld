import pygame

def Main_Menu_Looping_Check(self, camera_x, camera_y):
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
            self.bgm.play()
        if keys[pygame.K_ESCAPE]:
            self.running = False
        self.clock.tick(60)
        return True
    return False
