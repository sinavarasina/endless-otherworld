use bevy::prelude::*;

use crate::core::constants::*;
use crate::player::components::Player;
use crate::world::components::{MainCamera, MapBackground};

pub fn setup_camera_and_map(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    commands.spawn((
        Camera2d,
        Transform::from_xyz(HALF_MAP_SIZE, HALF_MAP_SIZE, 1000.0),
        MainCamera,
    ));

    // Map background (stretched across 10000x10000 world)
    commands.spawn((
        MapBackground,
        Sprite {
            image: asset_server.load("images/Map/Ground/map_pbo_fix.png"),
            custom_size: Some(Vec2::new(MAP_SIZE, MAP_SIZE)),
            ..default()
        },
        Transform::from_xyz(HALF_MAP_SIZE, HALF_MAP_SIZE, Z_BACKGROUND),
    ));
}

pub fn camera_follow_player_system(
    player_q: Query<&Transform, (With<Player>, Without<MainCamera>)>,
    mut camera_q: Query<&mut Transform, With<MainCamera>>,
    windows: Query<&Window>,
) {
    let Ok(player_transform) = player_q.get_single() else {
        return;
    };
    let Ok(mut camera_transform) = camera_q.get_single_mut() else {
        return;
    };

    let (half_w, half_h) = if let Ok(window) = windows.get_single() {
        (window.width() / 2.0, window.height() / 2.0)
    } else {
        (WINDOW_WIDTH / 2.0, WINDOW_HEIGHT / 2.0)
    };

    let min_x = half_w;
    let max_x = (MAP_SIZE - half_w).max(half_w);
    let min_y = half_h;
    let max_y = (MAP_SIZE - half_h).max(half_h);

    camera_transform.translation.x = player_transform.translation.x.clamp(min_x, max_x);
    camera_transform.translation.y = player_transform.translation.y.clamp(min_y, max_y);
}
