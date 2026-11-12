use bevy::prelude::*;
use crate::fps::manager::FpsManager;
use crate::fps::systems::*;

pub struct FpsPlugin;

impl Plugin for FpsPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<FpsManager>()
            .add_systems(Startup, setup_fps_overlay)
            .add_systems(
                Update,
                (
                    fps_counter_system,
                    fps_input_system,
                    update_fps_overlay,
                ),
            )
            .add_systems(Last, fps_pacer_system);
    }
}
