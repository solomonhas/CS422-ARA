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
User Table holds 
Username 
User ID # it is auto incramented everytime a new user is created


Notes Table holds 
User ID // has a refrence to the other table 
Note ID
Note text // holds the txt

"""

