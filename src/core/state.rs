use bevy::prelude::*;

#[derive(States, Default, Debug, Clone, Copy, PartialEq, Eq, Hash, Reflect)]
pub enum GameState {
    #[default]
    MainMenu,
    Playing,
    GachaMenu,
    GameOver,
}
