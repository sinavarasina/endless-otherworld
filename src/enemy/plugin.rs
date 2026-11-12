use bevy::prelude::*;
use crate::core::cleanup::cleanup_entities;
use crate::core::state::GameState;
use crate::enemy::ai::{enemy_movement_system, enemy_shooting_system};
use crate::enemy::assets::load_enemy_assets;
use crate::enemy::components::Enemy;
use crate::enemy::spawner::{spawn_enemies_system, EnemySpawner};

pub struct EnemyPlugin;

impl Plugin for EnemyPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<EnemySpawner>()
            .add_systems(Startup, load_enemy_assets)
            .add_systems(OnEnter(GameState::MainMenu), cleanup_entities::<Enemy>)
            .add_systems(
                Update,
                (
                    spawn_enemies_system,
                    enemy_movement_system,
                    enemy_shooting_system,
                )
                    .run_if(in_state(GameState::Playing)),
            );
    }
}
