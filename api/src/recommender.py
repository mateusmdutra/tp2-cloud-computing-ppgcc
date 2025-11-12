from .config import Config
from .model_loader import ModelLoader
from collections import defaultdict

class RecommendationService:
    """Provides song recommendations based on association rules."""

    def __init__(self, config: Config, model_loader: ModelLoader):
        self.config = config
        self.model_loader = model_loader
        self.logger = config.logger

    def recommend(self, user_songs: list[str]) -> dict:
        """Return song recommendations given user's song list."""
        if not user_songs:
            return {"error": "No songs provided."}, 400

        rules = self.model_loader.rules
        user_set = set(user_songs)
        recommendations = defaultdict(float)

        for antecedent, consequent, confidence in rules:
            if user_set.issuperset(antecedent):
                for song in consequent:
                    if song not in user_set:
                        recommendations[song] = max(recommendations[song], confidence)

        top_songs = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )[: self.config.num_recommendations]

        songs = [song for song, _ in top_songs]

        response = {
            "songs": songs,
            "version": self.config.version,
            "model_date": self.model_loader.model_date,
        }

        self.logger.info(
            f"Recommended {len(songs)} songs (input={len(user_songs)}, rules={len(rules)})"
        )
        return response, 200