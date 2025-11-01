
import mysql.connector
from seed import connect_to_prodev

def stream_users():
    """Generates user data from the database one by one."""
    connection = None
    try:
        connection = connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            for row in cursor:
                yield row
    except mysql.connector.Error as err:
        print(f"Error streaming users: {err}")
    finally:
        if connection:
            connection.close()

