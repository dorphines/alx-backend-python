# Context Managers and Asynchronous Programming in Python

This project demonstrates advanced Python techniques for managing database connections and executing queries using context managers and asynchronous programming. It provides implementations for a custom context manager for database connections, a reusable query executor, and concurrent asynchronous database operations.

## Learning Objectives

*   Implement class-based context managers using `__enter__` and `__exit__` methods.
*   Understand resource management and automatic cleanup with context managers.
*   Master asynchronous database operations using `aiosqlite`.
*   Implement concurrent query execution with `asyncio.gather`.
*   Handle database connections and queries in a Pythonic way.

## Tasks Implemented

### 0. Custom Class-Based Context Manager for Database Connection

**Objective**: Create a class-based context manager to handle opening and closing database connections automatically.

**File**: `0-databaseconnection.py`

**Explanation**:

The `DatabaseConnection` class acts as a context manager. The `__enter__` method establishes a connection to an SQLite database and returns a cursor. The `__exit__` method ensures that the database connection is properly closed, even if errors occur during the `with` block.

A `setup_database` function is included to create a sample `users` table and populate it with some data for demonstration purposes.

**How to Run**:

```bash
python3 0-databaseconnection.py
```

This script will set up a `test_database.db`, open a connection, execute a `SELECT * FROM users` query, print the results, and then close the connection, demonstrating the automatic resource management of the context manager.

### 1. Reusable Query Context Manager

**Objective**: Create a reusable context manager that takes a query as input and executes it, managing both connection and query execution.

**File**: `1-execute.py`

**Explanation**:

The `ExecuteQuery` class is a context manager that leverages the `DatabaseConnection` to execute a given SQL query with optional parameters. The `__enter__` method performs the query and fetches all results, which are then returned. The `__exit__` method handles any exceptions during query execution.

This task reuses the `DatabaseConnection` class and `setup_database` function (with minor adjustments to `setup_database` to add more sample data) to ensure a consistent database environment.

**How to Run**:

```bash
python3 1-execute.py
```

This script will demonstrate executing queries with and without parameters using the `ExecuteQuery` context manager, printing the fetched results.

### 2. Concurrent Asynchronous Database Queries

**Objective**: Run multiple database queries concurrently using `asyncio.gather`.

**File**: `3-concurrent.py`

**Explanation**:

This task utilizes the `aiosqlite` library for asynchronous interaction with an SQLite database. It defines two asynchronous functions: `async_fetch_users` to fetch all users and `async_fetch_older_users` to fetch users older than 40. The `fetch_concurrently` function uses `asyncio.gather` to run these two functions concurrently, significantly improving performance for independent database operations.

A `setup_async_database` function is provided to prepare the database for asynchronous operations.

**Prerequisites**:

Before running, ensure `aiosqlite` is installed. If not, you can install it using pip:

```bash
python3 -m venv venv_async_db
source venv_async_db/bin/activate
pip install aiosqlite
```

**How to Run**:

```bash
source venv_async_db/bin/activate
python3 3-concurrent.py
```

This script will set up an asynchronous database, then concurrently fetch all users and users older than 40, printing the results from both operations.
