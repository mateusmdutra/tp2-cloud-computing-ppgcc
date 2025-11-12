import pickle
import os
from .config import Config

class ModelLoader:
    """Loads and provides access to association rules from the trained model."""

    def __init__(self, config: Config):
        self.config = config
        self.logger = config.logger
        self.rules = []
        self.model_date = "unknown"
        self._load_model()

    def _load_model(self):
        """Load pickled rules from disk."""
        path = "data/rules.pickle"
        self.logger.info(path)
        if not os.path.exists(path):
            self.logger.error(f"Model file not found at {path}")
            return

        with open(path, "rb") as file:
            content = pickle.load(file)

        self.rules = content.get("rules", [])
        self.model_date = content.get("model_date", "unknown")
        self.logger.info(f"Loaded {len(self.rules)} rules (model date: {self.model_date})")
