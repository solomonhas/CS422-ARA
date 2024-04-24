import mysql.connector
import os


class DatabaseManager:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect_to_database()

    #  connect to the mysql database
    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database!")
            return connection
        except mysql.connector.Error as err:
            print("Error connecting to MySQL:", err)
            return None

    # create the pdf_table and insert pdfs
    def build_pdf_table(self):
        pdf_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfs")
        os.chdir(pdf_directory)
        pdf_names = [filename for filename in os.listdir() if filename != "dummy"]
        pdf_names.sort()
        file_data = [(i + 1, pdf_name, os.path.join(pdf_directory, pdf_name)) for i, pdf_name in enumerate(pdf_names)]
        if self.connection:
            try:
                cursor = self.connection.cursor()
                insert_query = "INSERT INTO pdf_table (pdf_id, pdf_name, pdf_location) VALUES (%s, %s, %s)"
                cursor.executemany(insert_query, file_data)
                self.connection.commit()
                print("PDFs loaded successfully!")
            except mysql.connector.Error as err:
                print("Error loading PDFs:", err)
                self.connection.rollback()
            finally:
                cursor.close()
        else:
            print("No database connection.")

    # delete all entries from pdf_table
    def delete_pdf_entries(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                delete_query = "DELETE FROM pdf_table"
                cursor.execute(delete_query)
                self.connection.commit()
                print("All PDF entries deleted successfully!")
            except mysql.connector.Error as err:
                print("Error deleting PDF entries:", err)
                self.connection.rollback()
            finally:
                cursor.close()

    # get the pdf_id for a given pdf_name
    def get_pdf_id(self, pdf_name):
        select_data = (pdf_name,)
        if self.connection:
            try:
                cursor = self.connection.cursor()
                select_query = "SELECT pdf_id FROM pdf_table WHERE pdf_name = %s"
                cursor.execute(select_query, select_data)
                result = cursor.fetchone()
                if result:
                    pdf_id = result[0]
                    return pdf_id
                else:
                    print("PDF not found in the database.")
                    return None
            except mysql.connector.Error as err:
                print("Error retrieving PDF ID:", err)
                return None
            finally:
                cursor.close()
        else:
            print("No database connection.")
            return None

    def get_pdf_locations(self):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT pdf_location FROM pdf_table"
                cursor.execute(select_query)
                results = cursor.fetchall()
                if results:
                    pdf_locations = [row[0] for row in results]
                    return pdf_locations
                else:
                    print("No PDF locations found in the database.")
                    return []
        except mysql.connector.Error as err:
            print("Error fetching PDF locations:", err)
            return []
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    # add a new note to the database
    def add_note(self, pdf_id, note_text):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                insert_query = "INSERT INTO notes (pdf_id, note) VALUES (%s, %s)"
                insert_data = (pdf_id, note_text)
                cursor.execute(insert_query, insert_data)
                self.connection.commit()
                print("Note added successfully!")
            except mysql.connector.Error as err:
                print("Error adding note:", err)
                self.connection.rollback()
            finally:
                cursor.close()

    # update the text of a note in the database by note_id
    def delete_note(self, note_id):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                delete_query = "DELETE FROM notes WHERE note_id = %s"
                cursor.execute(delete_query, (note_id,))
                self.connection.commit()
                print("Note deleted successfully!")
            except mysql.connector.Error as err:
                print("Error deleting note:", err)
                self.connection.rollback()
            finally:
                cursor.close()

    # display the text of a note from the database by note_id
    def update_note(self, note_id, new_note_text):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                update_query = "UPDATE notes SET note = %s WHERE note_id = %s"
                update_data = (new_note_text, note_id)
                cursor.execute(update_query, update_data)
                self.connection.commit()
                print("Note updated successfully!")
            except mysql.connector.Error as err:
                print("Error updating note:", err)
                self.connection.rollback()
            finally:
                cursor.close()

    # display the text of a note from the database by note_id
    def display_note(self, pdf_id):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT note FROM notes WHERE pdf_id = %s"
                cursor.execute(select_query, (pdf_id,))
                results = cursor.fetchall()
                if results:
                    for result in results:
                        note_text = result[0]
                        print("Note:")
                        print(note_text)
                        return note_text
                else:
                    print("No notes found for the given PDF.")
                    return None
        except mysql.connector.Error as err:
            print("Error fetching notes:", err)
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    # check if a note exists for a given pdf_id and note_text
    def note_exists(self, pdf_id, note_text):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT COUNT(*) FROM notes WHERE pdf_id = %s AND note = %s"
                cursor.execute(select_query, (pdf_id, note_text))
                count = cursor.fetchone()[0]
                if count > 0:
                    print("Note already exists for the given PDF.")
                    return True
                else:
                    print("Note does not exist for the given PDF.")
                    return False
        except mysql.connector.Error as err:
            print("Error checking if note exists:", err)
            return False
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

db_manager = DatabaseManager(
    host='ix-dev.cs.uoregon.edu',
    port=3056,
    user='group6',
    password='group6',
    database='ara_db'
)
"""
How it works:

When adding a new note, you provide it with a PDF ID, which associates the note with a specific PDF.

In the notes table, there is a column that holds PDF IDs.

When manipulating the notes, we can use the PDF ID to filter the notes. We can use the "check if exists" function to see if the note already exists using the PDF ID and note text.

Displaying the note retrieves the text based on the PDF ID, which is unique for each PDF.
"""

