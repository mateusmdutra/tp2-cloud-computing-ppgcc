from datetime import datetime
import pytz
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

    def get_current_time_str(self):
        now_utc = datetime.now(pytz.utc)
        sao_paulo_time = now_utc.astimezone(pytz.timezone("America/Sao_Paulo"))
        sao_paulo_time_str = sao_paulo_time.strftime("%Y-%m-%d %H:%M:%S")
        return sao_paulo_time_str

    def run(self):
        """Run the complete rule generation pipeline."""
        self.config.logger.info("Starting playlist rule generation service...")
        df = self.loader.load()
        itemsets = self.loader.prepare_itemsets(df)
        rules = self.miner.mine(itemsets)
        self.repo.save(rules)

        self.config.logger.info(
            f"Run complete. Exiting, current time is {self.get_current_time_str()}"
        )
