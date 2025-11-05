import asyncio
import aiosqlite

DB_NAME = "test_async_database.db"

async def setup_async_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
        """)
        await db.execute("""
            INSERT OR IGNORE INTO users (id, name, age) VALUES
            (1, 'Alice', 30),
            (2, 'Bob', 24),
            (3, 'Charlie', 35),
            (4, 'David', 40),
            (5, 'Eve', 28),
            (6, 'Frank', 45),
            (7, 'Grace', 50)
        """)
        await db.commit()
    print("Asynchronous database setup complete.")

async def async_fetch_users():
    print("Fetching all users...")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users fetched.")
            return users

async def async_fetch_older_users():
    print("Fetching users older than 40...")
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("Users older than 40 fetched.")
            return older_users

async def fetch_concurrently():
    await setup_async_database()
    print("\n--- Starting concurrent fetches ---")
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("--- Concurrent fetches complete ---")

    print("\nAll Users:")
    for user in users:
        print(user)

    print("\nUsers Older than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    try:
        asyncio.run(fetch_concurrently())
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure 'aiosqlite' is installed (pip install aiosqlite).")
