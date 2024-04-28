# Logs

## Date: 04/10/2024
- **Logged by:** Areyan Rastawan
- **Activities:**
  - Added logs to GitHub.
  - Set up the project plan.

## Date: 04/11/2024 - Group Meeting
- **Meeting Time:** 6:00 PM - 8:00 PM
- **Notes:**
  - Made the Gantt chart.
  - Progress on project plan.
  - Progress check on the SDS.
  - Discussed milestones.

**Logged by:** Solomon Haskell
- **Activities:**
  - Updated Gantt Chart.
  - Added roles to project plan.
  - Linked Gantt chart to SDS.
  - Added to the SDS as well as formatting.

**Logged by:** Jerin Spencer
- **Activities:**
  - Updated Gantt Chart.
  - Added roles to project plan.
  - Linked Gantt chart to SDS.
  - Added to the SDS as well as formatting.

**Logged by:** Areyan Rastawan
- **Activities:**
  - Finalized Project Plan.
  - Cleaned scheduling.
  - Added roles and expected dates to Gantt chart.
  - Added work breakdown milestones.

## Date: 04/15/2024
- **Logged by:** Miles Anderson
- **Activities:**
  - Created UI.py, planning on using TKinter to create the UI for the project.
  - Initial creation of the file, very little actual code written.

## Date: 04/18/2024 - Group Meeting
- **Meeting Time:** 6:00 PM - 6:30 PM
- **Notes:**
  - Discussed personal task deadlines.
  - Updated Gantt chart.
  - Planned next meeting to review teams' material and tie them together.

**Logged by:** Areyan Rastawan
- **Activities:**
  - Set up the MySQL database.
  - Connected the MySQL database to ix-dev server.
  - Researched SQL.
  - I added a table for usernames and user IDs with notes for testing.


## Date: 04/20/2024
**Logged by:** Solomon Haskell
- **Activities:**
  - Created pdf_test.py to try and send pdfs to table on server
  - Added a Running tab to the readme to help users run code when they download
  - added pdfs directory to store pdfs before they are sent to the server. Going to change this for sure.
  - added requirements.txt to help speed up getting required modules


## Date: 4/21/2024
**logged by:** Miles Anderson
  - **Activities:**
  - Worked entirely in UI.py
  - Created classes that act as different pages in program
  - Login page, where you enter username and password is complete
  - PDF Selector page is a work in progress but have the ability to pass information between pages
  - Just need to get PDF Viewer Complete

  **Logged by:** Solomon Haskell
- **Activities:**
  - Made sql_functions.py and pdfs and received_pdfs for pdf-database usage.
  - Added to requirements.
  - Worked on the logic for pdf tables


## Date: 4/21/2024
**Logged by:** Areyan Rastawan
  - **Activities:**
    - Worked on initializing the PDFs when the program opens.
    - Worked on a way for the server to communicate with the preloaded PDFs.
    - Started using the Tkinter PDF viewer.
    - PDFs can now be generated (broken).


## Date: 4/22/2024
**Logged by:** Areyan Rastawan
  - **Activities:**
    - PDFs now auto-generate the location on the startup of the program.
    - The PDFs are now being deleted at the end of the program to stop the overlapping.
    - Changed the password and username system to autofill for testing.
    - Removed the TkPDF viewer and PDFs are finally fixed (PyMuPDF).
    - Added a scrollbar to be able to scroll in the PDF.
    - Added buttons for saving and deleting notes (don't communicate with the database yet).


## Date: 4/23/2024
**Logged by:** Areyan Rastawan
  - **Activities:**
    - Notes can successfully be saved and deleted.
    - Added a way to be able to load the previous notes.
    - Changed the notes table to also hold a note name.
    - The PDF can now also turn into the highlighted version of the PDF.
    - Added a dropdown bar for all the saved notes.


## Date: 4/24/2024
**Logged by:** Areyan Rastawan
  - **Activities:**
    - Implemented a way to be able to add chapters and sections to the notes.
    - Gave the notes a hierarchy system.
    - Messed around with the GUI, tried to format it better (buggy).


## Date: 4/25/2024
**Logged by:** Areyan Rastawan
  - **Activities:**
    - Finished the full functionality of the program and moved on to testing phases.
    - Made a couple of edits to the GUI and login system.
    - The user can now either log in with a user system, which will take you to an auto server, or an admin system for someone who has their own server.
    - The program works completely on my end but will need to be tested with other computers.

## Date: 4/25/2024
**Logged by:** Solomon Haskell
- **Activities:**
  - Highlighted chapter 5 and added chapter 6 highlighed to the pdfs
  - comments for some functions


## Date: 4/26/2024
**Logged by:** Areyan Rastawan
  - **Activities:**
    - made the guiu look better 
    - added the sq3r hintto the main menu 
    - fixed some internalisssues with the ntoes syste , someneer along th eway it broke 
    - tried with the macbook it works
    - tried testng with he another server but it broke 

## Date: 4/27/2024
**Logged by:** Areyan Rastawan
  - **Activities:**
    - Fixed issues with tabling and port, and now the user can sign in using a different server.
    - The program's progress is saved through the server.
    - Added documentation to the functions.
    - The server and program should now support full functionality.