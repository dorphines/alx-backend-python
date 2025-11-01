
import mysql.connector
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """Generates user data from the database in batches."""
    connection = None
    try:
        connection = connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            offset = 0
            while True:
                cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {batch_size} OFFSET {offset}")
                batch = cursor.fetchall()
                if not batch:
                    break
                yield batch
                offset += batch_size
    except mysql.connector.Error as err:
        print(f"Error streaming users in batches: {err}")
    finally:
        if connection:
            connection.close()

def batch_processing(batch_size):
    """Processes each batch to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user

