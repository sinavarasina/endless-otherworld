use bevy::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GachaEffect {
    HealFull,
    BoostHpMax,
    SacrificeHpForAttack,
    Vitality,
    SecondWind,
    AttackRate,
    BulletSpeed,
    MoveSpeed,
    AddAttack,
    Sniper,
    Haste,
    AllStats,
    KillSelf,
}

#[derive(Debug, Clone)]
pub struct GachaItem {
    pub id: String,
    pub image_name: String,
    pub description: String,
    pub effect: GachaEffect,
}

#[derive(Component, Debug)]
pub struct GachaCard {
    pub choice_index: usize,
    pub item: GachaItem,
}

#[derive(Component, Debug, Default)]
pub struct GachaMenuRoot;
