use bevy::prelude::*;
use std::time::{Duration, Instant};

use crate::fps::manager::{FpsLimit, FpsManager};

#[derive(Component)]
pub struct FpsOverlayText;

pub fn fps_counter_system(
    time: Res<Time>,
    mut manager: ResMut<FpsManager>,
) {
    manager.frame_counter += 1;
    manager.update_timer.tick(time.delta());

    if manager.update_timer.just_finished() {
        let elapsed = manager.update_timer.duration().as_secs_f32();
        if elapsed > 0.0 {
            manager.current_fps = (manager.frame_counter as f32) / elapsed;
        }
        manager.frame_counter = 0;
    }
}

pub fn fps_input_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut manager: ResMut<FpsManager>,
    mut windows: Query<&mut Window>,
) {
    let mut limit_changed = false;

    // F4: Cycle FPS presets (VSync -> 30 -> 60 -> 75 -> 120 -> 144 -> 180 -> 240 -> Uncapped)
    if keyboard.just_pressed(KeyCode::F4) {
        manager.limit = manager.limit.next();
        limit_changed = true;
    }

    // F3: Toggle FPS overlay on/off
    if keyboard.just_pressed(KeyCode::F3) {
        manager.visible = !manager.visible;
    }

    if limit_changed
        && let Ok(mut window) = windows.get_single_mut()
    {
        window.present_mode = manager.limit.target_present_mode();
    }
}

pub fn fps_pacer_system(
    manager: Res<FpsManager>,
    mut last_frame: Local<Option<Instant>>,
) {
    if let FpsLimit::Cap(target_fps) = manager.limit {
        let target_duration = Duration::from_secs_f64(1.0 / (target_fps as f64));

        if let Some(prev) = *last_frame {
            let elapsed = prev.elapsed();
            if elapsed < target_duration {
                let remaining = target_duration - elapsed;

                // Coarse sleep if more than 2ms remaining to save CPU cycles
                if remaining > Duration::from_millis(2) {
                    std::thread::sleep(remaining - Duration::from_millis(1));
                }

                // Fine spin-wait for sub-millisecond precision
                while prev.elapsed() < target_duration {
                    std::hint::spin_loop();
                }
            }
        }

        *last_frame = Some(Instant::now());
    } else {
        *last_frame = None;
    }
}

pub fn setup_fps_overlay(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
) {
    let font_handle: Handle<Font> = asset_server.load("font/bloodcrow.ttf");

    commands.spawn((
        FpsOverlayText,
        Text::new("FPS: -- | Limit: VSync"),
        TextFont {
            font: font_handle,
            font_size: 20.0,
            ..default()
        },
        TextColor(Color::srgb(0.0, 1.0, 0.5)),
        Node {
            position_type: PositionType::Absolute,
            right: Val::Px(16.0),
            top: Val::Px(16.0),
            ..default()
        },
    ));
}

pub fn update_fps_overlay(
    manager: Res<FpsManager>,
    mut query: Query<(&mut Text, &mut Visibility), With<FpsOverlayText>>,
) {
    let Ok((mut text, mut visibility)) = query.get_single_mut() else {
        return;
    };

    if !manager.visible {
        *visibility = Visibility::Hidden;
        return;
    }

    *visibility = Visibility::Visible;
    **text = format!(
        "FPS: {:.0} | Limit: {} [F4: Cycle, F3: Toggle]",
        manager.current_fps,
        manager.limit.display_name()
    );
}
