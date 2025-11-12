from fpgrowth_py import fpgrowth

class RuleMiner:
    """Responsible for discovering association rules."""

    def __init__(self, config):
        self.config = config
        self.logger = config.logger

    def mine(self, itemsets: list[list[str]]) -> list:
        """Run FPGrowth and return discovered rules."""
        min_sup = self.config.min_support
        min_conf = self.config.min_confidence
        self.logger.info(f"Running FPGrowth (support={min_sup}, confidence={min_conf})...")
        _, rules = fpgrowth(itemsets, min_sup, min_conf)
        self.logger.info(f"Generated {len(rules)} rules.")
        return rules
