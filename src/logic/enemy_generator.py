import random
from src.character.enemies.common_enemy_demonz import Common_Enemy_Demonz
from src.character.enemies.common_enemy_flame import Common_Enemy_Flame
from src.character.enemies.common_enemy_ghost import Common_Enemy_Ghost

enemy_list = {
    1: Common_Enemy_Ghost,
    2: Common_Enemy_Flame,
    3: Common_Enemy_Demonz,
}


class EnemyGenerator:
    def __init__(self, map_obj, hero, enemies_list, spawn_interval=60):
        self.map_obj = map_obj
        self.hero = hero
        self.enemies = enemies_list
        self.obstacle_list = self.map_obj.get_obstacles()
        self.spawn_interval = spawn_interval
        self.tick = 0

    def __is_valid(self, enemy):
        return not any(
            obstacle.obstacle_collision(enemy) for obstacle in self.obstacle_list
        )

    def __find_valid_position(
        self, enemy_class, map_width, map_height, hero_x, hero_y, max_attempts=10
    ):
        for _ in range(max_attempts):
            spawn_x = hero_x + random.randint(960, 1100) * random.choice([-1, 1])
            spawn_y = hero_y + random.randint(540, 700) * random.choice([-1, 1])
            temp_enemy = enemy_class(spawn_x, spawn_y, map_width, map_height)

            if self.__is_valid(temp_enemy):
                return temp_enemy

        return enemy_class(spawn_x, spawn_y, map_width, map_height)

    def generate(self):
        map_width, map_height = self.map_obj.get_map_size()
        hero_x, hero_y = self.hero.x, self.hero.y
        enemy_class = random.choice(list(enemy_list.values()))
        return self.__find_valid_position(
            enemy_class, map_width, map_height, hero_x, hero_y
        )

    def update(self):
        self.tick += 1
        if self.tick % self.spawn_interval == 0:
            new_enemy = self.generate()
            self.enemies.append(new_enemy)
