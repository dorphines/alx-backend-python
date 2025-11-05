import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # print(f"Database connection to {self.db_name} opened.")
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            # print(f"Database connection to {self.db_name} closed.")
        if exc_type:
            print(f"An exception occurred: {exc_val}")
        return False # Propagate exceptions

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.results = None

    def __enter__(self):
        with DatabaseConnection(self.db_name) as cursor:
            cursor.execute(self.query, self.params)
            self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        # No explicit cleanup needed here as DatabaseConnection handles it
        if exc_type:
            print(f"An exception occurred during query execution: {exc_val}")
        return False

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
            (3, 'Charlie', 35),
            (4, 'David', 40),
            (5, 'Eve', 28)
        """)
        cursor.connection.commit()
    print("Database setup complete.")

if __name__ == "__main__":
    DB_NAME = "test_database.db"
    setup_database(DB_NAME)

    print("\n--- Querying users older than 25 ---")
    query_str = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(DB_NAME, query_str, (25,)) as users_over_25:
        for row in users_over_25:
            print(row)
    print("--- Query complete ---")

    print("\n--- Querying all users ---")
    query_all_str = "SELECT * FROM users"
    with ExecuteQuery(DB_NAME, query_all_str) as all_users:
        for row in all_users:
            print(row)
    print("--- Query complete ---")
