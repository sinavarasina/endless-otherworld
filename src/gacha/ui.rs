use bevy::prelude::*;
use rand::seq::SliceRandom;

use crate::core::cleanup::cleanup_entities;
use crate::core::state::GameState;
use crate::gacha::components::{GachaCard, GachaEffect, GachaMenuRoot};
use crate::gacha::loader::GachaDeck;
use crate::player::components::PlayerStats;

pub fn spawn_gacha_menu(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    deck: Res<GachaDeck>,
) {
    if deck.items.is_empty() {
        return;
    }

    let mut rng = rand::thread_rng();
    let mut chosen_items: Vec<_> = deck.items.clone();
    chosen_items.shuffle(&mut rng);
    let chosen_items: Vec<_> = chosen_items.into_iter().take(3).collect();

    let font_handle: Handle<Font> = asset_server.load("font/bloodcrow.ttf");

    commands
        .spawn((
            GachaMenuRoot,
            Node {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                flex_direction: FlexDirection::Column,
                justify_content: JustifyContent::SpaceEvenly,
                align_items: AlignItems::Center,
                padding: UiRect::all(Val::Px(40.0)),
                ..default()
            },
            BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.75)),
        ))
        .with_children(|parent| {
            // Title Header
            parent.spawn((
                Text::new("Choose your faith!"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 72.0,
                    ..default()
                },
                TextColor(Color::WHITE),
            ));

            // Cards row
            parent
                .spawn(Node {
                    width: Val::Percent(90.0),
                    flex_direction: FlexDirection::Row,
                    justify_content: JustifyContent::SpaceEvenly,
                    align_items: AlignItems::Center,
                    ..default()
                })
                .with_children(|row| {
                    for (i, item) in chosen_items.into_iter().enumerate() {
                        let item_image_path = format!("images/GachaItems/{}", item.image_name);

                        row.spawn((
                            Button,
                            GachaCard {
                                choice_index: i,
                                item: item.clone(),
                            },
                            Node {
                                width: Val::Px(280.0),
                                min_height: Val::Px(380.0),
                                flex_direction: FlexDirection::Column,
                                justify_content: JustifyContent::SpaceBetween,
                                align_items: AlignItems::Center,
                                padding: UiRect::all(Val::Px(20.0)),
                                border: UiRect::all(Val::Px(3.0)),
                                ..default()
                            },
                            BorderColor(Color::srgba(0.9, 0.9, 0.9, 0.8)),
                            BackgroundColor(Color::srgba(0.1, 0.1, 0.15, 0.85)),
                        ))
                        .with_children(|card| {
                            // Number at top
                            card.spawn((
                                Text::new(format!("{}", i + 1)),
                                TextFont {
                                    font: font_handle.clone(),
                                    font_size: 48.0,
                                    ..default()
                                },
                                TextColor(Color::srgb(1.0, 0.84, 0.0)),
                            ));

                            // Item Image
                            card.spawn((
                                ImageNode::new(asset_server.load(item_image_path)),
                                Node {
                                    width: Val::Px(160.0),
                                    height: Val::Px(160.0),
                                    margin: UiRect::vertical(Val::Px(10.0)),
                                    ..default()
                                },
                            ));

                            // Description text
                            card.spawn((
                                Text::new(&item.description),
                                TextFont {
                                    font: font_handle.clone(),
                                    font_size: 20.0,
                                    ..default()
                                },
                                TextColor(Color::WHITE),
                            ));
                        });
                    }
                });

            // Subtitle footer
            parent.spawn((
                Text::new("Press 1, 2, or 3 (or Click) to select your reward"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 32.0,
                    ..default()
                },
                TextColor(Color::srgb(0.8, 0.8, 0.8)),
            ));
        });
}

pub fn gacha_input_system(
    keyboard: Res<ButtonInput<KeyCode>>,
    mut interaction_q: Query<(&Interaction, &GachaCard), Changed<Interaction>>,
    all_cards_q: Query<&GachaCard>,
    mut next_state: ResMut<NextState<GameState>>,
    mut player_stats_q: Query<&mut PlayerStats>,
) {
    let mut selected_effect: Option<GachaEffect> = None;

    // Check keyboard input: 1, 2, 3
    if keyboard.just_pressed(KeyCode::Digit1) || keyboard.just_pressed(KeyCode::Numpad1) {
        selected_effect = all_cards_q.iter().find(|c| c.choice_index == 0).map(|c| c.item.effect);
    } else if keyboard.just_pressed(KeyCode::Digit2) || keyboard.just_pressed(KeyCode::Numpad2) {
        selected_effect = all_cards_q.iter().find(|c| c.choice_index == 1).map(|c| c.item.effect);
    } else if keyboard.just_pressed(KeyCode::Digit3) || keyboard.just_pressed(KeyCode::Numpad3) {
        selected_effect = all_cards_q.iter().find(|c| c.choice_index == 2).map(|c| c.item.effect);
    }

    // Check mouse click input
    if selected_effect.is_none() {
        for (interaction, card) in interaction_q.iter_mut() {
            if *interaction == Interaction::Pressed {
                selected_effect = Some(card.item.effect);
                break;
            }
        }
    }

    // Apply effect if selected
    if let (Some(effect), Ok(mut stats)) = (selected_effect, player_stats_q.get_single_mut()) {
        match effect {
                GachaEffect::HealFull => {
                    stats.hp = stats.max_hp;
                }
                GachaEffect::BoostHpMax => {
                    stats.max_hp *= 3.0;
                    stats.hp = stats.max_hp;
                }
                GachaEffect::SacrificeHpForAttack => {
                    stats.hp = (stats.hp / 2.0).max(1.0);
                    stats.attack += 20.0;
                }
                GachaEffect::KillSelf => {
                    stats.hp = 0.0;
                }
                GachaEffect::AttackSpeed => {
                    stats.bullet_speed += 150.0;
                    stats.shoot_cooldown = Timer::from_seconds(0.12, TimerMode::Once);
                }
                GachaEffect::BulletSpeed => {
                    stats.bullet_anim_speed *= 1.5;
                    stats.bullet_speed += 200.0;
                }
            }

        if stats.hp <= 0.0 {
            next_state.set(GameState::GameOver);
        } else {
            next_state.set(GameState::Playing);
        }
    }
}

pub fn despawn_gacha_menu(
    commands: Commands,
    query: Query<Entity, With<GachaMenuRoot>>,
) {
    cleanup_entities::<GachaMenuRoot>(commands, query);
}
