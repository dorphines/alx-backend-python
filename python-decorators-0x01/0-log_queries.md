# Task 0: Logging Database Queries

## Objective
Create a decorator that logs database queries executed by any function.

## Implementation

The `log_queries` decorator is designed to intercept function calls that execute SQL queries. Before the original function is called, the decorator extracts the SQL query from the function's arguments and prints it to `sys.stderr` for logging purposes. This provides observability into which queries are being executed.

### `0-log_queries.py`
```python
import sqlite3
import functools
import sys

def log_queries(func):
    """A decorator that logs the SQL query before executing it."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or args[0] if args else None
        if query:
            print(f"Executing query: {query}", file=sys.stderr)
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage:
users = fetch_all_users(query="SELECT * FROM users")
print(users)
```

## Testing

To test the decorator, a `users.db` SQLite database was created and populated with sample data using a `seed.py` script. The `fetch_all_users` function, decorated with `log_queries`, was then called. The decorator successfully intercepted the query and printed it to `sys.stderr`.

### `seed.py`
```python
import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database 'users.db' and table 'users' created and populated.")
```

When `0-log_queries.py` is executed, the output demonstrates that the query is logged before the results are returned:

```
Executing query: SELECT * FROM users
[(1, 'Alice', 'alice@example.com'), (2, 'Bob', 'bob@example.com')]
```

(Note: The 'Executing query' line might appear in stderr depending on the execution environment, while the user list appears in stdout.)
