use bevy::prelude::*;
use crate::enemy::components::EnemyKind;

#[derive(Resource)]
pub struct EnemyAssets {
    // Enemy textures & layouts
    pub ghost_texture: Handle<Image>,
    pub ghost_layout: Handle<TextureAtlasLayout>,

    pub flame_texture: Handle<Image>,
    pub flame_layout: Handle<TextureAtlasLayout>,

    pub demonz_texture: Handle<Image>,
    pub demonz_layout: Handle<TextureAtlasLayout>,

    pub capybara_texture: Handle<Image>,
    pub capybara_layout: Handle<TextureAtlasLayout>,

    // Enemy bullet textures & layouts
    pub ghost_bullet_texture: Handle<Image>,
    pub ghost_bullet_layout: Handle<TextureAtlasLayout>,

    pub flame_bullet_texture: Handle<Image>,
    pub flame_bullet_layout: Handle<TextureAtlasLayout>,

    pub demonz_bullet_texture: Handle<Image>,
    pub demonz_bullet_layout: Handle<TextureAtlasLayout>,

    pub capybara_bullet_texture: Handle<Image>,
    pub capybara_bullet_layout: Handle<TextureAtlasLayout>,
}

impl EnemyAssets {
    pub fn get_enemy_render_info(
        &self,
        kind: EnemyKind,
    ) -> (Handle<Image>, Handle<TextureAtlasLayout>, usize, f32) {
        match kind {
            EnemyKind::Ghost => (self.ghost_texture.clone(), self.ghost_layout.clone(), 6, 2.5),
            EnemyKind::Flame => (self.flame_texture.clone(), self.flame_layout.clone(), 6, 2.5),
            EnemyKind::Demonz => (self.demonz_texture.clone(), self.demonz_layout.clone(), 6, 2.5),
            EnemyKind::Capybara => (self.capybara_texture.clone(), self.capybara_layout.clone(), 6, 2.5),
        }
    }

    pub fn get_bullet_render_info(
        &self,
        kind: EnemyKind,
    ) -> (Handle<Image>, Handle<TextureAtlasLayout>, usize, f32) {
        match kind {
            EnemyKind::Ghost => (
                self.ghost_bullet_texture.clone(),
                self.ghost_bullet_layout.clone(),
                6,
                2.0,
            ),
            EnemyKind::Flame => (
                self.flame_bullet_texture.clone(),
                self.flame_bullet_layout.clone(),
                4,
                2.0,
            ),
            EnemyKind::Demonz => (
                self.demonz_bullet_texture.clone(),
                self.demonz_bullet_layout.clone(),
                4,
                2.0,
            ),
            EnemyKind::Capybara => (
                self.capybara_bullet_texture.clone(),
                self.capybara_bullet_layout.clone(),
                4,
                2.0,
            ),
        }
    }
}

pub fn load_enemy_assets(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let ghost_layout = atlas_layouts.add(TextureAtlasLayout::from_grid(
        UVec2::new(48, 48),
        6,
        1,
        None,
        None,
    ));
    let flame_layout = atlas_layouts.add(TextureAtlasLayout::from_grid(
        UVec2::new(24, 24),
        6,
        1,
        None,
        None,
    ));
    let demonz_layout = atlas_layouts.add(TextureAtlasLayout::from_grid(
        UVec2::new(24, 24),
        6,
        1,
        None,
        None,
    ));
    let capybara_layout = atlas_layouts.add(TextureAtlasLayout::from_grid(
        UVec2::new(64, 70),
        6,
        1,
        None,
        None,
    ));

    // Bullet layouts
    let bullet_layout_6 = atlas_layouts.add(TextureAtlasLayout::from_grid(
        UVec2::new(32, 32),
        6,
        1,
        None,
        None,
    ));
    let bullet_layout_4 = atlas_layouts.add(TextureAtlasLayout::from_grid(
        UVec2::new(32, 32),
        4,
        1,
        None,
        None,
    ));

    commands.insert_resource(EnemyAssets {
        ghost_texture: asset_server.load("images/Enemies/CasperSprites.png"),
        ghost_layout,

        flame_texture: asset_server.load("images/Enemies/flame_mons.png"),
        flame_layout,

        demonz_texture: asset_server.load("images/Enemies/demonz.png"),
        demonz_layout,

        capybara_texture: asset_server.load("images/Enemies/bigcapybara.png"),
        capybara_layout,

        ghost_bullet_texture: asset_server.load("images/Bullet/PurpleBulletAnimation.png"),
        ghost_bullet_layout: bullet_layout_6,

        flame_bullet_texture: asset_server.load("images/Bullet/Bullet_Flamez_32x32px.png"),
        flame_bullet_layout: bullet_layout_4.clone(),

        demonz_bullet_texture: asset_server.load("images/Bullet/Bullet_Demonz_32x32px.png"),
        demonz_bullet_layout: bullet_layout_4.clone(),

        capybara_bullet_texture: asset_server.load("images/Bullet/bluetornadobullet.png"),
        capybara_bullet_layout: bullet_layout_4,
    });
}
