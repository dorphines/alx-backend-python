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

#### Update user's email with automatic transaction handling

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



# Verify the update (should be the email before the failed transaction)

user = get_user_by_id(user_id=1)

print(f"User after failed update attempt (should be previous email): {user}")
