import tkinter as tk
from tkinter import Button, Entry, Toplevel, Label, Text
import database
import fitz
import sys
import tkinter.messagebox as messagebox
import os
import mysql.connector

#
class ServerLogin:
    def __init__(self, root, on_login_success):
        """Initialize the ServerLogin class."""
        self.root = root
        self.root.configure(highlightbackground="blue")
        self.root.minsize(400, 200)
        self.root.title("server login")

        # Labels
        self.host_label = Label(self.root, text="host:")
        self.host_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.port_label = Label(self.root, text="port:")
        self.port_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.username_label = Label(self.root, text="username:")
        self.username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.password_label = Label(self.root, text="password:")
        self.password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        # Entry fields
        self.host_textbox = Entry(self.root)
        self.host_textbox.insert(0, 'ix-dev.cs.uoregon.edu')
        self.host_textbox.grid(row=0, column=1, padx=10, pady=5)

        self.port_textbox = Entry(self.root)
        self.port_textbox.insert(0, '3056')
        self.port_textbox.grid(row=1, column=1, padx=10, pady=5)

        self.username_textbox = Entry(self.root)
        self.username_textbox.insert(0, 'group6')
        self.username_textbox.grid(row=2, column=1, padx=10, pady=5)

        self.password_textbox = Entry(self.root)
        self.password_textbox.insert(0, 'group6')
        self.password_textbox.grid(row=3, column=1, padx=10, pady=5)

        # Login button
        self.enter_button = Button(self.root, text="login", command=self.login_server)
        self.enter_button.grid(row=4, columnspan=2, pady=10)

        self.on_login_success = on_login_success

    def login_server(self):
        """Attempt to login to the server."""
        host = self.host_textbox.get()
        port = self.port_textbox.get()
        username = self.username_textbox.get()
        password = self.password_textbox.get()

        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("error", "port must be an integer.")
            return

        if not all([host, username, password]):
            messagebox.showerror("error", "please fill in all fields.")
            return

        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password
            )
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("authentication error", "failed to authenticate. please check your credentials.")
            return

        self.on_login_success(host, port, username, password)


class LoginScreen:
    def __init__(self, root):
        """Initialize the LoginScreen class."""
        self.root = root
        self.root.configure(highlightbackground="red")
        self.root.minsize(400, 200)
        self.root.title("group 6 ara")
        self.show_login()

    def show_login(self):
        """Display the login screen."""
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        self.username_label = tk.Label(self.login_frame, text="username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = Entry(self.login_frame)
        self.username_entry.insert(0, 'admin')
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.insert(0, 'admin')
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.error_label = tk.Label(self.login_frame, text="", fg="red")
        self.error_label.grid(row=2, columnspan=2, padx=5, pady=5)

        self.login_button = Button(self.login_frame, text="login", command=self.login)
        self.login_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def login(self):
        """Validate the login credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin":
            self.show_server_login()
        else:
            self.error_label.config(text="invalid username or password.")

    def show_server_login(self):
        """Show the server login screen."""
        self.login_frame.destroy()
        self.server_login = ServerLogin(self.root, self.show_main_window)

    def show_main_window(self, host, port, username, password):
        """Show the main window."""
        self.root.withdraw()
        self.main_window = HomeScreen("blank_user", self.root, host, port, username,
                                      password)


class HomeScreen:
    def __init__(self, userid, login_root, host, port, username, password):
        """Initialize the HomeScreen class."""
        self.login_root = login_root
        self.root = tk.Toplevel(login_root)
        self.root.minsize(600, 400)
        self.root.title("group 6 ara")

        self.db_manager = database.DatabaseManager(
            host=host,
            port=int(port),
            user=username,
            password=password,
            database='ara_db'
        )
        self.db_manager.update_pdf_locations()
        pdf_locations = self.db_manager.get_pdf_locations()

        for i, pdf_location in enumerate(pdf_locations):
            pdf_button = Button(self.root, text=f"pdf {i + 1}", height=1, width=1, padx=30, pady=30,
                                command=lambda loc=pdf_location: self.open_pdf_viewer(loc))
            pdf_button.pack(pady=10)

        back_button = Button(self.root, text="back", command=self.back_to_login)
        back_button.pack(pady=30)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def back_to_login(self):
        """Navigate back to the login screen."""
        self.root.destroy()
        self.login_root.deiconify()

    def open_pdf_viewer(self, pdf_location_var):
        """Open a PDF viewer."""
        viewer = Toplevel(self.root)
        viewer.title(pdf_location_var)

        canvas = tk.Canvas(viewer)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(viewer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        pdf_document = fitz.open(pdf_location_var)

        pdf_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=pdf_frame, anchor="nw")

        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            image = page.get_pixmap()
            photo = tk.PhotoImage(data=image.tobytes("ppm"))
            label = Label(pdf_frame, image=photo)
            label.image = photo
            label.pack()

        pdf_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_canvas_configure)

        notes_frame = tk.Frame(viewer)
        notes_frame.pack(side="right", fill="y")

        note_name_label = Label(notes_frame, text="Note Name:")
        note_name_label.pack()
        note_name_entry = Entry(notes_frame)
        note_name_entry.pack()

        pdf_name = os.path.basename(pdf_location_var)
        pdf_id = self.db_manager.get_pdf_id(pdf_name)
        note_text = self.db_manager.display_note(pdf_id)

        notes_label = Label(notes_frame, text="Notes")
        notes_label.pack()

        notes_text = Text(notes_frame, wrap=tk.WORD, height=20, width=40)
        notes_text.insert(tk.END, note_text if note_text else "No notes available")
        notes_text.pack()

        add_note_button = Button(notes_frame, text="Add Note", command=lambda: self.add_note_to_db(pdf_id, note_name_entry.get(), notes_text))
        add_note_button.pack()

        delete_note_button = Button(notes_frame, text="Delete Note", command=lambda: self.delete_note_from_db(pdf_id))
        delete_note_button.pack()

        back_button = Button(viewer, text="Back", command=viewer.destroy)
        back_button.pack()

    def add_note_to_db(self, pdf_id, note_name, notes_text):
        """Add a note to the database."""
        note_text = notes_text.get("1.0", tk.END).strip()
        if note_text:
            self.db_manager.add_note(pdf_id, note_name, note_text)
            messagebox.showinfo("Note Added", "Note added successfully!")
        else:
            messagebox.showwarning("Empty Note", "Please enter some text for the note.")

    def delete_note_from_db(self, pdf_id):
        """Delete a note from the database."""
        confirmation = messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?")
        if confirmation:
            self.db_manager.delete_note(pdf_id)
            messagebox.showinfo("Note Deleted", "Note deleted successfully!")

    def on_closing(self):
        """Handle closing the window."""
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    root.login_screen = LoginScreen(root)
    root.mainloop()
