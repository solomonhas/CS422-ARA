import tkinter as tk
from tkinter import *
from tkinter import font
import os

win = tk.Tk()

def fill_chapter_frame(sections_frame, chapter_path, prev_frame):
    """
    Makes a frame for a chapter folder, gives each section txt a button.
    """
    files = os.listdir(chapter_path)
    print(chapter_path) # test print
    sec_buts = []
    for i in range(len(files)):
        print("\t"+ files[i])   #test print
        sec_buts.append(tk.Button(sections_frame, text=files[i], bg = "white", height = 5, width = 50, font = ("times", 10), pady = 10))
        sec_buts[i].pack(padx = 0)
    sec_buts.append(Button(sections_frame, text = "page2", command =lambda: page2.tkraise(), font = style2))
    sec_buts[i+1].pack()
    print(sections_frame)



style1 = font.Font(size = 25)
style2 = font.Font(size = 20)
page1 = Frame(win)
page2 = Frame(win)

page1.grid(row = 0, column= 0, sticky = "nsew")
page2.grid(row = 0, column= 0, sticky = "nsew")

lb1 = Label(page1, text = "page 1", font = style1)
lb1.pack(pady=20)

lb2 = Label(page2, text = "page 2", font = style1)
lb2.pack(pady=20)

btn1 = Button(page1, text = "page2", command =lambda: page2.tkraise(), font = style2)
btn1.pack()

#set up chapter select frame--------------
directory = os.getcwd()
files = os.listdir(directory)
sections = [] #frames for each chapter to hold display the sections
buttons= []
for i in range(len(files)):
    sections.append(Frame(win))
    sections[i].grid(row = 0, column= 0, sticky = "nsew")
    chapter_path = directory +"\\" + files[i] #construct path to chapter folder
    fill_chapter_frame(sections[i], chapter_path, page2)

    #TODO Problem: the buttons will all link to the same chapter folder
    buttons.append(tk.Button(page2, text=files[i], command =lambda: sections[i].tkraise(),
                              bg = "white", height = 5, width = 50, font = ("times", 10), pady = 10))
    buttons[i].pack(padx = 100)

btn2 = Button(page2, text = "page1", command =lambda: page1.tkraise(), font = style2)
btn2.pack()
#-----------------------------------

page1.tkraise()

win.geometry("650x650")
win.title("Multiple Pages application")

win.resizable(False,False)
win.mainloop()


