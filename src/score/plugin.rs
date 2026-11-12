use bevy::prelude::*;
use crate::combat::components::GameOverEvent;
use crate::score::storage::{ScoreManager, ScoreRecord};

pub struct ScorePlugin;

fn handle_game_over_score(
    mut game_over_events: EventReader<GameOverEvent>,
    mut score_manager: ResMut<ScoreManager>,
) {
    for event in game_over_events.read() {
        let minutes = event.survival_seconds / 60;
        let seconds = event.survival_seconds % 60;
        let duration_str = format!("{}:{:02}", minutes, seconds);

        score_manager.save_record(ScoreRecord {
            level: event.level,
            score: event.final_score,
            duration: duration_str,
        });
    }
}

impl Plugin for ScorePlugin {
    fn build(&self, app: &mut App) {
        let manager = ScoreManager::load_default();
        app.insert_resource(manager)
            .add_systems(Update, handle_game_over_score);
    }
}
