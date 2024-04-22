import mysql.connector
from mysql.connector import Error

import os

##
##This file is soley to send pdfs from Backend/pdfs to a table in MySQL called PdfTable
##This can be used by placing pdfs you want in the table in the Backend/pdfs
##
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


def store_pdf_in_database(pdf_folder, connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            for filename in os.listdir(pdf_folder):
                if filename.endswith(".pdf"):
                    with open(os.path.join(pdf_folder, filename), 'rb') as file:
                        pdf_data = file.read()

                    cursor.execute("SELECT COUNT(*) FROM PdfTable WHERE Filename = %s", (filename,))
                    count = cursor.fetchone()[0]

                    if count == 0:  # PDF with same filename not found in the database, insert it
                        cursor.execute("INSERT INTO PdfTable (PdfData, Filename) VALUES (%s, %s)", (pdf_data, filename))
                        print(f"Inserted {filename} into the database.")
                    else:
                        print(f"{filename} already in the table, not adding.")

            connection.commit()
            print("Insert to database successful")

            cursor.close()
            connection.close()

    except Error as e:
        print("Error while storing PDFs in the database:", e)



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

            create_pdf_table(connection)  #create the table


            #This is where i call the function to store any pdfs into the table from mySQL
            store_pdf_in_database(pdf_folder, connection)

    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        #close it once its done.
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
