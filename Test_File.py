import tkinter as tk
from tkinter import *

from tkPDFViewer import tkPDFViewer as pdf


test_file_1 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\final notesheet 2.pdf"
test_file_2 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Resume 2_1_2024.pdf"


class Veiwer(Frame):
    def __init__(self,given_file):
        self.root = tk.Tk()

        v1 = pdf.ShowPdf() 
        v2 = v1.pdf_view(self.root, pdf_location=given_file, width = 77, height = 77) 
        v2.pack(pady=10,padx=10)

        self.root.mainloop()

def open_pdf_viewer(file):
    #root.destroy()
    Veiwer(file)


#########################################################################

root = tk.Tk()
root.geometry("500x250")

def main():
    frame = Frame(root, width=500,height=250)
    frame.place(x=0,y=0)

    pdf_1_button = Button(frame, text= "PDF 1")
    pdf_1_button.place(x=10,y=10)


#pdf_2_button = Button(root, text= "PDF 2",height=1,width=1, padx=30, pady = 30, command=lambda: open_pdf_viewer(test_file_2))
#pdf_2_button.pack()


main()

root.mainloop
    






