from maps.obstacle.obstacle import Obstacle


class Stone(Obstacle):
    def __init__(self, image_dir, pos):
        super().__init__(image_dir, pos)
