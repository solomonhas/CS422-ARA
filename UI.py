import tkinter as tk
from tkinter import Button, Entry, Toplevel, Label
import database
import fitz #pymuPDF
import sys
import tkinter.messagebox as messagebox
import mysql.connector


class ServerLogin:
    def __init__(self, root, on_login_success):
        """initialize the serverlogin class."""
        self.root = root
        self.root.configure(highlightbackground="blue")
        self.root.minsize(400, 200)
        self.root.title("server login")

        # labels
        self.host_label = Label(self.root, text="host:")
        self.host_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.port_label = Label(self.root, text="port:")
        self.port_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.username_label = Label(self.root, text="username:")
        self.username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.password_label = Label(self.root, text="password:")
        self.password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        # entry fields
        self.host_textbox = Entry(self.root)
        self.host_textbox.insert(0, 'ix-dev.cs.uoregon.edu')  # fill in the host field
        self.host_textbox.grid(row=0, column=1, padx=10, pady=5)

        self.port_textbox = Entry(self.root)
        self.port_textbox.insert(0, '3056')  # fill in the port field
        self.port_textbox.grid(row=1, column=1, padx=10, pady=5)

        self.username_textbox = Entry(self.root)
        self.username_textbox.insert(0, 'group6')  # fill in the username field
        self.username_textbox.grid(row=2, column=1, padx=10, pady=5)

        self.password_textbox = Entry(self.root)
        self.password_textbox.insert(0, 'group6')  # fill in the password field
        self.password_textbox.grid(row=3, column=1, padx=10, pady=5)

        self.enter_button = Button(self.root, text="login", command=self.login_server)
        self.enter_button.grid(row=4, columnspan=2, pady=10)

        self.on_login_success = on_login_success

    def login_server(self):
        """attempt to login to the server."""
        host = self.host_textbox.get()
        port = self.port_textbox.get()
        username = self.username_textbox.get()
        password = self.password_textbox.get()

        # convert port to an integer
        try:
            port = int(port)
        except ValueError:
            messagebox.showerror("error", "port must be an integer.")
            return

        # check if any of the fields are empty
        if not all([host, username, password]):
            messagebox.showerror("error", "please fill in all fields.")
            return

        # attempt to connect to the mysql server for authentication
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password
            )
            conn.close()  # close the connection if successful
        except mysql.connector.Error as e:
            messagebox.showerror("authentication error", "failed to authenticate. please check your credentials.")
            return

        # pass the server credentials to the on_login_success callback
        self.on_login_success(host, port, username, password)


class LoginScreen:
    def __init__(self, root):
        """initialize the loginscreen class."""
        self.root = root
        self.root.configure(highlightbackground="red")
        self.root.minsize(400, 200)
        self.root.title("group 6 ara")
        self.show_login()

    def show_login(self):
        """display the login screen."""
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        self.username_label = tk.Label(self.login_frame, text="username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = Entry(self.login_frame)
        self.username_entry.insert(0, 'admin')  # default username
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.insert(0, 'admin')  # default password
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.error_label = tk.Label(self.login_frame, text="", fg="red")
        self.error_label.grid(row=2, columnspan=2, padx=5, pady=5)

        self.login_button = Button(self.login_frame, text="login", command=self.login)
        self.login_button.grid(row=3, columnspan=2, padx=5, pady=5)

    def login(self):
        """validate the login credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        # validate username and password (add your validation logic here)
        if username == "admin" and password == "admin":
            self.show_server_login()
        else:
            self.error_label.config(text="invalid username or password.")

    def show_server_login(self):
        """show the server login screen."""
        self.login_frame.destroy()  # destroy the login frame
        self.server_login = ServerLogin(self.root, self.show_main_window)

    def show_main_window(self, host, port, username, password):
        """show the main window."""
        self.root.withdraw()  # hide the login screen window
        self.main_window = HomeScreen("blank_user", self.root, host, port, username,
                                      password)  # pass the server login window root


class HomeScreen:
    def __init__(self, userid, login_root, host, port, username, password):
        """initialize the homescreen class."""
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
        self.db_manager.build_pdf_table()
        pdf_locations = self.db_manager.get_pdf_locations()

        for i, pdf_location in enumerate(pdf_locations):
            pdf_button = Button(self.root, text=f"pdf {i + 1}", height=1, width=1, padx=30, pady=30,
                                command=lambda loc=pdf_location: self.open_pdf_viewer(loc))
            pdf_button.pack(pady=10)

        back_button = Button(self.root, text="back", command=self.back_to_login)
        back_button.pack(pady=30)
        self.root.protocol("wm_delete_window", self.on_closing)

    def back_to_login(self):
        """navigate back to the login screen."""
        self.root.destroy()
        self.login_root.deiconify()
        self.db_manager.delete_pdf_entries()

    def open_pdf_viewer(self, pdf_location_var):
        """open a pdf viewer."""
        viewer = Toplevel(self.root)
        viewer.title(pdf_location_var)

        back_button = Button(viewer, text="back", command=viewer.destroy)
        back_button.pack()

        # open pdf using pymupdf
        pdf_document = fitz.open(pdf_location_var)
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            image = page.get_pixmap()
            photo = tk.PhotoImage(data=image.tobytes("ppm"))
            label = Label(viewer, image=photo)
            label.image = photo
            label.pack()

    def on_closing(self):
        """handle closing the window."""
        self.root.destroy()
        self.db_manager.delete_pdf_entries()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    root.login_screen = LoginScreen(root)
    root.mainloop()
