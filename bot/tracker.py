import time
import requests
import sqlite3
from solana.rpc.api import Client
from solana.publickey import PublicKey
from .database import Database
from .alerts import TelegramAlerts

class WalletTracker:
    def __init__(self, solana_rpc_url, watched_wallets, db_path, telegram_token, telegram_chat_id):
        self.client = Client(solana_rpc_url)
        self.watched_wallets = watched_wallets
        self.db = Database(db_path)
        self.alerts = TelegramAlerts(telegram_token, telegram_chat_id)

    def fetch_wallet_transactions(self, wallet_address):
        try:
            response = self.client.get_confirmed_signature_for_address2(
                PublicKey(wallet_address), limit=10
            )
            return response.get("result", [])
        except Exception as e:
            print(f"Error fetching transactions for {wallet_address}: {e}")
            return []

    def analyze_transactions(self, transactions):
        token_movements = []
        for tx in transactions:
            tx_data = self.client.get_confirmed_transaction(tx["signature"])
            if tx_data["result"]:
                meta = tx_data["result"]["meta"]
                if meta and "preTokenBalances" in meta and "postTokenBalances" in meta:
                    pre_balances = meta["preTokenBalances"]
                    post_balances = meta["postTokenBalances"]
                    for pre, post in zip(pre_balances, post_balances):
                        if pre["owner"] != post["owner"]:
                            movement = {
                                "wallet": pre["owner"],
                                "token": post["mint"],
                                "change": int(post["uiTokenAmount"]["amount"])
                                - int(pre["uiTokenAmount"]["amount"]),
                                "signature": tx["signature"],
                            }
                            token_movements.append(movement)
        return token_movements

    def monitor_wallets(self):
        while True:
            for wallet in self.watched_wallets:
                transactions = self.fetch_wallet_transactions(wallet)
                movements = self.analyze_transactions(transactions)
                for movement in movements:
                    print(f"Detected activity: {movement}")
                    self.db.store_movement(movement)
                    self.alerts.send_alert(movement)
            time.sleep(30)
