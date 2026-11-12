use bevy::prelude::*;
use crate::animation::components::SpriteAnimation;
use crate::combat::components::{Bullet, BulletFaction, Collider};
use crate::core::constants::*;
use crate::player::assets::PlayerAssets;
use crate::player::components::*;
use crate::world::components::{MainCamera, Obstacle};

pub fn spawn_player(
    mut commands: Commands,
    player_assets: Res<PlayerAssets>,
    existing_player: Query<Entity, With<Player>>,
) {
    // If player already exists, don't spawn duplicate
    if !existing_player.is_empty() {
        return;
    }

    commands.spawn((
        Player,
        PlayerStats::default(),
        PlayerExperience::default(),
        PlayerFacing::IdleDown,
        PlayerScore::default(),
        Collider::new(30.0),
        Sprite {
            image: player_assets.idle_down.clone(),
            texture_atlas: Some(TextureAtlas {
                layout: player_assets.layout.clone(),
                index: 0,
            }),
            ..default()
        },
        SpriteAnimation::new(6, 10.0),
        Transform::from_xyz(HALF_MAP_SIZE, HALF_MAP_SIZE, Z_PLAYER).with_scale(Vec3::splat(3.0)),
    ));
}

#[allow(clippy::type_complexity)]
pub fn player_movement(
    time: Res<Time>,
    keyboard: Res<ButtonInput<KeyCode>>,
    mut player_q: Query<(&PlayerStats, &mut Transform, &Collider), With<Player>>,
    obstacles_q: Query<(&Transform, &Collider), (With<Obstacle>, Without<Player>)>,
) {
    let Ok((stats, mut transform, player_collider)) = player_q.get_single_mut() else {
        return;
    };

    let mut dir = Vec2::ZERO;
    if keyboard.pressed(KeyCode::KeyW) || keyboard.pressed(KeyCode::ArrowUp) {
        dir.y += 1.0;
    }
    if keyboard.pressed(KeyCode::KeyS) || keyboard.pressed(KeyCode::ArrowDown) {
        dir.y -= 1.0;
    }
    if keyboard.pressed(KeyCode::KeyA) || keyboard.pressed(KeyCode::ArrowLeft) {
        dir.x -= 1.0;
    }
    if keyboard.pressed(KeyCode::KeyD) || keyboard.pressed(KeyCode::ArrowRight) {
        dir.x += 1.0;
    }

    if dir != Vec2::ZERO {
        let normalized = dir.normalize();
        let move_delta = normalized * stats.speed * time.delta_secs();

        let current_pos = transform.translation.truncate();
        let target_pos_x = Vec2::new(current_pos.x + move_delta.x, current_pos.y);
        let target_pos_y = Vec2::new(current_pos.x, current_pos.y + move_delta.y);

        // Slide along X if no obstacle collision
        let mut final_pos = current_pos;
        let collides_x = obstacles_q.iter().any(|(obs_transform, obs_collider)| {
            player_collider.intersects(target_pos_x, obs_collider, obs_transform.translation.truncate())
        });
        if !collides_x {
            final_pos.x = target_pos_x.x;
        }

        // Slide along Y if no obstacle collision
        let collides_y = obstacles_q.iter().any(|(obs_transform, obs_collider)| {
            player_collider.intersects(
                Vec2::new(final_pos.x, target_pos_y.y),
                obs_collider,
                obs_transform.translation.truncate(),
            )
        });
        if !collides_y {
            final_pos.y = target_pos_y.y;
        }

        // Clamp to map boundaries
        final_pos.x = final_pos.x.clamp(50.0, MAP_SIZE - 50.0);
        final_pos.y = final_pos.y.clamp(50.0, MAP_SIZE - 50.0);

        transform.translation.x = final_pos.x;
        transform.translation.y = final_pos.y;
    }
}

pub fn player_facing_animation(
    keyboard: Res<ButtonInput<KeyCode>>,
    player_assets: Res<PlayerAssets>,
    mut query: Query<(&mut PlayerFacing, &mut Sprite), With<Player>>,
) {
    let Ok((mut facing, mut sprite)) = query.get_single_mut() else {
        return;
    };

    let w = keyboard.pressed(KeyCode::KeyW) || keyboard.pressed(KeyCode::ArrowUp);
    let s = keyboard.pressed(KeyCode::KeyS) || keyboard.pressed(KeyCode::ArrowDown);
    let a = keyboard.pressed(KeyCode::KeyA) || keyboard.pressed(KeyCode::ArrowLeft);
    let d = keyboard.pressed(KeyCode::KeyD) || keyboard.pressed(KeyCode::ArrowRight);

    let new_facing = match (w, s, a, d) {
        (true, false, true, false) => PlayerFacing::WalkLeftUp,
        (true, false, false, true) => PlayerFacing::WalkRightUp,
        (false, true, true, false) => PlayerFacing::WalkLeftDown,
        (false, true, false, true) => PlayerFacing::WalkRightDown,
        (true, false, false, false) => PlayerFacing::WalkUp,
        (false, true, false, false) => PlayerFacing::WalkDown,
        (false, false, true, false) => PlayerFacing::WalkLeftDown,
        (false, false, false, true) => PlayerFacing::WalkRightDown,
        _ => PlayerFacing::IdleDown,
    };

    if *facing != new_facing {
        *facing = new_facing;
        sprite.image = player_assets.get_image_for_facing(new_facing);
    }
}

pub fn player_shooting(
    mut commands: Commands,
    time: Res<Time>,
    mouse_buttons: Res<ButtonInput<MouseButton>>,
    windows: Query<&Window>,
    camera_q: Query<(&Camera, &GlobalTransform), With<MainCamera>>,
    player_assets: Res<PlayerAssets>,
    mut player_q: Query<(&mut PlayerStats, &Transform), With<Player>>,
) {
    let Ok((mut stats, transform)) = player_q.get_single_mut() else {
        return;
    };

    stats.shoot_cooldown.tick(time.delta());

    if mouse_buttons.pressed(MouseButton::Left) && stats.shoot_cooldown.finished() {
        let Ok(window) = windows.get_single() else { return; };
        let Some(cursor_pos) = window.cursor_position() else { return; };
        let Ok((camera, camera_transform)) = camera_q.get_single() else { return; };
        let Ok(world_pos) = camera.viewport_to_world_2d(camera_transform, cursor_pos) else { return; };

        let player_pos = transform.translation.truncate();
        let shoot_dir = (world_pos - player_pos).normalize_or_zero();

        if shoot_dir != Vec2::ZERO {
            stats.shoot_cooldown.reset();

            commands.spawn((
                Bullet {
                    damage: stats.attack,
                    speed: stats.bullet_speed,
                    direction: shoot_dir,
                    lifetime: Timer::from_seconds(1.2, TimerMode::Once),
                    faction: BulletFaction::Player,
                },
                Collider::new(16.0),
                Sprite {
                    image: player_assets.bullet_texture.clone(),
                    texture_atlas: Some(TextureAtlas {
                        layout: player_assets.bullet_layout.clone(),
                        index: 0,
                    }),
                    ..default()
                },
                SpriteAnimation::new(4, stats.bullet_anim_speed),
                Transform::from_xyz(player_pos.x, player_pos.y, Z_BULLET)
                    .with_scale(Vec3::splat(2.0)),
            ));
        }
    }
}

pub fn player_survival_timer(
    time: Res<Time>,
    mut query: Query<&mut PlayerScore, With<Player>>,
) {
    for mut score in query.iter_mut() {
        score.timer.tick(time.delta());
        if score.timer.just_finished() {
            score.survival_seconds += 1;
            score.score += 1;
        }
    }
}
