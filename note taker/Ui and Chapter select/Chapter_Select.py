import tkinter as tk
from tkinter import font, Frame, Label, Button
import os

win = tk.Tk()


def fill_chapter_frame(sections_frame, chapter_path, prev_frame):
    files = os.listdir(chapter_path)
    print(chapter_path)  # debug print
    sec_buts = []
    for i, file_name in enumerate(files):
        print("\t" + file_name)  # debug print
        sec_buts.append(
            tk.Button(sections_frame, text=file_name, bg="white", height=5, width=50, font=("times", 10), pady=10))
        sec_buts[i].pack(padx=0)
    sec_buts.append(Button(sections_frame, text="page2", command=lambda: prev_frame.tkraise(), font=style2))
    sec_buts[-1].pack()
    print(sections_frame)


style1 = font.Font(size=25)
style2 = font.Font(size=20)
page1 = Frame(win)
page2 = Frame(win)

page1.grid(row=0, column=0, sticky="nsew")
page2.grid(row=0, column=0, sticky="nsew")

lb1 = Label(page1, text="page 1", font=style1)
lb1.pack(pady=20)

lb2 = Label(page2, text="page 2", font=style1)
lb2.pack(pady=20)

btn1 = Button(page1, text="page2", command=lambda: page2.tkraise(), font=style2)
btn1.pack()

directory = os.getcwd()
files = os.listdir(directory)
sections = []
buttons = []

for i, file in enumerate(files):
    chapter_path = os.path.join(directory, file)
    if os.path.isdir(chapter_path):  # Make sure it's a directory
        sections.append(Frame(win))
        sections[i].grid(row=0, column=0, sticky="nsew")
        fill_chapter_frame(sections[i], chapter_path, page2)

        buttons.append(tk.Button(page2, text=file, command=lambda i=i: sections[i].tkraise(),
                                 bg="white", height=5, width=50, font=("times", 10), pady=10))
        buttons[i].pack(padx=100)

btn2 = Button(page2, text="page1", command=lambda: page1.tkraise(), font=style2)
btn2.pack()

page1.tkraise()

win.geometry("650x650")
win.title("Multiple Pages application")
win.resizable(False, False)
win.mainloop()
