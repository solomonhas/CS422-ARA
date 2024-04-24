import tkinter as tk
from tkinter import *
import os
from tkPDFViewer import tkPDFViewer as pdf

test_file_1 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Frontend\sample.pdf"
test_file_2 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Frontend\Resume 2_1_2024.pdf"


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

        pdf_1_button = Button(self.root, text= "PDF 1",height=1,width=1, padx=30, pady = 30, command=lambda: self.open_pdf_viewer(test_file_1))
        pdf_1_button.pack(pady=10)

        pdf_2_button = Button(self.root, text= "PDF 2",height=1,width=1, padx=30, pady = 30, command=lambda: self.open_pdf_viewer(test_file_2))
        pdf_2_button.pack()

        back_button = Button(self.root, text="Back", command=lambda: self.back_to_login())
        back_button.pack(pady=30)

        self.root.mainloop()
    
    def back_to_login(self):
        self.root.destroy()
        LoginScreen()

    def back_to_home(self):
        self.viewer.destroy()
        HomeScreen("Blank_User")

    def open_pdf_viewer(self, pdf_location_var):
        self.root.destroy()

        self.viewer = tk.Tk()
        self.viewer.title(pdf_location_var)

        back_button = Button(self.viewer, text="Back",height=1,width=1,padx=100, command=lambda: self.back_to_home())
        back_button.pack()

        v1 = pdf.ShowPdf() 
        v2 = v1.pdf_view(self.viewer, pdf_location=pdf_location_var, width = 77, height = 77) 
        v2.pack(pady=10,padx=10)

        self.viewer.mainloop()



class PDF_Viewer(object):
    def __init__(self, pdf_location_var):

        self.root = tk.Tk()
        self.root.minsize(400,400)
        self.root.maxsize(600,600)
        self.root.title(pdf_location_var)



        v1 = pdf.ShowPdf() 
        v2 = v1.pdf_view(self.root, pdf_location=pdf_location_var, width = 77, height = 100) 
        v2.pack(pady=(0,0))

        self.root.mainloop()




      

class User():
   def __init__(self, user_name, pass_word, user_number):
        self.user_number = user_number
        self.name = user_name
        self.password = pass_word
        

if __name__ == "__main__":
    #LoginScreen() Tabbed out currently to skip log in for practicality of testing
    test_file_1 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Frontend\sample.pdf"
    test_file_2 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Frontend\Resume 2_1_2024.pdf"


    HomeScreen("Blank_User")





    




