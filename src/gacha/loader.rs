use bevy::prelude::*;
use serde::Deserialize;
use std::fs::File;
use std::io::BufReader;

use crate::gacha::components::{GachaEffect, GachaItem};

#[derive(Deserialize, Debug)]
struct RawGachaItem {
    items: String,
    imagename: String,
    #[serde(rename = "Description")]
    description: String,
}

#[derive(Deserialize, Debug)]
struct RawGachaData {
    gacha_items: Vec<RawGachaItem>,
}

#[derive(Resource, Debug, Default, Clone)]
pub struct GachaDeck {
    pub items: Vec<GachaItem>,
}

impl GachaDeck {
    pub fn load_from_file(config_path: &str) -> Self {
        let file = match File::open(config_path) {
            Ok(f) => f,
            Err(err) => {
                warn!("Could not open gacha config at {}: {}", config_path, err);
                return Self::default();
            }
        };

        let reader = BufReader::new(file);
        let raw_data: RawGachaData = match serde_json::from_reader(reader) {
            Ok(data) => data,
            Err(err) => {
                warn!("Failed to parse gacha config: {}", err);
                return Self::default();
            }
        };

        let items: Vec<GachaItem> = raw_data
            .gacha_items
            .into_iter()
            .map(|raw| {
                let effect = match raw.items.as_str() {
                    "heart1" => GachaEffect::HealFull,
                    "heart2" => GachaEffect::BoostHpMax,
                    "heart3" => GachaEffect::SacrificeHpForAttack,
                    "killyourself" => GachaEffect::KillSelf,
                    "ring1" => GachaEffect::AttackSpeed,
                    "ring2" => GachaEffect::BulletSpeed,
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

        info!("Loaded {} gacha items into deck", items.len());
        Self { items }
    }
}
