import sqlite3

class Database:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT,
            token TEXT,
            change INTEGER,
            signature TEXT
        )
        """
        self.connection.execute(query)
        self.connection.commit()

    def store_movement(self, movement):
        query = """
        INSERT INTO movements (wallet, token, change, signature)
        VALUES (?, ?, ?, ?)
        """
        self.connection.execute(
            query, (movement["wallet"], movement["token"], movement["change"], movement["signature"])
        )
        self.connection.commit()

    def fetch_movements(self):
        query = "SELECT * FROM movements"
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
