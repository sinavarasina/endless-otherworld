use bevy::prelude::*;
use crate::core::state::GameState;
use crate::player::assets::load_player_assets;
use crate::player::systems::*;

pub struct PlayerPlugin;

impl Plugin for PlayerPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, load_player_assets)
            .add_systems(OnEnter(GameState::Playing), spawn_player)
            .add_systems(
                Update,
                (
                    player_movement,
                    player_facing_animation,
                    player_shooting,
                    player_survival_timer,
                )
                    .run_if(in_state(GameState::Playing)),
            );
    }
}
