import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'ix-dev.cs.uoregon.edu',
    'port': 3056,
    'user': 'group6',
    'password': 'group6',
    'database': 'ara_db'
}

try:
    # Connect to the MySQL server
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)

        # Prompt user for name and message
        name = input("Enter your name: ")
        message = input("Enter your message: ")

        # Get cursor
        cursor = connection.cursor()

        # Execute query to insert data into the Users table
        cursor.execute("INSERT INTO Users (username, message) VALUES (%s, %s)", (name, message))

        # Commit the transaction
        connection.commit()

        print("Message inserted successfully!")

        # Print contents of Users table
        cursor.execute("SELECT * FROM Users")
        rows = cursor.fetchall()
        print("\nContents of Users table:")
        for row in rows:
            print(row)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    # Close database connection
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
