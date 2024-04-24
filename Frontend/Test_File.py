import tkinter as tk
from tkinter import *

from tkPDFViewer import tkPDFViewer as pdf


test_file_1 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Frontend\sample.pdf"
test_file_2 = r"C:\Users\tarsa\OneDrive\Documents\GitHub\CS422-ARA\Frontend\Resume 2_1_2024.pdf"





def open_pdf_viewer(pdf_location_var):
    viewer = tk.Tk()

    v1 = pdf.ShowPdf() 
    v2 = v1.pdf_view(viewer, pdf_location=pdf_location_var, width = 77, height = 77) 
    v2.pack(pady=10,padx=10)

    viewer.mainloop()

root = tk.Tk()
root.minsize(600,400)
root.title("Group 6 ARA")



pdf_1_button = Button(root, text= "PDF 1",height=1,width=1, padx=30, pady = 30, command=lambda: open_pdf_viewer(test_file_1))
pdf_1_button.pack(pady=10)


#pdf_2_button = Button(root, text= "PDF 2",height=1,width=1, padx=30, pady = 30, command=lambda: open_pdf_viewer(test_file_2))
#pdf_2_button.pack()

back_button = Button(root, text="Back", command=lambda: self.back_to_login())
back_button.pack(pady=30)

root.mainloop()
    






