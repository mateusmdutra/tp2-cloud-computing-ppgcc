import pandas as pd

class DatasetLoader:
    """Handles loading and preprocessing of playlist data."""

    def __init__(self, config):
        self.config = config
        self.logger = config.logger

    def load(self) -> pd.DataFrame:
        """Load dataset from configured URL."""
        url = self.config.dataset_url
        self.logger.info(f"Loading dataset from {url}")
        return pd.read_csv(url)

    def prepare_itemsets(self, df: pd.DataFrame) -> list[list[str]]:
        """Convert playlist DataFrame into itemsets."""
        self.logger.info("Preparing itemsets for rule mining...")
        itemsets = (
            df.dropna(subset=["pid", "track_name"])
              .astype({"pid": str, "track_name": str})
              .groupby("pid", sort=False)["track_name"]
              .apply(lambda s: s.drop_duplicates().astype(str).tolist())
              .tolist()
        )
        self.logger.info(f"Prepared {len(itemsets)} playlists.")
        return itemsets
