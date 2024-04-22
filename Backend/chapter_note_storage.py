import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'ix-dev.cs.uoregon.edu',
    'port': 3056,
    'user': 'group6',
    'password': 'group6',
    'database': 'ara_db'
}
"""

This handles each chapter by giving it an 
Id and name for each chapter
ID auto incraments

CREATE TABLE Chapters (
    chapter_id INT AUTO_INCREMENT PRIMARY KEY,
    chapter_name VARCHAR(255) NOT NULL
);

This handles the chapter notes
this gives a note id that incraments
a chapter ID that is linked to the Chapters Table

CREATE TABLE ChapterNotes (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    chapter_id INT,
    note_file_path VARCHAR(255),
    FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id)
);

"""
