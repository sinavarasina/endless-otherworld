use bevy::prelude::*;

#[derive(Component, Debug, Default)]
pub struct Enemy;

#[derive(Component, Debug, Clone, Copy, PartialEq, Eq, Reflect)]
pub enum EnemyKind {
    Ghost,
    Flame,
    Demonz,
    Capybara,
}

#[derive(Component, Debug, Clone)]
pub struct EnemyStats {
    pub hp: f32,
    pub max_hp: f32,
    pub speed: f32,
    pub killed_exp: u32,
}

#[derive(Component, Debug, Clone)]
pub struct EnemyShooter {
    pub timer: Timer,
    pub bullet_speed: f32,
    pub bullet_damage: f32,
}
