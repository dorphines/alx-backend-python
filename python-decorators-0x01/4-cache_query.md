# Task 4: Using Decorators to Cache Database Queries

## Objective
Create a decorator that caches the results of database queries to avoid redundant calls.

## Implementation

The `cache_query` decorator optimizes database performance by storing the results of SQL queries in an in-memory cache (`query_cache`). When a decorated function is called, the decorator first checks if the query already exists in the cache. If so, it returns the cached result, avoiding a database round-trip. Otherwise, it executes the query, stores the result in the cache, and then returns the result.

This task also reuses the `with_db_connection` decorator from Task 1 to handle database connection management.

### `4-cache_query.py`
```python
import time
import sqlite3
import functools

query_cache = {}

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

def cache_query(func):
    """A decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("Fetching from cache")
            return query_cache[query]
        else:
            print("Fetching from database")
            result = func(conn, query)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
print("First call:")
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
print("\nSecond call:")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
```

## Testing

The `fetch_users_with_cache` function is called twice with the same SQL query. The output demonstrates the caching mechanism:

```
First call:
Fetching from database
[(1, 'Alice', 'Crawford_Cartwright@hotmail.com'), (2, 'Bob', 'bob@example.com')]

Second call:
Fetching from cache
[(1, 'Alice', 'Crawford_Cartwright@hotmail.com'), (2, 'Bob', 'bob@example.com')]
```

On the first call, the decorator fetches the data from the database and stores it in the cache. On the second call, it retrieves the data directly from the cache, which is significantly faster and reduces the load on the database.

```