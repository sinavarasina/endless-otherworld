from .character import Character
from .bullets.Enemy_Bullets.bullet import Bullet
import math
from path_config import ASSET_DIR
import os

class Enemy(Character):
    def __init__(self, map_width, map_height):
        animation_path = os.path.join(ASSET_DIR, "Enemies", "CasperSprites.png")

        super().__init__(animation_path, 48, 48, (0, 0, 0), 50, 10, 2.5, map_width, map_height)
        self.speed = 2
        self.bullet = Bullet(owner=self)

    # def updated(self, target_x, target_y, obstacle_list=None):
    #     old_x, old_y = self.x, self.y

    #     dx = target_x - self.x
    #     dy = target_y - self.y
    #     distance = math.hypot(dx, dy)

    #     if distance != 0:
    #         self.x += (dx / distance) * self.speed
    #         self.y += (dy / distance) * self.speed

    #     if obstacle_list:
    #         for obstacle in obstacle_list:
    #             if obstacle.obstacle_collision(self):
    #                 self.x = old_x
    #                 self.y = old_y
    #                 break

    #     self.bullet.update(target_x, target_y)

    def updated(self, target_x, target_y, obstacle_list=None):
        MAP_WIDTH = 10000
        MAP_HEIGHT = 10000

        old_x, old_y = self.x, self.y

        target_positions = [
            (target_x, target_y),  
            (target_x + MAP_WIDTH, target_y),  
            (target_x - MAP_WIDTH, target_y), 
            (target_x, target_y + MAP_HEIGHT),  
            (target_x, target_y - MAP_HEIGHT),  
            (target_x + MAP_WIDTH, target_y + MAP_HEIGHT),  
            (target_x + MAP_WIDTH, target_y - MAP_HEIGHT),  
            (target_x - MAP_WIDTH, target_y + MAP_HEIGHT),
            (target_x - MAP_WIDTH, target_y - MAP_HEIGHT)   
        ]
        closest_target = None
        min_distance = float('inf')

        for tx, ty in target_positions:
            dx = tx - self.x
            dy = ty - self.y
            distance = math.hypot(dx, dy)

            if distance < min_distance:
                min_distance = distance
                closest_target = (tx, ty)

        if closest_target:
            tx, ty = closest_target
            dx = tx - self.x
            dy = ty - self.y
            distance = math.hypot(dx, dy)

            if distance != 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed

                self.x %= MAP_WIDTH
                self.y %= MAP_HEIGHT

        if obstacle_list:
            for obstacle in obstacle_list:
                if obstacle.obstacle_collision(self):
                    self.x, self.y = old_x, old_y
                    break
                
        self.bullet.update(target_x, target_y)
