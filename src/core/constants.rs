pub const WINDOW_WIDTH: f32 = 1920.0;
pub const WINDOW_HEIGHT: f32 = 1080.0;

pub const MAP_SIZE: f32 = 10000.0;
pub const HALF_MAP_SIZE: f32 = MAP_SIZE / 2.0;

pub const Z_BACKGROUND: f32 = 0.0;
pub const Z_OBSTACLE: f32 = 10.0;
pub const Z_ENEMY: f32 = 20.0;
pub const Z_PLAYER: f32 = 30.0;
pub const Z_BULLET: f32 = 40.0;
pub const Z_EFFECT: f32 = 50.0;

/// Wraps world coordinate across [0, MAP_SIZE) for a toroidal map.
#[inline]
pub fn wrap_map_coord(val: f32) -> f32 {
    let rem = val % MAP_SIZE;
    if rem < 0.0 {
        rem + MAP_SIZE
    } else {
        rem
    }
}
