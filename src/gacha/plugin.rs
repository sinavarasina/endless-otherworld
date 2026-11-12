use bevy::prelude::*;
use crate::core::state::GameState;
use crate::gacha::loader::GachaDeck;
use crate::gacha::ui::{despawn_gacha_menu, gacha_input_system, spawn_gacha_menu};

pub struct GachaPlugin;

impl Plugin for GachaPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(GachaDeck::load_embedded())
            .add_systems(OnEnter(GameState::GachaMenu), spawn_gacha_menu)
            .add_systems(Update, gacha_input_system.run_if(in_state(GameState::GachaMenu)))
            .add_systems(OnExit(GameState::GachaMenu), despawn_gacha_menu);
    }
}
