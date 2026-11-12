use bevy::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Reflect)]
pub enum BulletFaction {
    Player,
    Enemy,
}

#[derive(Component, Debug, Clone)]
pub struct Bullet {
    pub damage: f32,
    pub speed: f32,
    pub direction: Vec2,
    pub lifetime: Timer,
    pub faction: BulletFaction,
}

#[derive(Component, Debug, Clone, Copy, Reflect)]
pub struct Collider {
    pub radius: f32,
}

impl Collider {
    pub fn new(radius: f32) -> Self {
        Self { radius }
    }

    pub fn intersects(&self, pos_a: Vec2, other: &Collider, pos_b: Vec2) -> bool {
        let distance_sq = pos_a.distance_squared(pos_b);
        let radius_sum = self.radius + other.radius;
        distance_sq <= radius_sum * radius_sum
    }
}

#[derive(Event, Debug, Clone)]
pub struct DamageEvent {
    pub target: Entity,
    pub amount: f32,
}

#[derive(Event, Debug, Clone)]
pub struct LevelUpEvent {
    pub new_level: u32,
}

#[derive(Event, Debug, Clone)]
pub struct GameOverEvent {
    pub level: u32,
    pub final_score: u32,
    pub survival_seconds: u32,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_collider_intersection() {
        let col_a = Collider::new(10.0);
        let col_b = Collider::new(10.0);

        // Touching or overlapping (distance 15 < 20)
        assert!(col_a.intersects(Vec2::new(0.0, 0.0), &col_b, Vec2::new(15.0, 0.0)));

        // Non-overlapping (distance 25 > 20)
        assert!(!col_a.intersects(Vec2::new(0.0, 0.0), &col_b, Vec2::new(25.0, 0.0)));
    }
}
