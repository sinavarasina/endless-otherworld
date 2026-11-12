use bevy::prelude::*;
use bevy::window::WindowResolution;
use std::path::Path;

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

fn find_asset_root() -> String {
    // 1. CARGO_MANIFEST_DIR (when running with cargo run)
    if let Ok(manifest_dir) = std::env::var("CARGO_MANIFEST_DIR") {
        let path = Path::new(&manifest_dir).join("assets");
        if path.is_dir() {
            return path.to_string_lossy().to_string();
        }
    }

    // 2. Current working directory
    let cwd_assets = Path::new("assets");
    if cwd_assets.is_dir() {
        return "assets".to_string();
    }

    // 3. Traverse parent directories from executable (target/release/ -> target/ -> root)
    if let Ok(mut exe) = std::env::current_exe() {
        exe.pop();
        for _ in 0..4 {
            let candidate = exe.join("assets");
            if candidate.is_dir() {
                return candidate.to_string_lossy().to_string();
            }
            exe.pop();
        }
    }

    "assets".to_string()
}

fn main() {
    let asset_root = find_asset_root();

    App::new()
        .add_plugins(
            DefaultPlugins
                .set(AssetPlugin {
                    file_path: asset_root,
                    ..default()
                })
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
