use bevy::prelude::*;
use rand::seq::SliceRandom;

use crate::core::cleanup::cleanup_entities;
use crate::core::state::GameState;
use crate::gacha::components::{GachaCard, GachaEffect, GachaItem, GachaMenuRoot};
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
    let mut chosen_items: Vec<GachaItem> = deck.items.clone();
    chosen_items.shuffle(&mut rng);
    let chosen_items: Vec<GachaItem> = chosen_items.into_iter().take(3).collect();

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
                padding: UiRect::axes(Val::Px(40.0), Val::Px(24.0)),
                ..default()
            },
            BackgroundColor(Color::srgba(0.0, 0.0, 0.0, 0.8)),
        ))
        .with_children(|parent| {
            // Title Header
            parent.spawn((
                Text::new("Choose your faith!"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 64.0,
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
                    column_gap: Val::Px(30.0),
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
                                width: Val::Px(290.0),
                                min_height: Val::Px(360.0),
                                flex_direction: FlexDirection::Column,
                                justify_content: JustifyContent::SpaceBetween,
                                align_items: AlignItems::Center,
                                padding: UiRect::all(Val::Px(18.0)),
                                border: UiRect::all(Val::Px(2.0)),
                                ..default()
                            },
                            BorderColor(Color::srgba(0.85, 0.85, 0.85, 0.7)),
                            BackgroundColor(Color::srgba(0.08, 0.08, 0.12, 0.9)),
                        ))
                        .with_children(|card| {
                            // Number at top
                            card.spawn((
                                Text::new(format!("{}", i + 1)),
                                TextFont {
                                    font: font_handle.clone(),
                                    font_size: 42.0,
                                    ..default()
                                },
                                TextColor(Color::srgb(1.0, 0.84, 0.0)),
                            ));

                            // Item Image
                            card.spawn((
                                ImageNode::new(asset_server.load(item_image_path)),
                                Node {
                                    width: Val::Px(140.0),
                                    height: Val::Px(140.0),
                                    margin: UiRect::vertical(Val::Px(8.0)),
                                    ..default()
                                },
                            ));

                            // Description text with word wrap
                            card.spawn((
                                Text::new(&item.description),
                                TextFont {
                                    font: font_handle.clone(),
                                    font_size: 18.0,
                                    ..default()
                                },
                                TextColor(Color::WHITE),
                                Node {
                                    max_width: Val::Px(250.0),
                                    ..default()
                                },
                            ));
                        });
                    }
                });

            // Subtitle footer
            parent.spawn((
                Text::new("Press 1, 2, or 3 (or Click) to select your reward"),
                TextFont {
                    font: font_handle.clone(),
                    font_size: 28.0,
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

    if keyboard.just_pressed(KeyCode::Digit1) || keyboard.just_pressed(KeyCode::Numpad1) {
        selected_effect = all_cards_q.iter().find(|c| c.choice_index == 0).map(|c| c.item.effect);
    } else if keyboard.just_pressed(KeyCode::Digit2) || keyboard.just_pressed(KeyCode::Numpad2) {
        selected_effect = all_cards_q.iter().find(|c| c.choice_index == 1).map(|c| c.item.effect);
    } else if keyboard.just_pressed(KeyCode::Digit3) || keyboard.just_pressed(KeyCode::Numpad3) {
        selected_effect = all_cards_q.iter().find(|c| c.choice_index == 2).map(|c| c.item.effect);
    }

    if selected_effect.is_none() {
        for (interaction, card) in interaction_q.iter_mut() {
            if *interaction == Interaction::Pressed {
                selected_effect = Some(card.item.effect);
                break;
            }
        }
    }

    if let (Some(effect), Ok(mut stats)) = (selected_effect, player_stats_q.get_single_mut()) {
        match effect {
            GachaEffect::HealFull => {
                stats.hp = stats.max_hp;
            }
            GachaEffect::BoostHpMax => {
                stats.max_hp *= 1.5;
                stats.hp = stats.max_hp;
            }
            GachaEffect::SacrificeHpForAttack => {
                stats.hp = (stats.hp * 0.7).max(1.0);
                stats.attack += 25.0;
            }
            GachaEffect::Vitality => {
                stats.max_hp += 40.0;
                stats.hp = (stats.hp + 40.0).min(stats.max_hp);
            }
            GachaEffect::SecondWind => {
                let missing = stats.max_hp - stats.hp;
                stats.hp = (stats.hp + missing * 0.5).min(stats.max_hp);
            }
            GachaEffect::AttackRate => {
                let cur = stats.shoot_cooldown.duration().as_secs_f32();
                stats.shoot_cooldown = Timer::from_seconds((cur * 0.8).max(0.06), TimerMode::Once);
            }
            GachaEffect::BulletSpeed => {
                stats.bullet_speed += 250.0;
                stats.bullet_anim_speed *= 1.3;
            }
            GachaEffect::MoveSpeed => {
                stats.speed += 50.0;
            }
            GachaEffect::AddAttack => {
                stats.attack += 20.0;
            }
            GachaEffect::Sniper => {
                stats.bullet_speed += 300.0;
                stats.attack += 15.0;
            }
            GachaEffect::Haste => {
                stats.speed += 35.0;
                let cur = stats.shoot_cooldown.duration().as_secs_f32();
                stats.shoot_cooldown = Timer::from_seconds((cur * 0.85).max(0.06), TimerMode::Once);
            }
            GachaEffect::AllStats => {
                stats.attack += 15.0;
                stats.max_hp += 30.0;
                stats.hp = (stats.hp + 30.0).min(stats.max_hp);
                stats.speed += 25.0;
            }
            GachaEffect::KillSelf => {
                stats.hp = 0.0;
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
