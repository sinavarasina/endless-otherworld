use bevy::prelude::*;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::{BufReader, BufWriter};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ScoreRecord {
    pub level: u32,
    pub score: u32,
    pub duration: String,
}

#[derive(Serialize, Deserialize, Debug, Default, Clone)]
pub struct ScoreHistory {
    pub history: Vec<ScoreRecord>,
}

#[derive(Resource, Debug, Default)]
pub struct ScoreManager {
    pub history: Vec<ScoreRecord>,
    pub file_path: String,
}

impl ScoreManager {
    pub fn load_from_file(path: &str) -> Self {
        let file = match File::open(path) {
            Ok(f) => f,
            Err(_) => {
                return Self {
                    history: Vec::new(),
                    file_path: path.to_string(),
                };
            }
        };

        let reader = BufReader::new(file);
        let history_data: ScoreHistory = serde_json::from_reader(reader).unwrap_or_default();

        Self {
            history: history_data.history,
            file_path: path.to_string(),
        }
    }

    pub fn save_record(&mut self, record: ScoreRecord) {
        self.history.push(record);
        self.history.sort_by_key(|a| std::cmp::Reverse(a.score));

        let data = ScoreHistory {
            history: self.history.clone(),
        };

        if let Ok(file) = File::create(&self.file_path) {
            let writer = BufWriter::new(file);
            let _ = serde_json::to_writer_pretty(writer, &data);
        }
    }

    pub fn get_top_score(&self) -> u32 {
        self.history.first().map(|r| r.score).unwrap_or(0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_score_ranking() {
        let mut manager = ScoreManager {
            history: Vec::new(),
            file_path: "".to_string(),
        };

        manager.save_record(ScoreRecord {
            level: 1,
            score: 100,
            duration: "0:30".to_string(),
        });
        manager.save_record(ScoreRecord {
            level: 3,
            score: 500,
            duration: "2:15".to_string(),
        });
        manager.save_record(ScoreRecord {
            level: 2,
            score: 250,
            duration: "1:10".to_string(),
        });

        assert_eq!(manager.get_top_score(), 500);
        assert_eq!(manager.history[0].score, 500);
        assert_eq!(manager.history[1].score, 250);
        assert_eq!(manager.history[2].score, 100);
    }
}
