use bevy::prelude::*;

use crate::combat::components::{Bullet, BulletFaction, Collider, DamageEvent, GameOverEvent, LevelUpEvent};
use crate::core::constants::MAP_SIZE;
use crate::core::state::GameState;
use crate::enemy::components::{Enemy, EnemyStats};
use crate::player::components::{Player, PlayerExperience, PlayerScore, PlayerStats};

pub fn bullet_movement_system(
    mut commands: Commands,
    time: Res<Time>,
    mut bullets_q: Query<(Entity, &mut Bullet, &mut Transform)>,
) {
    for (entity, mut bullet, mut transform) in bullets_q.iter_mut() {
        bullet.lifetime.tick(time.delta());

        if bullet.lifetime.just_finished() {
            commands.entity(entity).despawn();
            continue;
        }

        let delta = bullet.direction * bullet.speed * time.delta_secs();
        transform.translation.x += delta.x;
        transform.translation.y += delta.y;

        // Despawn if escaped outside map
        let pos = transform.translation.truncate();
        if pos.x < 0.0 || pos.x > MAP_SIZE || pos.y < 0.0 || pos.y > MAP_SIZE {
            commands.entity(entity).despawn();
        }
    }
}

pub fn bullet_collision_system(
    mut commands: Commands,
    mut damage_events: EventWriter<DamageEvent>,
    bullets_q: Query<(Entity, &Bullet, &Collider, &Transform)>,
    enemies_q: Query<(Entity, &Collider, &Transform), With<Enemy>>,
    player_q: Query<(Entity, &Collider, &Transform), With<Player>>,
) {
    for (bullet_entity, bullet, bullet_collider, bullet_transform) in bullets_q.iter() {
        let bullet_pos = bullet_transform.translation.truncate();

        match bullet.faction {
            BulletFaction::Player => {
                for (enemy_entity, enemy_collider, enemy_transform) in enemies_q.iter() {
                    let enemy_pos = enemy_transform.translation.truncate();
                    if bullet_collider.intersects(bullet_pos, enemy_collider, enemy_pos) {
                        damage_events.send(DamageEvent {
                            target: enemy_entity,
                            amount: bullet.damage,
                        });
                        commands.entity(bullet_entity).despawn();
                        break;
                    }
                }
            }
            BulletFaction::Enemy => {
                if let Ok((player_entity, player_collider, player_transform)) = player_q.get_single() {
                    let player_pos = player_transform.translation.truncate();
                    if bullet_collider.intersects(bullet_pos, player_collider, player_pos) {
                        damage_events.send(DamageEvent {
                            target: player_entity,
                            amount: bullet.damage,
                        });
                        commands.entity(bullet_entity).despawn();
                    }
                }
            }
        }
    }
}

pub fn damage_application_system(
    mut damage_events: EventReader<DamageEvent>,
    mut enemies_q: Query<&mut EnemyStats, With<Enemy>>,
    mut player_q: Query<&mut PlayerStats, With<Player>>,
) {
    for event in damage_events.read() {
        if let Ok(mut enemy_stats) = enemies_q.get_mut(event.target) {
            enemy_stats.hp -= event.amount;
        } else if let Ok(mut player_stats) = player_q.get_mut(event.target) {
            player_stats.hp -= event.amount;
        }
    }
}

pub fn combat_resolution_system(
    mut commands: Commands,
    mut next_state: ResMut<NextState<GameState>>,
    mut level_up_events: EventWriter<LevelUpEvent>,
    mut game_over_events: EventWriter<GameOverEvent>,
    enemies_q: Query<(Entity, &EnemyStats), With<Enemy>>,
    mut player_q: Query<(&PlayerStats, &mut PlayerExperience, &mut PlayerScore), With<Player>>,
) {
    let Ok((player_stats, mut player_exp, mut player_score)) = player_q.get_single_mut() else {
        return;
    };

    // Check player death
    if player_stats.hp <= 0.0 {
        game_over_events.send(GameOverEvent {
            level: player_exp.level,
            final_score: player_score.score,
            survival_seconds: player_score.survival_seconds,
        });
        next_state.set(GameState::GameOver);
        return;
    }

    // Process enemy deaths
    let mut total_exp_gained = 0;
    for (enemy_entity, stats) in enemies_q.iter() {
        if stats.hp <= 0.0 {
            total_exp_gained += stats.killed_exp;
            player_score.score += stats.killed_exp;
            commands.entity(enemy_entity).despawn();
        }
    }

    if total_exp_gained > 0 {
        let levels_gained = player_exp.add_exp(total_exp_gained);
        if levels_gained > 0 {
            level_up_events.send(LevelUpEvent {
                new_level: player_exp.level,
            });
            next_state.set(GameState::GachaMenu);
        }
    }
}
