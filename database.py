import mysql.connector
import os

class DatabaseManager:
    def __init__(self, host=None, port=None, user=None, password=None, database=None):
        # Initializing the DatabaseManager class with optional parameters for database credentials
        # If not provided, attempt to load from environment variables
        # If still not available, raise a ValueError
        if host is None or port is None or user is None or password is None or database is None:
            host = os.getenv('DB_HOST')
            port = os.getenv('DB_PORT')
            user = os.getenv('DB_USER')
            password = os.getenv('DB_PASSWORD')
            database = os.getenv('DB_DATABASE')

        if host is None or port is None or user is None or password is None or database is None:
            raise ValueError("Database credentials not provided and could not be loaded from configuration file or environment variables.")

        # Assigning the provided or loaded database credentials to class attributes
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        # Attempting to establish a connection to the database upon initialization
        self.connection = self.connect_to_database()

    def connect_to_database(self):
        # Method to establish a connection to the MySQL database
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

    def build_pdf_table(self):
        # Method to populate the PDF table in the database with PDF file locations
        # Retrieves PDF file names from a directory, constructs file paths, and inserts into the database
        pdf_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfs")
        highlighted_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "highlighted")

        pdf_names = [filename for filename in os.listdir(pdf_directory) if filename != "Chapter"]
        pdf_names.sort()

        highlighted_names = [filename for filename in os.listdir(highlighted_directory) if filename != "Chapter"]
        highlighted_names.sort()

        if self.connection:
            try:
                cursor = self.connection.cursor()
                for pdf_name, highlighted_name in zip(pdf_names, highlighted_names):
                    pdf_location = os.path.join(pdf_directory, pdf_name)
                    highlighted_location = os.path.join(highlighted_directory, highlighted_name)

                    insert_query = "INSERT INTO pdf_table (pdf_name, pdf_location, highlighted_pdf_location) VALUES (%s, %s, %s)"
                    insert_data = (pdf_name, pdf_location, highlighted_location)
                    cursor.execute(insert_query, insert_data)

                self.connection.commit()
                print("PDFs loaded successfully!")
            except mysql.connector.Error as err:
                print("Error loading PDFs:", err)
                self.connection.rollback()
            finally:
                cursor.close()
        else:
            print("No database connection.")

    def update_pdf_locations(self):
        # Method to update PDF file locations in the database
        # Retrieves current PDF locations, constructs updated paths, and updates database entries
        try:
            if self.connection:
                cursor = self.connection.cursor()
                pdf_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfs")
                highlighted_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "highlighted")

                pdf_names = [filename for filename in os.listdir(pdf_directory) if filename != "Chapter"]
                pdf_names.sort()

                for pdf_name in pdf_names:
                    pdf_location = os.path.join(pdf_directory, pdf_name)
                    highlighted_location = os.path.join(highlighted_directory, pdf_name)

                    update_query = "UPDATE pdf_table SET pdf_location = %s, highlighted_pdf_location = %s WHERE pdf_name = %s"
                    update_data = (pdf_location, highlighted_location, pdf_name)
                    cursor.execute(update_query, update_data)

                self.connection.commit()
                print("PDF locations updated successfully!")
        except mysql.connector.Error as err:
            print("Error updating PDF locations:", err)
            self.connection.rollback()
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    def delete_pdf_entries(self):
        # Method to delete all entries in the PDF table from the database
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

    def get_pdf_id(self, pdf_name):
        # Method to retrieve the ID of a PDF from the database based on its name
        select_data = (pdf_name,) #Get the data aka the name 
        if self.connection:
            try:
                cursor = self.connection.cursor()
                select_query = "SELECT pdf_id FROM pdf_table WHERE pdf_name = %s" #get pdf_id
                cursor.execute(select_query, select_data)
                result = cursor.fetchone()
                if result:
                    pdf_id = result[0] #if it exists return the pdf_id
                    return pdf_id
                else:
                    print("PDF not found in the database.") #If you dont find the pdf_id in the table, its not in the databse
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
        # Method to retrieve all PDF locations from the database
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT pdf_location FROM pdf_table" #same as id but for location
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

    def get_highlighted_pdfs(self):
        # Method to retrieve all highlighted PDF locations from the database
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT highlighted_pdf_location FROM pdf_table"
                cursor.execute(select_query)
                results = cursor.fetchall()
                if results:
                    highlighted_pdfs = [row[0] for row in results]
                    return highlighted_pdfs
                else:
                    print("No highlighted PDFs found in the database.")
                    return []
        except mysql.connector.Error as err:
            print("Error fetching highlighted PDFs:", err)
            return []
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    def is_pdf_table_empty(self):
        # Method to check if the PDF table in the database is empty
        #I orginally had this to check the table for debugging but not sure if it is needed still.
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT COUNT(*) FROM pdf_table"
                cursor.execute(select_query)
                count = cursor.fetchone()[0]
                return count == 0
        except mysql.connector.Error as err:
            print("Error checking if PDF table is empty:", err)
            return True
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    def add_note(self, pdf_id, note_name, note_text):
        # Method to add a note to the database for a given PDF
        if self.connection:
            try:
                cursor = self.connection.cursor()

                select_query = "SELECT COUNT(*) FROM notes WHERE pdf_id = %s AND note_name = %s"
                cursor.execute(select_query, (pdf_id, note_name))
                count = cursor.fetchone()[0]

                if count > 0:
                    note_name = f"{note_name}_{count + 1}"

                insert_query = "INSERT INTO notes (pdf_id, note_name, note) VALUES (%s, %s, %s)"
                insert_data = (pdf_id, note_name, note_text)
                cursor.execute(insert_query, insert_data)
                self.connection.commit()
                print("Note added successfully!")
            except mysql.connector.Error as err:
                print("Error adding note:", err)
                self.connection.rollback()
            finally:
                cursor.close()
        else:
            print("No database connection.")

    def delete_note(self, note_id):
        """Delete a note from the database using its ID."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                delete_query = "DELETE FROM notes WHERE note_id = %s" #DELTE FROM, the notes table using the note_id
                                                                      #this will be called sometimes but not much
                cursor.execute(delete_query, (note_id,))
                self.connection.commit()
                print("Note deleted successfully!")
            except mysql.connector.Error as err:
                print("Error deleting note:", err)
                self.connection.rollback()
            finally:
                if cursor is not None:
                    cursor.close()
        else:
            print("No database connection.")

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

    def display_note(self, pdf_id):
        #This function is just to display the note text given the note id
        #note id is linked to pdf id
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

    def note_exists(self, pdf_id, note_text):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT COUNT(*) FROM notes WHERE pdf_id = %s AND note = %s" #
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

    def get_saved_notes(self, pdf_id):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT note_name FROM notes WHERE pdf_id = %s"
                cursor.execute(select_query, (pdf_id,))
                results = cursor.fetchall()
                if results:
                    saved_notes = [row[0] for row in results]
                    return saved_notes
                else:
                    print("No saved notes found for the given PDF.")
                    return []
        except mysql.connector.Error as err:
            print("Error fetching saved notes:", err)
            return []
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    def get_notes(self, pdf_id):
        """Retrieve notes associated with the given PDF ID."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT note_name, note FROM notes WHERE pdf_id = %s"
                cursor.execute(select_query, (pdf_id,))
                results = cursor.fetchall()
                notes = []
                for note_name, note_text in results:
                    # Append only the note name (first element of the tuple) to the list
                    notes.append(note_name)
                return notes
            else:
                print("No database connection.")
                return []
        except mysql.connector.Error as err:
            print("Error fetching notes:", err)
            return []
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    def get_note_text(self, pdf_id, note_name):
        """Retrieve the text of a specific note associated with a PDF."""
        try:
            if self.connection:
                cursor = self.connection.cursor()
                print("Note name:", note_name)  # Add this line to print out the note_name
                select_query = "SELECT note FROM notes WHERE pdf_id = %s AND note_name = %s"
                cursor.execute(select_query, (pdf_id, note_name))
                result = cursor.fetchone()
                if result:
                    note_text = result[0]
                    print("Note text:", note_text)  # Add this line to print out the retrieved note_text
                    return note_text
                else:
                    print("Note not found in the database.")
                    return None
        except mysql.connector.Error as err:
            print("Error fetching note text:", err)
            return None
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    def get_note_id(self, pdf_id, note_name):
        """Retrieve the ID of a specific note associated with a PDF based on the note name."""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                select_query = "SELECT note_id FROM notes WHERE pdf_id = %s AND note_name = %s"
                cursor.execute(select_query, (pdf_id, note_name))
                result = cursor.fetchone()
                if result:
                    note_id = result[0]
                    return note_id
                else:
                    print("Note not found in the database.")
                    return None
            except mysql.connector.Error as err:
                print("Error fetching note ID:", err)
                return None
            finally:
                if cursor is not None:
                    cursor.close()
        else:
            print("No database connection.")
            return None