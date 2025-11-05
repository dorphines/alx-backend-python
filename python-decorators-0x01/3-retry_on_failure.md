# Task 3: Using Decorators to Retry Database Queries

## Objective
Create a decorator that retries database operations if they fail due to transient errors.

## Implementation

The `retry_on_failure` decorator enhances the resilience of database operations by automatically re-attempting a function call a specified number of times if it encounters an exception. This is particularly useful for transient errors (e.g., temporary network issues, database locks) that might resolve themselves after a short delay.

This task also reuses the `with_db_connection` decorator from Task 1 to handle database connection management.

### `3-retry_on_failure.py`
```python
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
```

## Testing

The `fetch_users_with_retry` function is decorated with `retry_on_failure` to simulate a transient database error. The function is designed to fail on its first two attempts and succeed on the third. The output demonstrates the retry mechanism in action:

```
Attempt 1/3 failed: Database locked (simulated transient error)
Attempt 2/3 failed: Database locked (simulated transient error)
[(1, 'Alice', 'Crawford_Cartwright@hotmail.com'), (2, 'Bob', 'bob@example.com')]
```

This output confirms that the `retry_on_failure` decorator successfully retried the function after the simulated failures and eventually succeeded in fetching the user data, thus enhancing the robustness of the database operation.
