import mysql.connector
from mysql.connector import Error


##
##This file is just for functions like listing what tables are in the database, as well as clearing the database if needed.
##

def clear_pdf_table(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("DELETE FROM PdfTable")
            print("PdfTable cleared successfully.")

            connection.commit()
            cursor.close()

    except Error as e:
        print("Error while clearing PdfTable:", e)

def list_tables(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            if tables:
                print("Existing tables in the database:")
                for table in tables:
                    table_name = table[0]
                    print(f"Table: {table_name}")
                    cursor.execute(f"DESCRIBE {table_name}")
                    columns = cursor.fetchall()
                    print("Attributes:")
                    for column in columns:
                        print(f"\t{column[0]} {column[1]}")
            else:
                print("No tables found in the database.")

            cursor.close()

    except Error as e:
        print("Error while listing tables:", e)


def create_pdf_table(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SHOW TABLES LIKE 'PdfTable'")
            table_exists = cursor.fetchone()

            #create the table with longblob whichh is large binary object

            if table_exists:
                print("PdfTable already exists.")
            else:
                #If the table does not exist
                cursor.execute("CREATE TABLE PdfTable (PdfID INT AUTO_INCREMENT PRIMARY KEY, PdfData LONGBLOB, Filename VARCHAR(255))")
                print("PdfTable created successfully!")


            connection.commit()
            cursor.close()

    except Error as e:
        print("Error while creating PdfTable:", e)

def list_pdf_table_filename(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("SELECT Filename FROM PdfTable")
            pdf_data = cursor.fetchall()

            if pdf_data:
                print("Data in PdfTable:")
                for row in pdf_data:
                    filename = row[0]  # Extracting the filename from the row
                    print(filename)
            else:
                print("PdfTable is empty.")

            cursor.close()

    except Error as e:
        print("Error while listing PdfTable data:", e)

    except Error as e:
        print("Error while listing PdfTable data:", e)

if __name__ == "__main__":
    #This is the pdf folcer that will store the pdfs

    #NEED TO CHANGE THIS
    pdf_folder = "Backend\pdfs" #had to do horrible blackslashes for this to work

    #for this from connections.py, not sure if i need it here
    db_config = {
        'host': 'ix-dev.cs.uoregon.edu',
        'port': 3056,
        'user': 'group6',
        'password': 'group6',
        'database': 'ara_db'
    }

    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print("Connected to MySQL Server")

            #clear_pdf_table(connection)
            list_tables(connection)
            list_pdf_table_filename(connection)
  

            #This is where i call the function to store any pdfs into the table from mySQL

    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        #close it once its done.
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")