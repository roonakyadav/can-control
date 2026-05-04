import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('agent.log')
    ]
)
logger = logging.getLogger('browser-agent')

# API Keys with Fallbacks
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Browser Settings
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# LLM Config
MODEL_NAME = "openai/gpt-4o-mini"
OPEN_ROUTER_BASE_URL = "https://openrouter.ai/api/v1"

def validate_config():
    """Validates that essential configuration is present."""
    missing = []
    if not OPEN_ROUTER_API_KEY: missing.append("OPEN_ROUTER_API_KEY")
    if not TELEGRAM_TOKEN: missing.append("TELEGRAM_TOKEN")
    if not TELEGRAM_CHAT_ID: missing.append("TELEGRAM_CHAT_ID")
    
    if missing:
        logger.warning(f"Missing configuration variables: {', '.join(missing)}")
        return False
    return True
