import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Database connection to {self.db_name} opened.")
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print(f"Database connection to {self.db_name} closed.")
        if exc_type:
            print(f"An exception occurred: {exc_val}")
        return False # Propagate exceptions

def setup_database(db_name="test_database.db"):
    with DatabaseConnection(db_name) as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        cursor.execute("""
            INSERT OR IGNORE INTO users (id, name, age) VALUES
            (1, 'Alice', 30),
            (2, 'Bob', 24),
            (3, 'Charlie', 35)
        """)
        cursor.connection.commit()
    print("Database setup complete.")

if __name__ == "__main__":
    DB_NAME = "test_database.db"
    setup_database(DB_NAME)

    print("\n--- Querying users ---")
    with DatabaseConnection(DB_NAME) as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
    print("--- Query complete ---")
