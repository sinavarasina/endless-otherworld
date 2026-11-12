use bevy::prelude::*;
use crate::player::components::PlayerFacing;

#[derive(Resource)]
pub struct PlayerAssets {
    pub layout: Handle<TextureAtlasLayout>,
    pub bullet_layout: Handle<TextureAtlasLayout>,
    pub bullet_texture: Handle<Image>,
    pub idle_down: Handle<Image>,
    pub walk_down: Handle<Image>,
    pub walk_up: Handle<Image>,
    pub walk_left_down: Handle<Image>,
    pub walk_right_down: Handle<Image>,
    pub walk_left_up: Handle<Image>,
    pub walk_right_up: Handle<Image>,
}

impl PlayerAssets {
    pub fn get_image_for_facing(&self, facing: PlayerFacing) -> Handle<Image> {
        match facing {
            PlayerFacing::IdleDown => self.idle_down.clone(),
            PlayerFacing::WalkDown => self.walk_down.clone(),
            PlayerFacing::WalkUp => self.walk_up.clone(),
            PlayerFacing::WalkLeftDown => self.walk_left_down.clone(),
            PlayerFacing::WalkRightDown => self.walk_right_down.clone(),
            PlayerFacing::WalkLeftUp => self.walk_left_up.clone(),
            PlayerFacing::WalkRightUp => self.walk_right_up.clone(),
        }
    }
}

pub fn load_player_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let hero_layout = TextureAtlasLayout::from_grid(
        UVec2::new(48, 64),
        6,
        1,
        None,
        None,
    );
    let bullet_layout = TextureAtlasLayout::from_grid(
        UVec2::new(32, 32),
        4,
        1,
        None,
        None,
    );

    let assets = PlayerAssets {
        layout: atlas_layouts.add(hero_layout),
        bullet_layout: atlas_layouts.add(bullet_layout),
        bullet_texture: asset_server.load("images/Bullet/BlueShurikenAnimation.png"),
        idle_down: asset_server.load("images/Hero/idle_down.png"),
        walk_down: asset_server.load("images/Hero/walk_down.png"),
        walk_up: asset_server.load("images/Hero/walk_up.png"),
        walk_left_down: asset_server.load("images/Hero/walk_left_down.png"),
        walk_right_down: asset_server.load("images/Hero/walk_right_down.png"),
        walk_left_up: asset_server.load("images/Hero/walk_left_up.png"),
        walk_right_up: asset_server.load("images/Hero/walk_right_up.png"),
    };

    commands.insert_resource(assets);
}
