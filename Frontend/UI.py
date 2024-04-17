import tkinter as tk
from tkinter import *


class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.correct_password = False




if __name__ == "__main__":
    window = tk.Tk()
    window.title("SQ3R Helper")
    window.configure(background="grey")
    #window.minsize(800,800)
    window.geometry("800x800+100+100")
    window.mainloop()





