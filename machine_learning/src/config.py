import os
import logging

class Config:
    """Holds all configuration and environment settings."""

    def __init__(self):
        self.min_support = self._get_env_float("MIN_SUPPORT_RATIO", 0.05)
        self.min_confidence = self._get_env_float("MIN_CONFIDENCE", 0.03)
        self.dataset_url = os.getenv("DATASET_ADDRESS", "https://homepages.dcc.ufmg.br/~cunha/hosted/cloudcomp-2023s2-datasets/2023_spotify_ds2.csv")
        self.results_path = "data/rules.pickle"
        self.version = os.getenv("VERSION", "1.0")

        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)

    def _get_env_float(self, name: str, default: float) -> float:
        """Retrieve a float environment variable safely."""
        try:
            return float(os.getenv(name, default))
        except ValueError:
            self.logger.warning(f"Invalid value for {name}, using default {default}")
            return default
