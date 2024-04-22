import tkinter as tk
from tkinter import *
import os
import shutil


#from tkPDFViewer import tkPDFViewer as pdf

test_file ="/Users/milesoop/Documents/GitHub/CS422-ARA/Backend/pdfs/dummy1.pdf"

class LoginScreen:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.configure(highlightbackground="red")
        self.root.minsize(400,200)
        self.root.title("Group 6 ARA")

        self.username_textbox = tk.Entry(self.root,text="Username:")
        self.username_textbox.pack(padx=10,pady=20)

        self.password_textbox = tk.Entry(self.root,text="Password:")
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

        pdf_1_button = Button(self.root, text= "PDF 1",height=1,width=1, padx=30, pady = 30, command=lambda: self.open_pdf_viewer("PDF1"))
        pdf_1_button.pack(pady=10)

        pdf_2_button = Button(self.root, text= "PDF 2",height=1,width=1, padx=30, pady = 30, command=lambda: self.open_pdf_viewer("PDF2"))
        pdf_2_button.pack()

        back_button = Button(self.root, text="Back", command=lambda: self.back_to_login())
        back_button.pack(pady=30)

        self.root.mainloop()
    
    def back_to_login(self):
        self.root.destroy()
        LoginScreen()

    def open_pdf_viewer(self, pdf_location):
        PDF_Viewer(pdf_location)


class PDF_Viewer(object):
    def __init__(self, pdf_location_var):
        self.root = tk.Tk()
        self.root.minsize(400,400)
        self.root.maxsize(600,600)
        self.root.title(pdf_location_var)
        print(pdf_location_var)
        #self.root.bg("black")

        #v1 = pdf.ShowPdf() 
        #v2 = v1.pdf_view(self.root, pdf_location=pdf_location_var, width = 400, height = 400) 
        #v2.pack()

        self.root.mainloop()
      

class User():
   def __init__(self, user_name, pass_word, user_number):
        self.user_number = user_number
        self.name = user_name
        self.password = pass_word
        

if __name__ == "__main__":
    LoginScreen()




    




