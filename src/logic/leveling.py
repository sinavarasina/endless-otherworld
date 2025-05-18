#solo leveling yeah baby!!!!!!

def Leveling(self):
    self.hero.level_bar += (1 / self.hero.level )
    if self.hero.level_bar > self.hero.level * 20:
        self.hero.level += 1
        self.hero.level_bar = 0

