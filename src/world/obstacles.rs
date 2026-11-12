use bevy::prelude::*;
use std::fs::File;
use std::io::BufReader;

use crate::combat::components::Collider;
use crate::core::constants::*;
use crate::world::components::{Obstacle, ObstacleEntry};

pub fn spawn_obstacles_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    let config_path = "assets/config/obstacle.json";
    let file = match File::open(config_path) {
        Ok(f) => f,
        Err(err) => {
            warn!("Could not open obstacle config at {}: {}", config_path, err);
            return;
        }
    };

    let reader = BufReader::new(file);
    let entries: Vec<ObstacleEntry> = match serde_json::from_reader(reader) {
        Ok(data) => data,
        Err(err) => {
            warn!("Failed to parse obstacle config: {}", err);
            return;
        }
    };

    info!("Spawning {} obstacles from config", entries.len());

    for entry in entries {
        let x = entry.position[0];
        let y = MAP_SIZE - entry.position[1]; // Convert Pygame Y (top-down) to Bevy Y (bottom-up)

        let is_tree = entry.image.contains("Tree");
        let radius = if is_tree { 42.0 } else { 32.0 };

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
