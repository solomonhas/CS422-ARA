import tkinter as tk
from tkinter import Button, Entry, Toplevel
import database
from tkPDFViewer import tkPDFViewer as pdf

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.configure(highlightbackground="red")
        self.root.minsize(400, 200)
        self.root.title("Group 6 ARA")

        self.username_textbox = Entry(self.root, text="Username:")
        self.username_textbox.pack(padx=10, pady=20)

        self.password_textbox = Entry(self.root, text="Password:")
        self.password_textbox.pack(padx=10, pady=10)

        self.enter_button = Button(self.root, text="Enter", command=self.retrieve_input)
        self.enter_button.pack()

    def nextWindow(self):
        self.root.withdraw()
        HomeScreen("Blank_User", self.root)

    def retrieve_input(self):
        username = self.username_textbox.get()
        password = self.password_textbox.get()
        if (username == " " and password == " ") or (username == "1"):
            self.nextWindow()
        else:
            print("Incorrect Password")

class HomeScreen:
    def __init__(self, userid, root):
        self.root = Toplevel(root)
        self.root.minsize(600, 400)
        self.root.title("Group 6 ARA")

        self.db_manager = database.DatabaseManager(
            host='ix-dev.cs.uoregon.edu',
            port=3056,
            user='group6',
            password='group6',
            database='ara_db'
        )
        # build PDF table and retrieve PDF locations
        self.db_manager.build_pdf_table()

        pdf_locations = self.db_manager.get_pdf_locations()

        # create buttons for each PDF location
        for i, pdf_location in enumerate(pdf_locations):
            pdf_button = Button(self.root, text=f"PDF {i + 1}", height=1, width=1, padx=30, pady=30,
                                command=lambda loc=pdf_location: self.open_pdf_viewer(loc))
            pdf_button.pack(pady=10)
        # create back button
        back_button = Button(self.root, text="Back", command=self.back_to_login)
        back_button.pack(pady=30)
        # configure close window event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # destroy the home screen and show the login window
    def back_to_login(self):
        self.root.destroy()
        self.root.master.deiconify()

        # open PDF viewer for the selected PDF location
    def open_pdf_viewer(self, pdf_location_var):
        viewer = Toplevel(self.root)
        viewer.title(pdf_location_var)

        back_button = Button(viewer, text="Back", height=1, width=1, padx=100, command=viewer.destroy)
        back_button.pack()

        v1 = pdf.ShowPdf()
        v2 = v1.pdf_view(viewer, pdf_location=pdf_location_var, width=77, height=77)
        v2.pack(pady=10, padx=10)

    # destroy the home screen and delete PDF entries from the database
    def on_closing(self):
        self.root.destroy()
        self.db_manager.delete_pdf_entries()

if __name__ == "__main__":
    root = tk.Tk()  # creates the main window
    login_screen = LoginScreen(root)
    root.mainloop()
