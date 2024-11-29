import requests

class TelegramAlerts:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_alert(self, movement):
        message = (
            f"Detected Wallet Activity:\n"
            f"Wallet: {movement['wallet']}\n"
            f"Token: {movement['token']}\n"
            f"Change: {movement['change']}\n"
            f"Signature: {movement['signature']}"
        )
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {"chat_id": self.chat_id, "text": message}
        requests.post(url, data=data)
