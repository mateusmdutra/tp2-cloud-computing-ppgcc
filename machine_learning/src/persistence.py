import os
import pickle
from datetime import datetime

class RuleRepository:
    """Handles persistence of rule metadata."""

    def __init__(self, config):
        self.config = config
        self.logger = config.logger

    def save(self, rules: list):
        """Save rules and metadata to a pickle file."""
        output_path = self.config.results_path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        metadata = {
            "rules": rules,
            "version": self.config.version,
            "model_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        with open(output_path, "wb") as f:
            pickle.dump(metadata, f)
        self.logger.info(f"Saved {len(rules)} rules to {output_path}")
