use bevy::prelude::*;
use crate::combat::components::{DamageEvent, GameOverEvent, LevelUpEvent};
use crate::combat::systems::*;
use crate::core::state::GameState;

pub struct CombatPlugin;

impl Plugin for CombatPlugin {
    fn build(&self, app: &mut App) {
        app.add_event::<DamageEvent>()
            .add_event::<LevelUpEvent>()
            .add_event::<GameOverEvent>()
            .add_systems(
                Update,
                (
                    bullet_movement_system,
                    bullet_collision_system,
                    damage_application_system,
                    combat_resolution_system,
                )
                    .chain()
                    .run_if(in_state(GameState::Playing)),
            );
    }
}
