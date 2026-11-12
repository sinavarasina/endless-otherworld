use bevy::audio::Volume;
use bevy::prelude::*;
use crate::core::state::GameState;

#[derive(Component, Debug, Default)]
pub struct BgmSource;

pub fn setup_bgm_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    commands.spawn((
        AudioPlayer::new(asset_server.load("sound/bgm/freelike-touhou125-music.ogg")),
        PlaybackSettings::LOOP.with_volume(Volume::new(0.2)),
        BgmSource,
    ));
}

pub fn update_bgm_volume_system(
    current_state: Res<State<GameState>>,
    audio_sink_q: Query<&AudioSink, With<BgmSource>>,
) {
    let Ok(sink) = audio_sink_q.get_single() else {
        return;
    };

    let target_volume = match current_state.get() {
        GameState::Playing => 0.8,
        _ => 0.2,
    };

    sink.set_volume(target_volume);
}
