use bevy::prelude::*;

#[derive(Component, Debug, Default)]
pub struct Player;

#[derive(Component, Debug, Clone)]
pub struct PlayerStats {
    pub hp: f32,
    pub max_hp: f32,
    pub attack: f32,
    pub speed: f32,
    pub bullet_speed: f32,
    pub bullet_anim_speed: f32,
    pub shoot_cooldown: Timer,
}

impl Default for PlayerStats {
    fn default() -> Self {
        Self {
            hp: 100.0,
            max_hp: 100.0,
            attack: 20.0,
            speed: 300.0,
            bullet_speed: 750.0,
            bullet_anim_speed: 8.0,
            shoot_cooldown: Timer::from_seconds(0.2, TimerMode::Once),
        }
    }
}

#[derive(Component, Debug, Clone)]
pub struct PlayerExperience {
    pub level: u32,
    pub exp: u32,
    pub xp_target: u32,
    pub xp_base: u32,
    pub xp_factor: f32,
}

impl Default for PlayerExperience {
    fn default() -> Self {
        let base = 1000;
        Self {
            level: 1,
            exp: 0,
            xp_target: base,
            xp_base: base,
            xp_factor: 1.25,
        }
    }
}

impl PlayerExperience {
    pub fn calculate_xp_target(level: u32, base: u32, factor: f32) -> u32 {
        if level <= 1 {
            return base;
        }
        (base as f32 * factor.powi((level - 1) as i32)) as u32
    }

    /// Adds exp and returns the number of levels gained (if any).
    pub fn add_exp(&mut self, amount: u32) -> u32 {
        self.exp += amount;
        let mut levels_gained = 0;
        while self.exp >= self.xp_target {
            self.exp -= self.xp_target;
            self.level += 1;
            levels_gained += 1;
            self.xp_target = Self::calculate_xp_target(self.level, self.xp_base, self.xp_factor);
        }
        levels_gained
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_xp_target_scaling() {
        let base = 1000;
        let factor = 1.25;

        assert_eq!(PlayerExperience::calculate_xp_target(1, base, factor), 1000);
        assert_eq!(PlayerExperience::calculate_xp_target(2, base, factor), 1250);
        assert_eq!(PlayerExperience::calculate_xp_target(3, base, factor), 1562);
    }

    #[test]
    fn test_add_exp_and_level_up() {
        let mut exp = PlayerExperience::default();
        assert_eq!(exp.level, 1);
        assert_eq!(exp.xp_target, 1000);

        // Add 500 exp (no level up)
        assert_eq!(exp.add_exp(500), 0);
        assert_eq!(exp.level, 1);
        assert_eq!(exp.exp, 500);

        // Add 600 exp (crosses 1000 -> level 2, leftover 100 exp)
        assert_eq!(exp.add_exp(600), 1);
        assert_eq!(exp.level, 2);
        assert_eq!(exp.exp, 100);
        assert_eq!(exp.xp_target, 1250);
    }
}

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum PlayerFacing {
    #[default]
    IdleDown,
    WalkDown,
    WalkUp,
    WalkLeftDown,
    WalkRightDown,
    WalkLeftUp,
    WalkRightUp,
}

#[derive(Component, Debug, Clone)]
pub struct PlayerScore {
    pub score: u32,
    pub survival_seconds: u32,
    pub timer: Timer,
}

impl Default for PlayerScore {
    fn default() -> Self {
        Self {
            score: 0,
            survival_seconds: 0,
            timer: Timer::from_seconds(1.0, TimerMode::Repeating),
        }
    }
}
