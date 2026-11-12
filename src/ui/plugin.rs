use bevy::prelude::*;
use crate::core::state::GameState;
use crate::ui::game_over::{despawn_game_over_system, game_over_input_system, spawn_game_over_system};
use crate::ui::hud::{despawn_hud_system, spawn_hud_system, update_hud_system};
use crate::ui::main_menu::{despawn_main_menu_system, main_menu_input_system, pause_on_escape_system, spawn_main_menu_system};

pub fn update_ui_scale_system(
    windows: Query<&Window, Changed<Window>>,
    mut ui_scale: ResMut<UiScale>,
) {
    if let Ok(window) = windows.get_single() {
        let scale = (window.height() / 1080.0).clamp(0.5, 3.0);
        ui_scale.0 = scale;
    }
}

pub struct UiPlugin;

impl Plugin for UiPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, update_ui_scale_system)
            // Main Menu
            .add_systems(OnEnter(GameState::MainMenu), spawn_main_menu_system)
            .add_systems(
                Update,
                main_menu_input_system.run_if(in_state(GameState::MainMenu)),
            )
            .add_systems(OnExit(GameState::MainMenu), despawn_main_menu_system)
            // Pause on Esc
            .add_systems(
                Update,
                pause_on_escape_system.run_if(in_state(GameState::Playing)),
            )
            // In-Game HUD
            .add_systems(OnEnter(GameState::Playing), spawn_hud_system)
            .add_systems(
                Update,
                update_hud_system.run_if(in_state(GameState::Playing)),
            )
            .add_systems(OnExit(GameState::Playing), despawn_hud_system.run_if(not(in_state(GameState::GachaMenu))))
            // Game Over Menu
            .add_systems(OnEnter(GameState::GameOver), spawn_game_over_system)
            .add_systems(
                Update,
                game_over_input_system.run_if(in_state(GameState::GameOver)),
            )
            .add_systems(OnExit(GameState::GameOver), despawn_game_over_system);
    }
}
