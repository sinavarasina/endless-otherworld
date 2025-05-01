
def Collition_Detection(self):
    Bullet_hero_mask = self.hero.bullet.mask
    Enemy_mask = self.enemy.mask

    Position_Hero_Bullet_x = self.hero.bullet.x
    Position_Hero_Bullet_y = self.hero.bullet.y
    Position_Enemy_x = self.enemy.x
    Position_Enemy_y = self.enemy.y

    print(f"postionbull:({Position_Hero_Bullet_x}, {Position_Hero_Bullet_y}) and positionenemy : ({Position_Enemy_x}, {Position_Enemy_y})")
    print(f"screenbullet:({self.hero.bullet.bullet_screen_x}, {self.hero.bullet.bullet_screen_y})")
    offset = (Position_Enemy_x - Position_Hero_Bullet_x, Position_Enemy_y - Position_Hero_Bullet_y)

    if Bullet_hero_mask.overlap(Enemy_mask, offset):
        print("overlap")