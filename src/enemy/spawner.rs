use bevy::prelude::*;
use rand::Rng;

use crate::animation::components::SpriteAnimation;
use crate::combat::components::Collider;
use crate::core::constants::*;
use crate::enemy::assets::EnemyAssets;
use crate::enemy::components::{Enemy, EnemyKind, EnemyShooter, EnemyStats};
use crate::player::components::{Player, PlayerExperience};
use crate::world::components::Obstacle;

#[derive(Resource)]
pub struct EnemySpawner {
    pub timer: Timer,
}

impl Default for EnemySpawner {
    fn default() -> Self {
        Self {
            timer: Timer::from_seconds(3.0, TimerMode::Repeating),
        }
    }
}

pub fn spawn_enemies_system(
    mut commands: Commands,
    time: Res<Time>,
    mut spawner: ResMut<EnemySpawner>,
    enemy_assets: Res<EnemyAssets>,
    player_q: Query<(&Transform, &PlayerExperience), With<Player>>,
    obstacles_q: Query<(&Transform, &Collider), With<Obstacle>>,
) {
    let Ok((player_transform, exp)) = player_q.get_single() else {
        return;
    };

    // Calculate dynamic spawn interval based on player level: max(20, 180 - level * 5) frames
    let frame_interval = 180_i32.saturating_sub((exp.level as i32) * 5).max(20);
    let interval_secs = (frame_interval as f32) / 60.0;
    spawner.timer.set_duration(std::time::Duration::from_secs_f32(interval_secs));

    spawner.timer.tick(time.delta());
    if !spawner.timer.just_finished() {
        return;
    }

    let mut rng = rand::thread_rng();
    let player_pos = player_transform.translation.truncate();

    let kind = match rng.gen_range(0..4) {
        0 => EnemyKind::Ghost,
        1 => EnemyKind::Flame,
        2 => EnemyKind::Demonz,
        _ => EnemyKind::Capybara,
    };

    let (hp, exp_reward, collider_radius) = match kind {
        EnemyKind::Ghost => (200.0, 100, 32.0),
        EnemyKind::Flame => (75.0, 60, 24.0),
        EnemyKind::Demonz => (80.0, 90, 24.0),
        EnemyKind::Capybara => (110.0, 90, 40.0),
    };

    // Attempt to find a valid spawn position not intersecting obstacles
    let mut chosen_pos = player_pos;
    for _ in 0..10 {
        let sign_x = if rng.gen_bool(0.5) { 1.0 } else { -1.0 };
        let sign_y = if rng.gen_bool(0.5) { 1.0 } else { -1.0 };
        let offset_x = rng.gen_range(960.0..1150.0) * sign_x;
        let offset_y = rng.gen_range(540.0..750.0) * sign_y;

        let test_pos = Vec2::new(
            (player_pos.x + offset_x).clamp(50.0, MAP_SIZE - 50.0),
            (player_pos.y + offset_y).clamp(50.0, MAP_SIZE - 50.0),
        );

        let test_collider = Collider::new(collider_radius);
        let collides = obstacles_q.iter().any(|(obs_transform, obs_collider)| {
            test_collider.intersects(test_pos, obs_collider, obs_transform.translation.truncate())
        });

        if !collides {
            chosen_pos = test_pos;
            break;
        }
    }

    let (image, layout, frame_count, scale) = enemy_assets.get_enemy_render_info(kind);

    commands.spawn((
        Enemy,
        kind,
        EnemyStats {
            hp,
            max_hp: hp,
            speed: 130.0,
            killed_exp: exp_reward,
        },
        EnemyShooter {
            timer: Timer::from_seconds(2.5, TimerMode::Repeating),
            bullet_speed: 450.0,
            bullet_damage: 10.0,
        },
        Collider::new(collider_radius),
        Sprite {
            image,
            texture_atlas: Some(TextureAtlas {
                layout,
                index: 0,
            }),
            ..default()
        },
        SpriteAnimation::new(frame_count, 8.0),
        Transform::from_xyz(chosen_pos.x, chosen_pos.y, Z_ENEMY).with_scale(Vec3::splat(scale)),
    ));
}
