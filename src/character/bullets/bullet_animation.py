import pygame


class BulletAnimation:
    def __init__(
        self,
        sprite_sheet,
        frame_width,
        frame_height,
        scale,
        color_key,
        frame_count,
        frame_delay,
    ):
        self.frames = [
            sprite_sheet.get_image(i, frame_width, frame_height, scale, color_key)
            for i in range(frame_count)
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = frame_delay
        self.animation_speed = 8
        self.mask = pygame.mask.from_surface(self.frames[0])

    def update(self):
        self.frame_timer += self.animation_speed
        if self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

        self.mask = pygame.mask.from_surface(self.frames[self.current_frame])

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def get_mask(self):
        return self.mask
