import tkinter as tk
from tkinter import *
from tkinter import font
win = tk.Tk()

style1 = font.Font(size = 25)
style2 = font.Font(size = 20)
page1 = Frame(win)
page2 = Frame(win)
page3 = Frame(win)

page1.grid(row = 0, column= 0, sticky = "nsew")
page2.grid(row = 0, column= 0, sticky = "nsew")
page3.grid(row = 0, column= 0, sticky = "nsew")

lb1 = Label(page1, text = "page 1", font = style1)
lb1.pack(pady=20)

lb2 = Label(page2, text = "page 2", font = style1)
lb2.pack(pady=20)

lb3 = Label(page3, text = "page 3", font = style1)
lb3.pack(pady=20)

btn1 = Button(page1, text = "page2", command =lambda: page2.tkraise(), font = style2)
btn1.pack()

btn2 = Button(page2, text = "page1", command =lambda: page1.tkraise(), font = style2)
btn2.pack()

btn3 = Button(page2, text = "page3", command =lambda: page3.tkraise(), font = style2)
btn3.pack()

btn4 = Button(page3, text = "page2", command =lambda: page2.tkraise(), font = style2)
btn4.pack()

page1.tkraise()

win.geometry("650x650")
win.title("Multiple Pages application")
win.resizable(False,False)
win.mainloop()