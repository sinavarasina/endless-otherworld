use bevy::prelude::*;

use crate::core::cleanup::cleanup_entities;
use crate::core::constants::{HALF_MAP_SIZE, Z_PLAYER};
use crate::core::state::GameState;
use crate::player::components::{Player, PlayerExperience, PlayerScore, PlayerStats};
use crate::score::storage::ScoreManager;

#[derive(Component, Debug, Default)]
pub struct MainMenuRoot;

pub fn spawn_main_menu_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    score_manager: Option<Res<ScoreManager>>,
) {
    let font_handle: Handle<Font> = asset_server.load("font/bloodcrow.ttf");
    let top_score = score_manager.as_ref().map(|sm| sm.get_top_score()).unwrap_or(0);

    commands
        .spawn((
            MainMenuRoot,
            Node {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                flex_direction: FlexDirection::Column,
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                row_gap: Val::Px(28.0),
                ..default()
            },
            BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.65)),
        ))
        .with_children(|parent| {
            // Title
            parent.spawn((
                Text::new("Endless Otherworld"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 84.0,
                    ..default()
                },
                TextColor(Color::WHITE),
            ));

            // Top score
            parent.spawn((
                Text::new(format!("TOP SCORE: {}", top_score)),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 32.0,
                    ..default()
                },
                TextColor(Color::srgb(1.0, 0.85, 0.0)),
            ));

            // Subtitle - Enter to Start
            parent.spawn((
                Text::new("Press Enter to Start"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 38.0,
                    ..default()
                },
                TextColor(Color::srgb(0.9, 0.9, 0.9)),
            ));

            // Subtitle - Esc to Quit
            parent.spawn((
                Text::new("Esc to Quit"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 30.0,
                    ..default()
                },
                TextColor(Color::srgb(0.7, 0.7, 0.7)),
            ));
        });
}

pub fn main_menu_input_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut next_state: ResMut<NextState<GameState>>,
    mut exit_events: EventWriter<AppExit>,
    mut player_q: Query<(&mut Transform, &mut PlayerStats, &mut PlayerExperience, &mut PlayerScore), With<Player>>,
) {
    if keyboard.just_pressed(KeyCode::Enter) || keyboard.just_pressed(KeyCode::NumpadEnter) || keyboard.just_pressed(KeyCode::Space) {
        // Reset player for new game run
        if let Ok((mut transform, mut stats, mut exp, mut score)) = player_q.get_single_mut() {
            transform.translation.x = HALF_MAP_SIZE;
            transform.translation.y = HALF_MAP_SIZE;
            transform.translation.z = Z_PLAYER;

            *stats = PlayerStats::default();
            *exp = PlayerExperience::default();
            *score = PlayerScore::default();
        }

        next_state.set(GameState::Playing);
    } else if keyboard.just_pressed(KeyCode::Escape) {
        exit_events.send(AppExit::Success);
    }
}

pub fn pause_on_escape_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if keyboard.just_pressed(KeyCode::Escape) {
        next_state.set(GameState::MainMenu);
    }
}

pub fn despawn_main_menu_system(
    commands: Commands,
    query: Query<Entity, With<MainMenuRoot>>,
) {
    cleanup_entities::<MainMenuRoot>(commands, query);
}
