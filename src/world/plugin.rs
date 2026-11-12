use bevy::prelude::*;
use crate::world::map::{camera_follow_player_system, setup_camera_and_map};
use crate::world::obstacles::spawn_obstacles_system;

pub struct WorldPlugin;

impl Plugin for WorldPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, (setup_camera_and_map, spawn_obstacles_system))
            .add_systems(PostUpdate, camera_follow_player_system);
    }
}
