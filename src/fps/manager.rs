use bevy::prelude::*;
use bevy::window::PresentMode;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FpsLimit {
    Vsync,
    Cap(u32),
    Uncapped,
}

impl FpsLimit {
    pub const PRESETS: [FpsLimit; 9] = [
        FpsLimit::Vsync,
        FpsLimit::Cap(30),
        FpsLimit::Cap(60),
        FpsLimit::Cap(75),
        FpsLimit::Cap(120),
        FpsLimit::Cap(144),
        FpsLimit::Cap(180),
        FpsLimit::Cap(240),
        FpsLimit::Uncapped,
    ];

    pub fn next(&self) -> Self {
        let current_index = Self::PRESETS.iter().position(|p| p == self).unwrap_or(0);
        let next_index = (current_index + 1) % Self::PRESETS.len();
        Self::PRESETS[next_index]
    }

    pub fn display_name(&self) -> String {
        match self {
            FpsLimit::Vsync => "VSync (Monitor Hz)".to_string(),
            FpsLimit::Cap(val) => format!("{} FPS", val),
            FpsLimit::Uncapped => "Uncapped".to_string(),
        }
    }

    pub fn target_present_mode(&self) -> PresentMode {
        match self {
            FpsLimit::Vsync => PresentMode::AutoVsync,
            _ => PresentMode::AutoNoVsync,
        }
    }
}

#[derive(Resource, Debug)]
pub struct FpsManager {
    pub limit: FpsLimit,
    pub visible: bool,
    pub current_fps: f32,
    pub frame_counter: u32,
    pub update_timer: Timer,
}

impl Default for FpsManager {
    fn default() -> Self {
        Self {
            limit: FpsLimit::Vsync,
            visible: true,
            current_fps: 60.0,
            frame_counter: 0,
            update_timer: Timer::from_seconds(0.5, TimerMode::Repeating),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fps_limit_cycle() {
        let mut limit = FpsLimit::Vsync;
        assert_eq!(limit.display_name(), "VSync (Monitor Hz)");

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Cap(30));

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Cap(60));

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Cap(75));

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Cap(120));

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Cap(144));

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Cap(180));

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Cap(240));

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Uncapped);

        limit = limit.next();
        assert_eq!(limit, FpsLimit::Vsync);
    }
}
