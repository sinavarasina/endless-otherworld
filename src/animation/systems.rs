use bevy::prelude::*;
use crate::animation::components::SpriteAnimation;

pub fn update_sprite_animation(
    time: Res<Time>,
    mut query: Query<(&mut SpriteAnimation, &mut Sprite)>,
) {
    for (mut animation, mut sprite) in query.iter_mut() {
        animation.timer.tick(time.delta());

        if animation.timer.just_finished()
            && let Some(atlas) = &mut sprite.texture_atlas
        {
            let current_offset = atlas.index.saturating_sub(animation.first_index);
            let next_offset = (current_offset + 1) % animation.frame_count.max(1);
            atlas.index = animation.first_index + next_offset;
        }
    }
}
