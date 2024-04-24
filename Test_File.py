import tkinter as tk
from tkinter import *
from tkinter import font

from tkPDFViewer import tkPDFViewer as pdf


test_file_1 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\final notesheet 2.pdf"
test_file_2 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Resume 2_1_2024.pdf"

#class Veiwer(Frame):
    #def __init__(self,given_file):
        #self.fr=tk.Frame(root)


        #v1 = pdf.ShowPdf() 
        #v2 = v1.pdf_view(self.root, pdf_location=given_file, width = 77, height = 77) 
        #v2.pack(pady=10,padx=10)

        #self.root.mainloop()

#def open_pdf_viewer(file):
    #root1 = tk.Tk()

    #v1 = pdf.ShowPdf()
    #v2 = v1.pdf_view(root1, pdf_location=test_file_1)
    #v2.pack()

    #root1.mainloop()

#########################################################################

class FirstWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Window 1").pack(padx=10,pady=10)
        first_pdf = pdf.ShowPdf()
        first_pdf_prepack = first_pdf.pdf_view(self, pdf_location=test_file_1, width=50,height=50,load='after')
        first_pdf_prepack.pack()
        self.pack(padx = 10, pady = 10)

class SecondWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Window 2").pack(padx=10,pady=10)
        second_pdf = pdf.ShowPdf()
        second_pdf_prepack = second_pdf.pdf_view(self, pdf_location=test_file_2, width=50,height=50,load='after')
        second_pdf_prepack.pack()
        self.pack(padx = 10, pady = 10)

class MainWindow():
    def __init__(self,master) -> None:
        mainframe = tk.Frame(master)
        mainframe.pack(padx=10,pady=10, fill='both',expand=1)
        self.index = 0

        self.frameList = [FirstWindow(mainframe),SecondWindow(mainframe)]
        self.frameList[1].forget()

        bottomframe = tk.Frame(master)
        bottomframe.pack(padx=10,pady=10)

        switch = tk.Button(bottomframe, text="switch", command= self.changeWindow)
        switch.pack(padx=10,pady=10)

    def changeWindow(self):
        self.frameList[self.index].forget()
        self.index = (self.index + 1)% len(self.frameList)
        self.frameList[self.index].tkraise()
        self.frameList[self.index].pack(padx=10,pady=10)



root = tk.Tk()
window = MainWindow(root)
root.mainloop()

    





