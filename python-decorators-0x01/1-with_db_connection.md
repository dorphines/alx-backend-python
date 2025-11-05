# Task 1: Handle Database Connections with a Decorator

## Objective
Create a decorator that automatically handles opening and closing database connections.

## Implementation

The `with_db_connection` decorator simplifies database interactions by abstracting away the connection management. It ensures that a new SQLite connection is established before the decorated function executes and that the connection is properly closed afterward, regardless of whether the function succeeds or raises an error.

### `1-with_db_connection.py`
```python
import sqlite3
import functools

def with_db_connection(func):
    """A decorator that automatically handles opening and closing database connections."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection object as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetches a user by ID using the provided database connection."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Example usage:
user = get_user_by_id(user_id=1)
print(user)
```

## Testing

The `get_user_by_id` function, decorated with `with_db_connection`, was called with `user_id=1`. The script successfully connected to `users.db`, fetched the user, and printed the result, confirming that the decorator correctly managed the database connection.

```
(1, 'Alice', 'alice@example.com')
```
