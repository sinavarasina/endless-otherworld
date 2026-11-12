use bevy::prelude::*;

use crate::combat::components::Collider;
use crate::core::constants::*;
use crate::world::components::{Obstacle, ObstacleEntry};

pub fn spawn_obstacles_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    const CONFIG_JSON: &str = include_str!("../../assets/config/obstacle.json");

    let entries: Vec<ObstacleEntry> = match serde_json::from_str(CONFIG_JSON) {
        Ok(data) => data,
        Err(err) => {
            warn!("Failed to parse embedded obstacle config: {}", err);
            return;
        }
    };

    for entry in entries {
        let x = entry.position[0];
        let y = MAP_SIZE - entry.position[1]; // Convert Pygame top-down Y to Bevy bottom-up Y

        let is_tree = entry.image.contains("Tree");
        let radius = if is_tree { 40.0 } else { 30.0 };
        let asset_path = format!("images/{}", entry.image);

        commands.spawn((
            Obstacle,
            Collider::new(radius),
            Sprite {
                image: asset_server.load(asset_path),
                ..default()
            },
            Transform::from_xyz(x, y, Z_OBSTACLE),
        ));
    }
}
