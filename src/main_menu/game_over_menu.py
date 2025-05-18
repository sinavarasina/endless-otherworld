from ..character.hero.hero import Hero
from src.logic.enemy_generator import EnemyGenerator

class GameOverMenu:
    def __init__(self, game) -> None:
        self.game = game

    
    def reboot_game(self):
        self.game.main_menu = True
        self.game.enemies = []

        # Reset Hero
        self.game.hero = Hero(
            *self.game.map_obj.get_map_size(),
        )

        # Reset Enemy Generator
        self.game.enemy_generator = EnemyGenerator(
            self.game.map_obj,
            self.game.hero,
            self.game.enemies
        )

        # Reset waktu dan XP
        self.game.tick = 0
        self.game.second = 0
        self.game.xp = 0

