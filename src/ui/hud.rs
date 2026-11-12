use bevy::prelude::*;

use crate::core::cleanup::cleanup_entities;
use crate::player::components::{Player, PlayerExperience, PlayerScore, PlayerStats};
use crate::score::storage::ScoreManager;

#[derive(Component, Debug, Default)]
pub struct HudRoot;

#[derive(Component, Debug, Default)]
pub struct HpBarFill;

#[derive(Component, Debug, Default)]
pub struct HpText;

#[derive(Component, Debug, Default)]
pub struct TopScoreText;

#[derive(Component, Debug, Default)]
pub struct LevelExpText;

#[derive(Component, Debug, Default)]
pub struct LevelProgressBarFill;

#[derive(Component, Debug, Default)]
pub struct ScoreTimeText;

pub fn spawn_hud_system(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    score_manager: Option<Res<ScoreManager>>,
) {
    let font_handle: Handle<Font> = asset_server.load("font/bloodcrow.ttf");

    commands
        .spawn((
            HudRoot,
            Node {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                position_type: PositionType::Absolute,
                left: Val::Px(0.0),
                top: Val::Px(0.0),
                ..default()
            },
        ))
        .with_children(|root| {
            // Top-left container: HP bar, HP text, Top score
            root.spawn(Node {
                position_type: PositionType::Absolute,
                left: Val::Px(20.0),
                top: Val::Px(20.0),
                flex_direction: FlexDirection::Column,
                row_gap: Val::Px(8.0),
                ..default()
            })
            .with_children(|col| {
                // HP Bar Border
                col.spawn((
                    Node {
                        width: Val::Px(220.0),
                        height: Val::Px(24.0),
                        border: UiRect::all(Val::Px(2.0)),
                        padding: UiRect::all(Val::Px(1.0)),
                        ..default()
                    },
                    BorderColor(Color::WHITE),
                    BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.5)),
                ))
                .with_children(|bar| {
                    // HP Bar Fill
                    bar.spawn((
                        HpBarFill,
                        Node {
                            width: Val::Percent(100.0),
                            height: Val::Percent(100.0),
                            ..default()
                        },
                        BackgroundColor(Color::srgb(0.0, 1.0, 0.0)),
                    ));
                });

                // HP Text
                col.spawn((
                    HpText,
                    Text::new("HP: 100 / 100"),
                    TextFont {
                        font: font_handle.clone(),
                        font_size: 24.0,
                        ..default()
                    },
                    TextColor(Color::WHITE),
                ));

                // Top Score text
                let top_score = score_manager.as_ref().map(|sm| sm.get_top_score()).unwrap_or(0);
                col.spawn((
                    TopScoreText,
                    Text::new(format!("TOP SCORE: {}", top_score)),
                    TextFont {
                        font: font_handle.clone(),
                        font_size: 24.0,
                        ..default()
                    },
                    TextColor(Color::srgb(1.0, 0.85, 0.0)),
                ));
            });

            // Bottom-left info: Level, EXP
            root.spawn((
                LevelExpText,
                Text::new("Level: 1  EXP: 0 / 1000"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 24.0,
                    ..default()
                },
                TextColor(Color::WHITE),
                Node {
                    position_type: PositionType::Absolute,
                    left: Val::Px(20.0),
                    bottom: Val::Px(24.0),
                    ..default()
                },
            ));

            // Bottom-right info: Score, Time
            root.spawn((
                ScoreTimeText,
                Text::new("SCORE: 0   Time: 0s"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 28.0,
                    ..default()
                },
                TextColor(Color::WHITE),
                Node {
                    position_type: PositionType::Absolute,
                    right: Val::Px(20.0),
                    bottom: Val::Px(24.0),
                    ..default()
                },
            ));

            // Bottom full-width leveling bar container
            root.spawn((
                Node {
                    position_type: PositionType::Absolute,
                    left: Val::Px(0.0),
                    bottom: Val::Px(0.0),
                    width: Val::Percent(100.0),
                    height: Val::Px(8.0),
                    ..default()
                },
                BackgroundColor(Color::srgb(0.15, 0.15, 0.15)),
            ))
            .with_children(|bar| {
                bar.spawn((
                    LevelProgressBarFill,
                    Node {
                        width: Val::Percent(0.0),
                        height: Val::Percent(100.0),
                        ..default()
                    },
                    BackgroundColor(Color::srgb(0.0, 1.0, 0.0)),
                ));
            });
        });
}

#[allow(clippy::type_complexity)]
pub fn update_hud_system(
    player_q: Query<(&PlayerStats, &PlayerExperience, &PlayerScore), With<Player>>,
    mut hp_bar_q: Query<(&mut Node, &mut BackgroundColor), (With<HpBarFill>, Without<LevelProgressBarFill>)>,
    mut hp_text_q: Query<&mut Text, (With<HpText>, Without<LevelExpText>, Without<ScoreTimeText>)>,
    mut level_exp_text_q: Query<&mut Text, (With<LevelExpText>, Without<HpText>, Without<ScoreTimeText>)>,
    mut level_bar_q: Query<&mut Node, (With<LevelProgressBarFill>, Without<HpBarFill>)>,
    mut score_time_text_q: Query<&mut Text, (With<ScoreTimeText>, Without<HpText>, Without<LevelExpText>)>,
) {
    let Ok((stats, exp, score)) = player_q.get_single() else {
        return;
    };

    // Update HP Bar and Text
    let hp_pct = (stats.hp / stats.max_hp.max(1.0)).clamp(0.0, 1.0);
    if let Ok((mut bar_node, mut bar_color)) = hp_bar_q.get_single_mut() {
        bar_node.width = Val::Percent(hp_pct * 100.0);
        let color = if hp_pct > 0.75 {
            Color::srgb(0.0, 1.0, 0.0)
        } else if hp_pct > 0.25 {
            Color::srgb(0.2, 0.4, 1.0)
        } else {
            Color::srgb(1.0, 0.15, 0.15)
        };
        *bar_color = BackgroundColor(color);
    }

    if let Ok(mut text) = hp_text_q.get_single_mut() {
        **text = format!("HP: {:.0} / {:.0}", stats.hp.max(0.0), stats.max_hp);
    }

    // Update Level & EXP text
    if let Ok(mut text) = level_exp_text_q.get_single_mut() {
        **text = format!("Level: {}   EXP: {} / {}", exp.level, exp.exp, exp.xp_target);
    }

    // Update Leveling Progress Bar along bottom
    let exp_pct = ((exp.exp as f32) / (exp.xp_target as f32).max(1.0)).clamp(0.0, 1.0);
    if let Ok(mut bar_node) = level_bar_q.get_single_mut() {
        bar_node.width = Val::Percent(exp_pct * 100.0);
    }

    // Update Score & Time text
    if let Ok(mut text) = score_time_text_q.get_single_mut() {
        **text = format!("SCORE: {}   Time: {}s", score.score, score.survival_seconds);
    }
}

pub fn despawn_hud_system(
    commands: Commands,
    query: Query<Entity, With<HudRoot>>,
) {
    cleanup_entities::<HudRoot>(commands, query);
}
