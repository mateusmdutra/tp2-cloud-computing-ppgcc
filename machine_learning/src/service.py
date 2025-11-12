import time
import ssl
from .data_loader import DatasetLoader
from .rule_miner import RuleMiner
from .persistence import RuleRepository

class RuleGenerationService:
    """Coordinates the entire pipeline: load → preprocess → mine → save → loop."""

    def __init__(self, config):
        self.config = config
        self.loader = DatasetLoader(config)
        self.miner = RuleMiner(config)
        self.repo = RuleRepository(config)
        ssl._create_default_https_context = ssl._create_unverified_context

    def run(self):
        """Run the complete rule generation pipeline."""
        self.config.logger.info("Starting playlist rule generation service...")
        df = self.loader.load()
        itemsets = self.loader.prepare_itemsets(df)
        rules = self.miner.mine(itemsets)
        self.repo.save(rules)

        while True:
            self.config.logger.info(
                f"Rules generated and saved. Sleeping for {self.config.loop_interval}s..."
            )
            time.sleep(self.config.loop_interval)
