import os
import logging

class Config:
    """Holds configuration for the recommendation API."""

    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH", "data/rules.pickle")
        self.version = os.getenv("VERSION", "1.0")
        self.num_recommendations = int(os.getenv("RECOMMENDATION_SONGS", 3))

        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)
