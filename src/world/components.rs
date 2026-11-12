use bevy::prelude::*;
use serde::Deserialize;

#[derive(Component, Debug, Default)]
pub struct Obstacle;

#[derive(Component, Debug, Default)]
pub struct MainCamera;

#[derive(Component, Debug, Default)]
pub struct MapBackground;

#[derive(Deserialize, Debug, Clone)]
pub struct ObstacleEntry {
    pub image: String,
    pub position: [f32; 2],
}
