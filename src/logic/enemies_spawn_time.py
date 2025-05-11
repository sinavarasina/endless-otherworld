from ..character.enemies.common_enemy_ghost import Common_Enemy_Ghost

def Enemies_Spawn_Time(self):
    # Spawn enemies periodically
    if self.tick % 60 == 0:
        self.enemies.append(Common_Enemy_Ghost(*self.map_obj.get_map_size(), self.hero.x, self.hero.y))
        # update the time every 60 tick
        self.second += 1

    
