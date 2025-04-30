import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height *scale))
        image.set_colorkey(colour)

        return image
    

# use this in global
# import spritesheet

# sprite_sheet_image = pygame.image.load("___.png").convert_alpha()
# sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# black = (0, 0, 0)

# frame_0 = sprite_sheet.get_image(0, 24, 24, 3, black)

# while:
#   screen.blit(frame_0, (0, 0))