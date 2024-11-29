import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment configurations
SOLANA_RPC_URL = os.getenv("SOLANA_RPC_URL")
WATCHED_WALLETS = os.getenv("WATCHED_WALLETS").split(",")
DB_PATH = os.getenv("DB_PATH")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
