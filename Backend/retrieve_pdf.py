import mysql.connector
from mysql.connector import Error
import os

##
##This file receives PDFs from the database table in MySQL called PdfTable
##It then places these pdfs with the same name they had when put in the table in a directory called Backend/received_pdfs
##

def retrieve_pdfs_from_database(connection, output_folder):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            #Pick the pdf storing table, i named it PdfTable
            #Also get the filename from the table
            cursor.execute("SELECT PdfData, Filename FROM PdfTable")

            #get the rows of the table
            pdf_rows = cursor.fetchall()

            #Not sure if this is allowed, its makedirs for making the directory for the pdfs once receives
            os.makedirs(output_folder, exist_ok=True)

            #for all the rows in the table recieve the pdf
            for pdf_data, filename in pdf_rows:
                output_path = os.path.join(output_folder, filename)
                with open(output_path, 'wb') as file:
                    file.write(pdf_data)

            print("PDFs retrieved and saved to", output_folder) #console output to show where the pdfs are recieved

            cursor.close()

    except Error as e:
        print("Error while retrieving PDFs from the database:", e)

if __name__ == "__main__":
    output_folder = "Backend/received_pdfs"

    db_config = { #same as the other send_pdf
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

            #this is the call for the pdfs
            retrieve_pdfs_from_database(connection, output_folder)

    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")