
import mysql.connector
from seed import connect_to_prodev

def stream_user_ages():
    """Generates user ages from the database one by one."""
    connection = None
    try:
        connection = connect_to_prodev()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT age FROM user_data")
            for row in cursor:
                yield row['age']
    except mysql.connector.Error as err:
        print(f"Error streaming user ages: {err}")
    finally:
        if connection:
            connection.close()

def calculate_average_age():
    """Calculates the average age of users using the stream_user_ages generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count > 0:
        return total_age / count
    return 0

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")
