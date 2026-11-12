use bevy::prelude::*;
use bevy::window::WindowResolution;

pub mod animation;
pub mod audio;
pub mod combat;
pub mod core;
pub mod enemy;
pub mod gacha;
pub mod player;
pub mod score;
pub mod ui;
pub mod world;

use animation::AnimationPlugin;
use audio::GameAudioPlugin;
use combat::CombatPlugin;
use core::constants::{WINDOW_HEIGHT, WINDOW_WIDTH};
use core::state::GameState;
use enemy::EnemyPlugin;
use gacha::GachaPlugin;
use player::PlayerPlugin;
use score::ScorePlugin;
use ui::UiPlugin;
use world::WorldPlugin;

fn main() {
    App::new()
        .add_plugins(
            DefaultPlugins
                .set(WindowPlugin {
                    primary_window: Some(Window {
                        title: "Endless Otherworld".to_string(),
                        resolution: WindowResolution::new(WINDOW_WIDTH, WINDOW_HEIGHT),
                        resizable: true,
                        ..default()
                    }),
                    ..default()
                })
                .set(ImagePlugin::default_nearest()), // Crisp pixel art rendering
        )
        .init_state::<GameState>()
        .add_plugins((
            AnimationPlugin,
            WorldPlugin,
            PlayerPlugin,
            EnemyPlugin,
            CombatPlugin,
            GachaPlugin,
            ScorePlugin,
            GameAudioPlugin,
            UiPlugin,
        ))
        .run();
}
