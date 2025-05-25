from .obstacle import Obstacle
from path_config import ASSET_DIR
import os


class Stone(Obstacle):
    BASE_PATH = "assets/stone/stone"
    IMAGE_PATH = BASE_PATH + ".png"
    
    def __init__(self, pos, image_dir=None):
        pos = (1000, 1200)
        
        if image_dir is None:
            image_dir = os.path.join(ASSET_DIR, "images", "stone", "stone.png")
        image_dir = os.path.normpath(image_dir)
        super().__init__(image_dir, pos)
