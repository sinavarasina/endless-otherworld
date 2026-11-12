use bevy::prelude::*;

#[derive(Component, Clone, Debug, Reflect)]
pub struct SpriteAnimation {
    pub timer: Timer,
    pub frame_count: usize,
    pub first_index: usize,
}

impl SpriteAnimation {
    pub fn new(frame_count: usize, fps: f32) -> Self {
        Self {
            timer: Timer::from_seconds(1.0 / fps.max(0.1), TimerMode::Repeating),
            frame_count,
            first_index: 0,
        }
    }

    pub fn with_first_index(mut self, index: usize) -> Self {
        self.first_index = index;
        self
    }
}
