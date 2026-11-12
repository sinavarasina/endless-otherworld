use bevy::prelude::*;

use crate::core::cleanup::cleanup_entities;
use crate::core::state::GameState;
use crate::player::components::{Player, PlayerExperience, PlayerScore};
use crate::score::storage::ScoreManager;

#[derive(Component, Debug, Default)]
pub struct GameOverRoot;

pub fn spawn_game_over_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    player_q: Query<(&PlayerExperience, &PlayerScore), With<Player>>,
    score_manager: Option<Res<ScoreManager>>,
) {
    let font_handle: Handle<Font> = asset_server.load("font/bloodcrow.ttf");

    let (level, score, seconds) = if let Ok((exp, player_score)) = player_q.get_single() {
        (exp.level, player_score.score, player_score.survival_seconds)
    } else {
        (1, 0, 0)
    };

    let top_score = score_manager.as_ref().map(|sm| sm.get_top_score()).unwrap_or(0);
    let minutes = seconds / 60;
    let sec_rem = seconds % 60;

    commands
        .spawn((
            GameOverRoot,
            Node {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                flex_direction: FlexDirection::Column,
                justify_content: JustifyContent::Center,
                align_items: AlignItems::Center,
                row_gap: Val::Px(24.0),
                ..default()
            },
            BackgroundColor(Color::srgba(0.2, 0.0, 0.0, 0.85)),
        ))
        .with_children(|parent| {
            // Game Over Title
            parent.spawn((
                Text::new("GAME OVER"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 96.0,
                    ..default()
                },
                TextColor(Color::srgb(0.9, 0.1, 0.1)),
            ));

            // Run stats summary
            parent.spawn((
                Text::new(format!(
                    "Level: {}    Score: {}    Survived: {}:{:02}",
                    level, score, minutes, sec_rem
                )),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 36.0,
                    ..default()
                },
                TextColor(Color::WHITE),
            ));

            // Top score comparison
            parent.spawn((
                Text::new(format!("Top Score: {}", top_score)),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 30.0,
                    ..default()
                },
                TextColor(Color::srgb(1.0, 0.85, 0.0)),
            ));

            // Subtitle
            parent.spawn((
                Text::new("Press Enter or Space to return to Main Menu"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 32.0,
                    ..default()
                },
                TextColor(Color::srgb(0.8, 0.8, 0.8)),
            ));
        });
}

pub fn game_over_input_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if keyboard.just_pressed(KeyCode::Enter)
        || keyboard.just_pressed(KeyCode::NumpadEnter)
        || keyboard.just_pressed(KeyCode::Space)
    {
        next_state.set(GameState::MainMenu);
    }
}

pub fn despawn_game_over_system(
    commands: Commands,
    query: Query<Entity, With<GameOverRoot>>,
) {
    cleanup_entities::<GameOverRoot>(commands, query);
}
