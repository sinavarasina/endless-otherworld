use bevy::prelude::*;
use crate::animation::systems::update_sprite_animation;

pub struct AnimationPlugin;

impl Plugin for AnimationPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, update_sprite_animation);
    }
}
