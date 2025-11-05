# Python Decorators for Database Operations

This project demonstrates the use of Python decorators to enhance and simplify database operations. Each task introduces a new decorator that adds a specific functionality, such as logging, connection handling, transaction management, retry mechanisms, and caching.

## Tasks

*   [Task 0: Logging Database Queries](./0-log_queries.md)
*   [Task 1: Handle Database Connections with a Decorator](./1-with_db_connection.md)
*   [Task 2: Transaction Management Decorator](./2-transactional.md)
*   [Task 3: Using Decorators to Retry Database Queries](./3-retry_on_failure.md)
*   [Task 4: Using Decorators to Cache Database Queries](./4-cache_query.md)

## Setup

To run the scripts in this project, you need to have a `users.db` SQLite database with a `users` table. You can create and populate this database by running the `seed.py` script:

```bash
python3 seed.py
```
