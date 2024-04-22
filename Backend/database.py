import mysql.connector
from mysql.connector import Error
import os


db_config = {
    'host': 'ix-dev.cs.uoregon.edu',
    'port': 3056,
    'user': 'group6',
    'password': 'group6',
    'database': 'ara_db'
}
"""

This handles each chapter by giving it an 
Id and name for each chapter
ID auto incraments

CREATE TABLE Chapters (
    chapter_id INT AUTO_INCREMENT PRIMARY KEY,
    chapter_name VARCHAR(255) NOT NULL
);

This handles the chapter notes
this gives a note id that incraments
a chapter ID that is linked to the Chapters Table

CREATE TABLE ChapterNotes (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    chapter_id INT,
    note_file_path VARCHAR(255),
    FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id)


This table handles the PDFs 
CREATE TABLE PdfTable (
    PdfID INT AUTO_INCREMENT PRIMARY KEY,
    PdfData LONGBLOB,
    Filename VARCHAR(255)
);
    
    
);

"""

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

# call for pdfs retrieve_pdfs_from_database(connection, output_folder)


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

# pdf_folder = "Backend\pdfs" had to do horrible blackslashes for this to work
# call to create Pdfs  create_pdf_table(connection)
# Call to store the pdfs  store_pdf_in_database(pdf_folder, connection)

"""
def insert_chapter(chapter_name):

def insert_chapter_note(chapter_id, note_file_path, pdf_id=None):

insert_chapter("Chapter 1")
chapter_id = 1
insert_chapter_note(chapter_id, "path_to_note.txt", pdf_id=1)

Insert a new chapter named Chapter 1 using insert_chapter.
Retrieve the chapter_id corresponding to Chapter 1 from the Chapters table.
If the chapter_id is found, use it to insert a new chapter note for Chapter 1 using insert_chapter_note.
If the chapter_id is not found, print a message indicating that the chapter was not found

"""