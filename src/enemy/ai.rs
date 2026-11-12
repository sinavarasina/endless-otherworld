use bevy::prelude::*;

use crate::animation::components::SpriteAnimation;
use crate::combat::components::{Bullet, BulletFaction, Collider};
use crate::core::constants::*;
use crate::enemy::assets::EnemyAssets;
use crate::enemy::components::{Enemy, EnemyKind, EnemyShooter, EnemyStats};
use crate::player::components::Player;
use crate::world::components::Obstacle;

#[allow(clippy::type_complexity)]
pub fn enemy_movement_system(
    time: Res<Time>,
    player_q: Query<&Transform, With<Player>>,
    mut enemies_q: Query<(&EnemyKind, &EnemyStats, &mut Transform, &Collider), (With<Enemy>, Without<Player>)>,
    obstacles_q: Query<(&Transform, &Collider), (With<Obstacle>, Without<Enemy>)>,
) {
    let Ok(player_transform) = player_q.get_single() else {
        return;
    };
    let player_pos = player_transform.translation.truncate();
    let dt = time.delta_secs();

    let target_offsets = [
        Vec2::ZERO,
        Vec2::new(MAP_SIZE, 0.0),
        Vec2::new(-MAP_SIZE, 0.0),
        Vec2::new(0.0, MAP_SIZE),
        Vec2::new(0.0, -MAP_SIZE),
        Vec2::new(MAP_SIZE, MAP_SIZE),
        Vec2::new(MAP_SIZE, -MAP_SIZE),
        Vec2::new(-MAP_SIZE, MAP_SIZE),
        Vec2::new(-MAP_SIZE, -MAP_SIZE),
    ];

    for (kind, stats, mut transform, collider) in enemies_q.iter_mut() {
        let current_pos = transform.translation.truncate();

        // Find the closest wrapped target position
        let mut min_dist_sq = f32::INFINITY;
        let mut best_target = player_pos;

        for offset in target_offsets.iter() {
            let candidate = player_pos + *offset;
            let dist_sq = current_pos.distance_squared(candidate);
            if dist_sq < min_dist_sq {
                min_dist_sq = dist_sq;
                best_target = candidate;
            }
        }

        let to_target = best_target - current_pos;
        if to_target.length_squared() < 1.0 {
            continue;
        }

        let direction = to_target.normalize();
        let mut pos = current_pos + direction * stats.speed * dt;

        // Ghost ignores obstacles, others slide around
        if *kind != EnemyKind::Ghost {
            for (obs_trans, obs_col) in obstacles_q.iter() {
                let obs_pos = obs_trans.translation.truncate();
                let min_dist = collider.radius + obs_col.radius;
                let diff = pos - obs_pos;
                let dist_sq = diff.length_squared();

                if dist_sq < min_dist * min_dist {
                    if dist_sq > 0.0001 {
                        let dist = dist_sq.sqrt();
                        let normal = diff / dist;
                        pos = obs_pos + normal * min_dist;
                    } else {
                        pos.x += min_dist;
                    }
                }
            }
        }

        pos.x = pos.x.clamp(30.0, MAP_SIZE - 30.0);
        pos.y = pos.y.clamp(30.0, MAP_SIZE - 30.0);

        transform.translation.x = pos.x;
        transform.translation.y = pos.y;
    }
}

pub fn enemy_shooting_system(
    mut commands: Commands,
    time: Res<Time>,
    enemy_assets: Res<EnemyAssets>,
    player_q: Query<&Transform, With<Player>>,
    mut enemies_q: Query<(&EnemyKind, &mut EnemyShooter, &Transform), With<Enemy>>,
) {
    let Ok(player_transform) = player_q.get_single() else {
        return;
    };
    let player_pos = player_transform.translation.truncate();

    for (kind, mut shooter, transform) in enemies_q.iter_mut() {
        shooter.timer.tick(time.delta());

        if shooter.timer.just_finished() {
            let enemy_pos = transform.translation.truncate();
            let shoot_dir = (player_pos - enemy_pos).normalize_or_zero();

            if shoot_dir != Vec2::ZERO {
                let (image, layout, frame_count, scale) = enemy_assets.get_bullet_render_info(*kind);

                commands.spawn((
                    Bullet {
                        damage: shooter.bullet_damage,
                        speed: shooter.bullet_speed,
                        direction: shoot_dir,
                        lifetime: Timer::from_seconds(2.5, TimerMode::Once),
                        faction: BulletFaction::Enemy,
                    },
                    Collider::new(16.0),
                    Sprite {
                        image,
                        texture_atlas: Some(TextureAtlas {
                            layout,
                            index: 0,
                        }),
                        ..default()
                    },
                    SpriteAnimation::new(frame_count, 10.0),
                    Transform::from_xyz(enemy_pos.x, enemy_pos.y, Z_BULLET)
                        .with_scale(Vec3::splat(scale)),
                ));
            }
        }
    }
}
