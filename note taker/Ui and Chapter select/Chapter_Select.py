import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter.scrolledtext import ScrolledText
import os
#done: change save file so it automatically saves in the a given file path
#done: add auto saving to the return command
#TODO: add some sort of bolding options or something for section differentiation
#TODO: add scroll bar to notepad 


win = tk.Tk()

#special button commands
cur_open = ["NULL"] #tracks the currently open file for savefile. done as single entry list cause its stupid like me
def saveFile():
    new_file = open(cur_open[0], "w") #in progress, not sure how to save the file path when opening the notepad frame
    if new_file is None:
        return
    text = str(entry.get(1.0, tk.END))
    new_file.write(text)
    new_file.close()

def openFile(file_path):
    cur_open[0] = str(file_path)
    file = open(file_path, "r")
    if file is not None:
        content = file.read()
    entry.insert(tk.INSERT, content)
    notepad.tkraise()

def clearFile():
    entry.delete(1.0, tk.END)

def to_chapter_select():
    saveFile()
    clearFile()
    page2.tkraise()


style1 = font.Font(size = 25)
style2 = font.Font(size = 20)
page1 = Frame(win)
page2 = Frame(win)
notepad = Frame(win)

page1.grid(row = 0, column= 0, sticky = "nsew")
page2.grid(row = 0, column= 0, sticky = "nsew")
notepad.grid(row = 0, column= 0, sticky = "nsew")

lb1 = Label(page1, text = "page 1", font = style1)
lb1.pack(pady=20)

lb2 = Label(page2, text = "page 2", font = style1)
lb2.pack(pady=20)

btn1 = Button(page1, text = "page2", command =lambda: page2.tkraise(), font = style2)
btn1.pack()

#set up chapter select frame--------------
directory = os.getcwd()
files = os.listdir(directory)
buttons= []
paths = [] # saves the path to each file
open_path = ""
for i in range(len(files)):
    paths.append( directory + "\\" + files[i])
    buttons.append(tk.Button(page2, text=files[i], command =lambda cur_path = paths[i]:  openFile(cur_path),
                              bg = "white", height = 5, width = 50, font = ("times", 10), pady = 10))
    buttons[i].pack(padx = 100)

btn2 = Button(page2, text = "page1", command =lambda: page1.tkraise(), font = style2)
btn2.pack()

btn3 = Button(page2, text = "to notes", command =lambda: notepad.tkraise(), font = style2)
btn3.pack()
#-----------------------------------

# Notepad Frame------------------------------------------------------------------------------------------------------

top = tk.Frame(notepad)  #frame holds the buttons, makes it easier to format

top.pack(padx = 10, pady = 5, anchor = "nw")
b1 = tk.Button(notepad, text="Open", bg = "white", command = openFile) #command links the button to a function
b1.pack(in_ = top, side = tk.LEFT)

b2 = tk.Button(notepad, text="Save", bg = "white", command = saveFile)
b2.pack(in_ = top, side = tk.LEFT)

b4 = tk.Button(notepad, text="Return to Chapter select", bg = "white", command = to_chapter_select)
b4.pack(in_ = top, side = tk.LEFT)

#text window
entry = ScrolledText(notepad,wrap = tk.WORD, bg = "#F9DDA4", font = ("times", 15), height = 25, width = 60)

entry.pack(padx = 10, pady = 5)

#-----------------------------------------------------------------------------------------------------

page1.tkraise()

win.geometry("650x650")
win.title("Multiple Pages application")

win.resizable(False,False)
win.mainloop()


