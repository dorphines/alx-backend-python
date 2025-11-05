# Task 2: Transaction Management Decorator

## Objective
Create a decorator that manages database transactions by automatically committing or rolling back changes.

## Implementation

The `transactional` decorator ensures that a series of database operations within a function are treated as a single atomic unit. If all operations succeed, the changes are committed to the database. If any operation fails (raises an exception), all changes made within that transaction are rolled back, maintaining data integrity.

This task also reuses the `with_db_connection` decorator from Task 1 to handle database connection management.

### `2-transactional.py`
```python
import sqlite3
import functools

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

def transactional(func):
    """A decorator that manages database transactions (commit/rollback)."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage and testing of rollback:
print("Attempting to update email to Crawford_Cartwright@hotmail.com (should commit)")
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
user = get_user_by_id(user_id=1)
print(f"User after successful update: {user}")

print("\nAttempting to update email to rollback@example.com (should rollback due to error)")
try:
    @with_db_connection
    @transactional
    def update_user_email_with_error(conn, user_id, new_email):
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        raise ValueError("Simulating an error to test rollback")
    update_user_email_with_error(user_id=1, new_email='rollback@example.com')
except ValueError as e:
    print(f"Caught expected error: {e}")

user = get_user_by_id(user_id=1)
print(f"User after failed update attempt (should be previous email): {user}")
```

## Testing

The script first successfully updates a user's email, demonstrating a committed transaction. Then, it attempts another update with a simulated `ValueError`. The `transactional` decorator catches this error, performs a rollback, and re-raises the exception. A subsequent fetch of the user confirms that the email address reverted to its state before the failed transaction, proving the rollback mechanism works.

```
Attempting to update email to Crawford_Cartwright@hotmail.com (should commit)
User after successful update: (1, 'Alice', 'Crawford_Cartwright@hotmail.com')

Attempting to update email to rollback@example.com (should rollback due to error)
Caught expected error: Simulating an error to test rollback
User after failed update attempt (should be previous email): (1, 'Alice', 'Crawford_Cartwright@hotmail.0com')
```
