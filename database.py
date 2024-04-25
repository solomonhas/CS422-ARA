import mysql.connector
import os
#
class DatabaseManager:
    def __init__(self, host=None, port=None, user=None, password=None, database=None):
        if host is None or port is None or user is None or password is None or database is None:
            host = os.getenv('DB_HOST')
            port = os.getenv('DB_PORT')
            user = os.getenv('DB_USER')
            password = os.getenv('DB_PASSWORD')
            database = os.getenv('DB_DATABASE')

        if host is None or port is None or user is None or password is None or database is None:
            raise ValueError(
                "Database credentials not provided and could not be loaded from configuration file or environment variables.")

        # Store the database credentials
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect_to_database()

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

    def update_pdf_locations(self):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                pdf_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pdfs")
                os.chdir(pdf_directory)
                pdf_names = [filename for filename in os.listdir() if filename != "dummy"]
                pdf_names.sort()
                for i, pdf_name in enumerate(pdf_names):
                    update_query = "UPDATE pdf_table SET pdf_location = %s WHERE pdf_name = %s"
                    update_data = (os.path.join(pdf_directory, pdf_name), pdf_name)
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

    def is_pdf_table_empty(self):
        try:
            if self.connection:
                cursor = self.connection.cursor()
                select_query = "SELECT COUNT(*) FROM pdf_table"
                cursor.execute(select_query)
                count = cursor.fetchone()[0]
                return count == 0
        except mysql.connector.Error as err:
            print("Error checking if PDF table is empty:", err)
            return True  # Assuming an error indicates an empty table
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()

    def add_note(self, pdf_id, note_name, note_text):
        if self.connection:
            try:
                cursor = self.connection.cursor()
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
