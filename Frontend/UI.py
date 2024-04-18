import tkinter as tk
from tkinter import *




#class User():
#   def __init__(self, username, user_passw):
#       self.name = username
#       self.password = user_passw
        


def retrieve_input():
    global username
    global password
    username = username_textbox.get()
    password = password_textbox.get()
    if username == "Admin" and password == "Admin":
        print("Welcome")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SQ3R Helper")
    root.configure(background="grey")
    root.minsize(600,600)
    root.geometry("800x800+100+100")


    username_textbox = tk.Entry(root)
    username_textbox.pack()

    password_textbox = tk.Entry(root)
    password_textbox.pack()

    
    enter_button = Button(root, text="Enter", command=retrieve_input)
    enter_button.pack()








    root.mainloop()



