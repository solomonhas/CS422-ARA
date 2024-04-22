#Code comes from youtube channel "Coding With Evan", has slight adaptations but mostly
#follows the tutorial to point: https://www.youtube.com/watch?v=gWeo8bZvu8o

from tkinter.filedialog import*
import tkinter as tk

def saveFile():
    new_file = asksaveasfile(mode ='w', filetype = [('text files', '.txt')])
    if new_file is None:
        return
    text = str(entry.get(1.0, tk.END))
    new_file.write(text)
    new_file.close()

def openFile():
    file = askopenfile(mode = 'r', filetype = [('text files', '*.txt')])
    if file is not None:
        content = file.read()
    entry.insert(tk.INSERT, content)

def clearFile():
    entry.delete(1.0, tk.END)


#setting up Notepad Canvas
canvas = tk.Tk()
canvas.geometry("400x600")  #size
canvas.title("Notepad") #window title
canvas.config(bg = "white") #background color

#Buttons
top = tk.Frame(canvas)  #frame holds the buttons, makes it easier to format

top.pack(padx = 10, pady = 5, anchor = "nw")
b1 = tk.Button(canvas, text="Open", bg = "white", command = openFile) #command links the button to a function
b1.pack(in_ = top, side = tk.LEFT)

b2 = tk.Button(canvas, text="Save", bg = "white", command = saveFile)
b2.pack(in_ = top, side = tk.LEFT)

b3 = tk.Button(canvas, text="Clear", bg = "white", command = clearFile)
b3.pack(in_ = top, side = tk.LEFT)

b4 = tk.Button(canvas, text="Exit", bg = "white", command = exit)
b4.pack(in_ = top, side = tk.LEFT)

#text window
entry = tk.Text(canvas,wrap = tk.WORD, bg = "#F9DDA4", font = ("times", 15))
entry.pack(padx = 10, pady = 5, expand = tk.TRUE, fill = tk.BOTH)

canvas.mainloop()