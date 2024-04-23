import tkinter as tk
from tkinter import *
from tkPDFViewer import tkPDFViewer as pdf 

test_file = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Frontend\sample.pdf"



root = tk.Tk()

v1 = pdf.ShowPdf() 
v2 = v1.pdf_view(root, pdf_location=test_file, width = 50, height = 10) 
v2.pack()

root.mainloop()