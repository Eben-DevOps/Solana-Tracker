import sqlite3
import requests
from config.settings import DB_PATH, SOLANA_RPC_URL, WATCHED_WALLETS

# Example script to show usage of configurations
def main():
    # Connect to SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create a sample table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS wallet_movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wallet TEXT NOT NULL,
        action TEXT NOT NULL,
        amount REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()

    # Sample interaction with Solana RPC
    response = requests.get(SOLANA_RPC_URL)
    print("RPC Response:", response.status_code)

    # Example wallet processing
    print("Tracking wallets:", WATCHED_WALLETS)

if __name__ == "__main__":
    main()
