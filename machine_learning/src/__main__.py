from .config import Config
from .service import RuleGenerationService

if __name__ == "__main__":
    config = Config()
    service = RuleGenerationService(config)
    service.run()
