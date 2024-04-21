import tkinter as tk
from tkinter import *

import tkPDFViewer as pdf 



class LoginScreen:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.minsize(400,200)
        self.root.title("Group 6 ARA")

        self.username_textbox = tk.Entry(self.root)
        self.username_textbox.pack(padx=10,pady=20)

        self.password_textbox = tk.Entry(self.root)
        self.password_textbox.pack(padx=10,pady=10)

        self.enter_button = Button(self.root, text="Enter", command=self.retrieve_input)
        self.enter_button.pack()

        self.root.mainloop()

    def nextWindow(self):
        self.root.destroy()
        HomeScreen("Blank_User")

    def retrieve_input(self):
        username = tk.StringVar
        password = tk.StringVar
        username = self.username_textbox.get()
        password = self.password_textbox.get()
        if (username == "Admin" and password == "Admin") or (username == "1"):
            self.nextWindow()
            return username and password
        else:
            print("Incorrect Password")
            return username and password

class HomeScreen(object):
    def __init__(self, userid):
        self.root = tk.Tk()
        self.root.minsize(600,400)
        self.root.title("Group 6 ARA")

        print(userid) #Print the current user to terminal

        pdf_1_button = Button(self.root, text= "PDF 1", padx=100, pady = 100, bg="black")
        pdf_1_button.pack()


        self.root.mainloop()    

    def open_pdf(self, pdf_location):
        pass


class PDF_Viewer(object):
    def __init__(self, pdf_location):
        self.root = tk.Tk()
        self.pdf_viewer = pdf.ShowPdf()
        self.pdf_viewer.pack(side="top", fill="both", expand=True)
        self.pdf_viewer.load_pdf(r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Backend\pdfs\dummy1")


        self.root.mainloop()
        



class User():
   def __init__(self, user_name, pass_word, user_number):
        self.user_number = user_number
        self.name = user_name
        self.password = pass_word
        





if __name__ == "__main__":
    LoginScreen()




    






