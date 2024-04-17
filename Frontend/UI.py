import tkinter as tk
from tkinter import ttk


class User():
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.correct_password = False


class MainApplication(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)

    notebook = ttk.Notebook(parent)

    notebook.add(Typ1(notebook), text='TAB1')
    notebook.add(Typ2(notebook), text='TAB2')
    notebook.pack()

class Typ1(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        shell_frame=tk.LabelFrame(self, padx=5, pady=5, width=200, height=200)
        shell_frame.grid(row=0,column=0,padx=5,pady=5)



if __name__ == "__main__":
    window = tk.Tk()
    MainApplication(window).pack(side="top", fill="both", expand=True)
    window.mainloop()





