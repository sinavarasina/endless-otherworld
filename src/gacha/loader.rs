use bevy::prelude::*;
use serde::Deserialize;

use crate::gacha::components::{GachaEffect, GachaItem};

#[derive(Deserialize, Debug)]
struct RawItem {
    items: String,
    imagename: String,
    #[serde(rename = "Description")]
    description: String,
    #[serde(rename = "Effect")]
    effect: Option<String>,
}

#[derive(Deserialize, Debug)]
struct RawData {
    gacha_items: Vec<RawItem>,
}

#[derive(Resource, Debug, Default, Clone)]
pub struct GachaDeck {
    pub items: Vec<GachaItem>,
}

impl GachaDeck {
    pub fn load_embedded() -> Self {
        const CONFIG_JSON: &str = include_str!("../../assets/config/game_data.json");

        let raw_data: RawData = match serde_json::from_str(CONFIG_JSON) {
            Ok(data) => data,
            Err(err) => {
                warn!("Failed to parse embedded gacha config: {}", err);
                return Self::default();
            }
        };

        let items: Vec<GachaItem> = raw_data
            .gacha_items
            .into_iter()
            .map(|raw| {
                let effect_str = raw.effect.as_deref().unwrap_or(raw.items.as_str());
                let effect = match effect_str {
                    "HealFull" | "heart1" => GachaEffect::HealFull,
                    "BoostHpMax" | "heart2" => GachaEffect::BoostHpMax,
                    "SacrificeHpForAttack" | "heart3" => GachaEffect::SacrificeHpForAttack,
                    "Vitality" => GachaEffect::Vitality,
                    "SecondWind" => GachaEffect::SecondWind,
                    "AttackRate" | "ring1" => GachaEffect::AttackRate,
                    "BulletSpeed" | "ring2" => GachaEffect::BulletSpeed,
                    "MoveSpeed" => GachaEffect::MoveSpeed,
                    "AddAttack" => GachaEffect::AddAttack,
                    "Sniper" => GachaEffect::Sniper,
                    "Haste" => GachaEffect::Haste,
                    "AllStats" => GachaEffect::AllStats,
                    "KillSelf" | "killyourself" => GachaEffect::KillSelf,
                    _ => GachaEffect::HealFull,
                };

                GachaItem {
                    id: raw.items,
                    image_name: raw.imagename,
                    description: raw.description,
                    effect,
                }
            })
            .collect();

        Self { items }
    }
}
