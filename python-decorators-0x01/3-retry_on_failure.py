import time
import sqlite3
import functools
import sys

def with_db_connection(func):
    """A decorator that automatically handles opening and closing database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=1):
    """A decorator that retries a function a certain number of times if it raises an exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {i + 1}/{retries} failed: {e}", file=sys.stderr)
                    if i < retries - 1:
                        time.sleep(delay)
            raise # Re-raise the last exception if all retries fail
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    # Simulate a transient error on the first two attempts
    if not hasattr(fetch_users_with_retry, 'attempts'):
        fetch_users_with_retry.attempts = 0
    fetch_users_with_retry.attempts += 1

    if fetch_users_with_retry.attempts < 3:
        raise sqlite3.OperationalError("Database locked (simulated transient error)")

    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)
