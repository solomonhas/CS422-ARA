# CS422-ARA

## Desciption
This project is an implimentation of a Active Reading Assistant. This is to help users engage in active learning using the SQ3R system of reading. SQ3R is Survey, Question, Read, Recite, Review. It is built using python with the tkinter import for the UI, and MySQL for that database to store notes and PDF's. When logging in, you are greeted with either logging in as Admin or User. If you choose admin, you have the option to connect your own MySQL database. If you login as user, you do not have that option.

## Authors
- Miles Anderson
- Solomon Haskell
- Areyan Rastawan
- Jerin Spencer

This Repository was made April 9th 2024 for CS 422 Software Methodologies at the University of Oregon. It was made to impliment an Active-Reading Assistant as our project 1.

## Installation/Running
To run our application, you can either click the green code button and click the "Download ZIP" dropdown, or you can clone our code using:

```bash
git clone https://github.com/solomonhas/CS422-ARA.git
```

### Installation Guide
Please complete the steps found [here](https://github.com/solomonhas/CS422-ARA/blob/main/Installation.txt).

###
Once you have installed the requirements and set up a server. you can type to run the program.
```bash
python3 UI.py
```

## Software Dependencies
This code runs on Python 3.12, and only requires to install mysql-connector-python and PyMuPDF. There are a few imports used mainly as an aid for PDF viewing within Tkinter as well as directory lookup for initial sending and receiving of PDFs. Theses are the imports that we have used

```python
import fitz
import sys
import tkinter.messagebox as messagebox
import os
import mysql.connector
import tkinter as tk
```

## Subdirectories
- There are two directories for storing PDFs received from the SQL server. CS422-ARA\pdfs and CS422-ARA\highlighted, any PDF files you store in pdf will be sent to the database in a table upon running the program. The other directory highlighted is for pre-highlighted pdfs that are manually stored there.

- CS422-ARA\logs contains a log.md file where each group member explains what they have worked on, whenever they have worked on the project, along with the dates.

- The database and UI are each their own python file labled as expected.

- requirements.txt is used to ease the process of installing the required dependencies for the program.