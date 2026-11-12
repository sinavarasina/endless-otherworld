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
    existing_hud_q: Query<Entity, With<HudRoot>>,
) {
    if !existing_hud_q.is_empty() {
        return;
    }

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

            // Dedicated Bottom HUD Bar: Flex row above progress bar (Never overlaps!)
            root.spawn(Node {
                position_type: PositionType::Absolute,
                left: Val::Px(0.0),
                bottom: Val::Px(0.0),
                width: Val::Percent(100.0),
                flex_direction: FlexDirection::Column,
                ..default()
            })
            .with_children(|bottom_bar| {
                // Text Row (Level/EXP on left, Score/Time on right)
                bottom_bar
                    .spawn((
                        Node {
                            width: Val::Percent(100.0),
                            flex_direction: FlexDirection::Row,
                            justify_content: JustifyContent::SpaceBetween,
                            align_items: AlignItems::Center,
                            padding: UiRect::axes(Val::Px(24.0), Val::Px(8.0)),
                            ..default()
                        },
                        BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.65)),
                    ))
                    .with_children(|row| {
                        row.spawn((
                            LevelExpText,
                            Text::new("Level: 1  |  EXP: 0 / 1000"),
                            TextFont {
                                font: font_handle.clone(),
                                font_size: 22.0,
                                ..default()
                            },
                            TextColor(Color::WHITE),
                        ));

                        row.spawn((
                            ScoreTimeText,
                            Text::new("SCORE: 0  |  Time: 0s"),
                            TextFont {
                                font: font_handle.clone(),
                                font_size: 22.0,
                                ..default()
                            },
                            TextColor(Color::WHITE),
                        ));
                    });

                // EXP Progress Bar (at the very bottom)
                bottom_bar
                    .spawn((
                        Node {
                            width: Val::Percent(100.0),
                            height: Val::Px(8.0),
                            ..default()
                        },
                        BackgroundColor(Color::srgb(0.12, 0.12, 0.12)),
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
    for (mut bar_node, mut bar_color) in hp_bar_q.iter_mut() {
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

    for mut text in hp_text_q.iter_mut() {
        **text = format!("HP: {:.0} / {:.0}", stats.hp.max(0.0), stats.max_hp);
    }

    // Update Level & EXP text
    for mut text in level_exp_text_q.iter_mut() {
        **text = format!("Level: {}  |  EXP: {} / {}", exp.level, exp.exp, exp.xp_target);
    }

    // Update Leveling Progress Bar along bottom
    let exp_pct = ((exp.exp as f32) / (exp.xp_target as f32).max(1.0)).clamp(0.0, 1.0);
    for mut bar_node in level_bar_q.iter_mut() {
        bar_node.width = Val::Percent(exp_pct * 100.0);
    }

    // Update Score & Time text
    for mut text in score_time_text_q.iter_mut() {
        **text = format!("SCORE: {}  |  Time: {}s", score.score, score.survival_seconds);
    }
}

pub fn despawn_hud_system(
    commands: Commands,
    query: Query<Entity, With<HudRoot>>,
) {
    cleanup_entities::<HudRoot>(commands, query);
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::state::GameState;
    use crate::ui::UiPlugin;

    #[test]
    fn test_hud_lifecycle() {
        let mut app = App::new();
        app.add_plugins(MinimalPlugins);
        app.add_plugins(bevy::state::app::StatesPlugin);
        app.add_plugins(AssetPlugin::default());
        app.init_asset::<Font>();
        app.init_resource::<ButtonInput<KeyCode>>();
        app.init_resource::<UiScale>();
        app.init_state::<GameState>();
        app.add_plugins(UiPlugin);

        // Frame 1: MainMenu
        app.update();
        let hud_count = app.world_mut().query_filtered::<Entity, With<HudRoot>>().iter(app.world()).count();
        assert_eq!(hud_count, 0, "HUD should not exist in MainMenu");

        // Transition: MainMenu -> Playing
        app.world_mut().resource_mut::<NextState<GameState>>().set(GameState::Playing);
        app.update(); // transition happens
        app.update(); // frame in Playing
        let hud_count = app.world_mut().query_filtered::<Entity, With<HudRoot>>().iter(app.world()).count();
        let text_count = app.world_mut().query_filtered::<Entity, With<LevelExpText>>().iter(app.world()).count();
        assert_eq!(hud_count, 1, "Exactly one HUD in Playing");
        assert_eq!(text_count, 1, "Exactly one LevelExpText in Playing");

        // Transition: Playing -> GachaMenu
        app.world_mut().resource_mut::<NextState<GameState>>().set(GameState::GachaMenu);
        app.update(); // transition happens
        app.update(); // frame in GachaMenu
        let hud_count = app.world_mut().query_filtered::<Entity, With<HudRoot>>().iter(app.world()).count();
        let text_count = app.world_mut().query_filtered::<Entity, With<LevelExpText>>().iter(app.world()).count();
        assert_eq!(hud_count, 0, "HUD should be despawned during GachaMenu");
        assert_eq!(text_count, 0, "No HUD text during GachaMenu");

        // Transition: GachaMenu -> Playing
        app.world_mut().resource_mut::<NextState<GameState>>().set(GameState::Playing);
        app.update(); // transition happens
        app.update(); // frame in Playing
        let hud_count = app.world_mut().query_filtered::<Entity, With<HudRoot>>().iter(app.world()).count();
        let text_count = app.world_mut().query_filtered::<Entity, With<LevelExpText>>().iter(app.world()).count();
        assert_eq!(hud_count, 1, "Exactly one HUD when returning to Playing");
        assert_eq!(text_count, 1, "Exactly one LevelExpText when returning to Playing");

        // Transition: Playing -> GachaMenu again (second level up)
        app.world_mut().resource_mut::<NextState<GameState>>().set(GameState::GachaMenu);
        app.update();
        app.update();

        // Transition: GachaMenu -> Playing again
        app.world_mut().resource_mut::<NextState<GameState>>().set(GameState::Playing);
        app.update();
        app.update();
        let hud_count = app.world_mut().query_filtered::<Entity, With<HudRoot>>().iter(app.world()).count();
        let text_count = app.world_mut().query_filtered::<Entity, With<LevelExpText>>().iter(app.world()).count();
        assert_eq!(hud_count, 1, "Still exactly one HUD after multiple level ups");
        assert_eq!(text_count, 1, "Still exactly one LevelExpText after multiple level ups");
    }
}

