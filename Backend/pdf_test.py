import mysql.connector
from mysql.connector import Error


def create_pdf_table(connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            #create the table with longblob whichh is large binary object
            cursor.execute("CREATE TABLE IF NOT EXISTS PdfTable (PdfID INT AUTO_INCREMENT PRIMARY KEY, PdfData LONGBLOB)")

            connection.commit()
            print("PdfTable created successfully!")

            cursor.close()

    except Error as e:
        print("Error while creating PdfTable:", e)


def store_pdf_in_database(pdf_folder, connection):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            #From what ive seen you have to iterate over all the pdf's located in the pdfs directory
            #this seems horrible so idk
            for filename in ["dummy1.pdf", "dummy2.pdf", "dummy3.pdf"]: #this i think works only for these 3? idk i have to check
                with open(pdf_folder + "/" + filename, 'rb') as file:
                    pdf_data = file.read()

                #This is to insert the binary data into the pdfdata table made earlier
                cursor.execute("INSERT INTO PdfTable (PdfData) VALUES (%s)", (pdf_data,))

            connection.commit()
            print("PDFs inserted successfully!")

            cursor.close()

    except Error as e:
        print("Error while storing PDFs in the database:", e)

if __name__ == "__main__":
    #This is the pdf folcer that will store the pdfs
    pdf_folder = "pdfs"

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

            #This is where i call the function to store any pdfs into the table from mySQL
            store_pdf_in_database(pdf_folder, connection)

    except Error as e:
        print("Error while connecting to MySQL:", e)
    finally:
        #close it once its done.
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
