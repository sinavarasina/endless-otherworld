from ..character.hero.hero import Hero
from src.logic.enemy_generator import EnemyGenerator


class GameOverMenu:
    def __init__(self, game) -> None:
        self.game = game

    def reboot_game(self):
        # keep old position
        hero_x = self.game.hero.x
        hero_y = self.game.hero.y

        # activate the main menu
        self.game.main_menu = True

        # empty the enemy
        self.game.enemies = []

        # recreate hero
        self.game.hero = Hero(
            *self.game.map_obj.get_map_size(),
        )

        # make sure character in the same place as their died
        self.game.hero.x = hero_x
        self.game.hero.y = hero_y

        # reset enemies
        self.game.enemy_generator = EnemyGenerator(
            self.game.map_obj, self.game.hero, self.game.enemies
        )

        # Reset time and XP
        self.game.tick = 0
        self.game.second = 0
        self.game.hero.exp = 0
        self.game.hero.level = 1
        self.game.hero.level_bar = 0
