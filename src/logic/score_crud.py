import json
import os
from path_config import SCORE_PATH


class ScoreCRUD:
    def __init__(self):
        if not os.path.exists(SCORE_PATH):
            with open(SCORE_PATH, "w") as f:
                json.dump({"history": []}, f)

        with open(SCORE_PATH, "r") as f:
            try:
                self.data = json.load(f)
            except json.JSONDecodeError:
                self.data = {"history": []}

    def read_all(self):
        return self.data.get("history", [])

    def add_score(self, new_score: dict):
        self.data["history"].append(new_score)
        self.data["history"].sort(key=lambda x: x.get("score", 0), reverse=True)
        self._commit()

    def _commit(self):
        with open(SCORE_PATH, "w") as f:
            json.dump(self.data, f, indent=4)
