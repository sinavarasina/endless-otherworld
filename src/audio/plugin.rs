use bevy::prelude::*;
use crate::audio::bgm::{setup_bgm_system, update_bgm_volume_system};

pub struct GameAudioPlugin;

impl Plugin for GameAudioPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_bgm_system)
            .add_systems(Update, update_bgm_volume_system);
    }
}
