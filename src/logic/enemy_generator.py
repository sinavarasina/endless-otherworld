import random
from src.character.enemies.common_enemy_demonz import Common_Enemy_Demonz
from src.character.enemies.common_enemy_flame import Common_Enemy_Flame
from src.character.enemies.common_enemy_ghost import Common_Enemy_Ghost

enemy_list = {1: Common_Enemy_Ghost, 2: Common_Enemy_Flame, 3: Common_Enemy_Demonz}


class EnemyGenerator:
    def __init__(self, map_obj, hero, enemies_list, spawn_interval=60):
        self.map_obj = map_obj
        self.hero = hero
        self.enemies = enemies_list
        self.spawn_interval = spawn_interval
        self.tick = 0
        self.second = 0

    def generate(self):
        map_width, map_height = self.map_obj.get_map_size()
        hero_x, hero_y = self.hero.x, self.hero.y
        enemy_class = random.choice(list(enemy_list.values()))
        return enemy_class(map_width, map_height, hero_x, hero_y)

    def update(self):
        self.tick += 1
        if self.tick % self.spawn_interval == 0:
            new_enemy = self.generate()
            self.enemies.append(new_enemy)
            self.second += 1
