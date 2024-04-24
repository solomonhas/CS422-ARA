import tkinter as tk
from tkinter import *

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
    #v2 = v1.pdf_view(root, pdf_location=file)
    #v2.pack()

    #root1.mainloop()



#########################################################################


class MainW(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        #init_frame = Frame(app, width=1000, height=1000)
        self.parent = parent
        self.function()

    def function(self):
        button1 = Button(self, text= "PDF 1",command=screen1)
        button1.place(x=10,y=10)

        button2 = Button(self, text= "PDF 2", command=screen2)
        button2.place(x=10,y=50)

        back_button = Button(self, text="Back", command=self)
        back_button.place(x=10,y=90)



def screen1():
    frame1 = Frame(app, width=1000,height=1000)
    frame1.place(x=0,y=0)

    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(frame1, pdf_location=test_file_1)
    v2.place(x=0,y=0)

    back_button = Button(frame1, text="Back", command= screen2)
    back_button.place(x=800,y=90)

def screen2():
    frame2 = Frame(app, width=1000,height=1000)
    frame2.place(x=0,y=0)

    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(frame2, pdf_location=test_file_2)
    v2.place(x=0,y=0)

    back_button = Button(frame2, text="Back",command=app)
    back_button.place(x=800,y=90)



#pdf_2_button = Button(root, text= "PDF 2",height=1,width=1, padx=30, pady = 30, command=lambda: open_pdf_viewer(test_file_2))
#pdf_2_button.pack()

app = MainW(None)

app.mainloop()

    





