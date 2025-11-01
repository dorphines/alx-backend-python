# Python Generators

This project introduces advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations. The tasks focus on leveraging Python’s yield keyword to implement generators that provide iterative access to data, promoting optimal resource utilization, and improving performance in data-driven applications.

## Task 0: Getting started with python generators

This task involves setting up a MySQL database, creating a table, and populating it with data from a CSV file.

### Files

*   `seed.py`: This script contains functions to connect to the MySQL database, create the database and table, and insert data from a CSV file.
*   `0-main.py`: This script uses the functions from `seed.py` to set up the database and verify the data insertion.
*   `user_data.csv`: This file contains the sample data to be inserted into the database.

### Usage

To run this project, you need to have MySQL server installed and running. You also need to have the `mysql-connector-python` library installed.

```bash
pip install mysql-connector-python
```

Then you can run the `0-main.py` script:

```bash
python3 0-main.py
```

This will create the `ALX_prodev` database, the `user_data` table, and populate it with the data from the `user_data.csv` file.

## Task 1: Generator that streams rows from an SQL database

This task focuses on creating a Python generator to stream rows from an SQL database one by one, ensuring memory efficiency.

### Files

*   `0-stream_users.py`: Contains the `stream_users()` generator function that fetches rows individually from the `user_data` table.
*   `1-main.py`: A test script to demonstrate the usage of `stream_users()`, printing the first 6 streamed users.

### Usage

Run the `1-main.py` script:

```bash
/home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/venv/bin/python /home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/1-main.py
```

## Task 2: Batch processing Large Data

This task involves creating generators to fetch and process data from the database in batches, optimizing for large datasets.

### Files

*   `1-batch_processing.py`: Contains `stream_users_in_batches(batch_size)` to fetch data in batches and `batch_processing(batch_size)` to filter users over the age of 25 from these batches.
*   `2-main.py`: A test script to demonstrate `batch_processing()`, printing filtered users in batches of 50.

### Usage

Run the `2-main.py` script:

```bash
/home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/venv/bin/python /home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/2-main.py
```

## Task 3: Lazy loading Paginated Data

This task simulates fetching paginated data from the database using a generator that lazily loads each page only when needed.

### Files

*   `2-lazy_paginate.py`: Implements `paginate_users(page_size, offset)` to fetch a specific page and `lazy_paginate(page_size)` as a generator to yield pages on demand.
*   `3-main.py`: A test script to demonstrate `lazy_paginate()`, iterating through all pages and printing users.

### Usage

Run the `3-main.py` script:

```bash
/home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/venv/bin/python /home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/3-main.py
```

## Task 4: Memory-Efficient Aggregation with Generators

This task focuses on using generators to compute memory-efficient aggregate functions, specifically calculating the average age for a large dataset without loading all data into memory.

### Files

*   `4-stream_ages.py`: Contains `stream_user_ages()` to yield individual user ages and `calculate_average_age()` to compute the average using the generator.

### Usage

Run the `4-stream_ages.py` script:

```bash
/home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/venv/bin/python /home/dorfin/alx/repos/alx-airbnb-database/database-adv-script/4-stream_ages.py
```
