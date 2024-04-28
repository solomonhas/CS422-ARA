# Active Reading Assistant Server Installation Setup Guide

## Pip Installs
- **`pip install mysql-connector-python`**
- **`pip install PyMuPDF`**

## Server Setup

### STEP 1
Log on to a Linux-enabled machine, such as the University of Oregon Computer Science department machine ix.  
From a terminal, the command would be:  

**\```bash
ssh username@ix.cs.uoregon.edu
\```**  

(Replace username with your login name.)

### STEP 2
In your home directory, run the command:  

**\```bash
mysqlctl install
\```**  

You will be prompted to enter a password. Remember this password as you will need it to run MySQL commands.

### STEP 3
Run the command:  

**\```bash
mysqlctl start
\```**  

This command will start the server, create a `.my.conf` file, and generate a port.

### STEP 4
Run the command:

**\```bash
mysqlctl status
\```** 

The output should be something like: `mysqld (pid 897565) listening on ix-dev:3056`  
Make a note of the port number (3056 in this example) as this is the server's port number. Note that your generated port number will be different.  

Alternatively, if you have administrative privileges, run:  

**\```bash
mysqladmin -p version
\```**  

and make note of the number that appears next to TCP port.

### STEP 5
Run the command: 

**\```bash
mysql -p
\```**  

Your terminal should now display `mysql >` and allow you to type queries.

### STEP 6
To create a database, type the query:  

**\```sql
CREATE DATABASE ara_db;
\```**

Press enter, you should see: `Query OK, 1 row affected`

### STEP 7
Run the query: 

**\```sql
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
\```**  

Replace username and password with your choices, but ensure to remember them.  

Next, grant the user privileges to the database by running:  

**\```sql
GRANT ALL PRIVILEGES ON ara_db.* TO 'username'@'%' WITH GRANT OPTION;
\```**  

Replace username with the username you chose.  
Finalize the grant by running:  

**\```sql
FLUSH PRIVILEGES;
\```**  

As each query is entered, you should see: `Query OK, 0 rows affected`

### STEP 8
You will then need to run three queries to create the database tables: 

**\```sql
CREATE TABLE pdf_table (pdf_id INT AUTO_INCREMENT PRIMARY KEY, pdf_name VARCHAR(255) NOT NULL, pdf_location VARCHAR(255) NOT NULL, highlighted_pdf_location VARCHAR(255));
\```**  

**\```sql
CREATE TABLE notes (note_id INT AUTO_INCREMENT PRIMARY KEY, pdf_id INT, note LONGTEXT, note_name VARCHAR(255) NOT NULL, FOREIGN KEY (pdf_id) REFERENCES pdf_table(pdf_id));
\```**

### STEP 9
The database is now set up with the appropriate fields. Enter `exit` into the SQL queries terminal and proceed to the Active Reading Assistant application.

### STEP 10
Launch the Active Reading Assistant and enter the server information:
- **Host:** Enter the server domain name (example: `ix-dev.cs.uoregon.edu`)
- **Port:** Enter the port number captured in step 4
- **Username:** Enter the username created in step 7
- **Password:** Enter the password created in step 7
- **Database:** Enter `ara_db`
