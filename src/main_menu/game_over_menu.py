from ..character.hero.hero import Hero
from src.logic.enemy_generator import EnemyGenerator
from src.logic.score_crud import ScoreCRUD
from datetime import timedelta


class GameOverMenu:
    def __init__(self, game) -> None:
        self.game = game

    def reboot_game(self):
        hero = self.game.hero

        duration_str = str(timedelta(seconds=self.game.second))

        score_data = {
            "level": hero.level,
            "score": hero.score,
            "duration": duration_str,
        }
        self.game.score_crud.add_score(score_data)
        print("Skor tersimpan:", score_data)

        hero_x, hero_y = hero.x, hero.y

        self.game.main_menu = True

        self.game.enemies = []

        self.game.hero = Hero(*self.game.map_obj.get_map_size())
        self.game.hero.x = hero_x
        self.game.hero.y = hero_y
        self.game.enemy_generator = EnemyGenerator(
            self.game.map_obj, self.game.hero, self.game.enemies
        )

        self.game.tick = 0
        self.game.second = 0
        # self.game.hero.exp = 0
        # self.game.hero.level = 1
        # self.game.hero.level_bar = 0
        # self.game.hero.score = 0
