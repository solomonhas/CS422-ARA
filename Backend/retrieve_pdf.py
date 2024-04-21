import mysql.connector
from mysql.connector import Error
import os

def retrieve_pdfs_from_database(connection, output_folder):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            #Pick the pdf storing table
            cursor.execute("SELECT PdfData FROM PdfTable")

            #get the rows of the table
            pdf_rows = cursor.fetchall()

            #Not sure if this is allowed, its makedirs for making the directory for the pdfs once receives
            os.makedirs(output_folder, exist_ok=True)

            #for all the rows in the table recieve the pdf
            for index, pdf_data in enumerate(pdf_rows):
                filename = f"received_pdf_{index + 1}.pdf"
                output_path = os.path.join(output_folder, filename) #add the path of the directory to store the pdfs
                with open(output_path, 'wb') as file:
                    file.write(pdf_data[0])

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