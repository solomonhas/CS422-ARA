import tkinter as tk
from tkinter import Button, Entry, Toplevel, Label, Text
import database
import fitz
import sys
import tkinter.messagebox as messagebox
import os
import mysql.connector
import random

#
class LoginScreen:
    def __init__(self, root):
        """Initialize the LoginScreen class."""
        self.root = root
        self.root.minsize(400, 300)
        self.root.title("group 6 ara")

        self.create_widgets()

    # Create the widgets for the login screen
    def create_widgets(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        # Select mode
        self.mode_label = tk.Label(self.login_frame, text="Select mode:")
        self.mode_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.mode_var = tk.StringVar(self.login_frame, value="user")
        self.mode_user_radio = tk.Radiobutton(self.login_frame, text="User", variable=self.mode_var, value="user",
                                              command=self.hide_server_login_fields)
        self.mode_user_radio.grid(row=0, column=1, padx=5, pady=5)  # Changed column to 1
        self.mode_admin_radio = tk.Radiobutton(self.login_frame, text="Admin", variable=self.mode_var, value="admin",
                                               command=self.show_server_login_fields)
        self.mode_admin_radio.grid(row=0, column=2, padx=5, pady=5)  # Changed column to 2

        # Server login fields
        self.host_label = Label(self.login_frame, text="host:")
        self.host_textbox = Entry(self.login_frame)
        self.host_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.host_textbox.insert(0, 'ix-dev.cs.uoregon.edu')
        self.host_textbox.grid(row=1, column=1, padx=10, pady=5)

        self.port_label = Label(self.login_frame, text="port:")
        self.port_textbox = Entry(self.login_frame)
        self.port_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.port_textbox.insert(0, '3056')
        self.port_textbox.grid(row=2, column=1, padx=10, pady=5)

        self.username_label = Label(self.login_frame, text="username:")
        self.username_textbox = Entry(self.login_frame)
        self.username_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.username_textbox.insert(0, 'group6')
        self.username_textbox.grid(row=3, column=1, padx=10, pady=5)

        self.password_label = Label(self.login_frame, text="password:")
        self.password_textbox = Entry(self.login_frame, show="*")
        self.password_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.password_textbox.insert(0, 'group6')
        self.password_textbox.grid(row=4, column=1, padx=10, pady=5)

        self.login_button = Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=5, columnspan=2, pady=10)

        self.hide_server_login_fields()  # Initially hide the server login fields

    # Show the server login fields
    def show_server_login_fields(self):
        self.host_label.grid()
        self.host_textbox.grid()
        self.port_label.grid()
        self.port_textbox.grid()
        self.username_label.grid()
        self.username_textbox.grid()
        self.password_label.grid()
        self.password_textbox.grid()

    # Hide the server login fields
    def hide_server_login_fields(self):
        self.host_label.grid_remove()
        self.host_textbox.grid_remove()
        self.port_label.grid_remove()
        self.port_textbox.grid_remove()
        self.username_label.grid_remove()
        self.username_textbox.grid_remove()
        self.password_label.grid_remove()
        self.password_textbox.grid_remove()

    # Validate the login credentials
    def login(self):
        mode = self.mode_var.get()

        if mode == "admin":
            self.show_admin_main_window()
        else:  # User mode
            self.auto_login()

    # Show the main window for admin mode
    def show_admin_main_window(self):
        host = self.host_textbox.get()
        port = self.port_textbox.get()
        username = self.username_textbox.get()
        password = self.password_textbox.get()

        if not all([host, port, username, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        self.root.withdraw()
        self.main_window = HomeScreen("blank_user", self.root, host, port, username, password)

    # Auto-login for user mode
    def auto_login(self):
        # Set default user credentials
        default_host = 'ix-dev.cs.uoregon.edu'
        default_port = 3056  # Change this to your desired default user port
        default_username = 'group6'
        default_password = 'group6'

        self.show_home_screen(default_host, default_port, default_username, default_password)

    def show_home_screen(self, host, port, username, password):
        """Show the home screen."""
        self.root.withdraw()
        self.main_window = HomeScreen("blank_user", self.root, host, port, username, password)


class HomeScreen:
    def __init__(self, userid, login_root, host, port, username, password):
        self.login_root = login_root
        self.root = tk.Toplevel(login_root)
        self.root.minsize(800, 600)
        self.root.title("group 6 ara")

        self.original_pdf_location = None  # Store the original PDF location
        self.show_notes_flag = True  # Track the state of showing notes

        # Connect to the database and retrieve PDF locations
        self.db_manager = database.DatabaseManager(
            host=host,
            port=int(port),
            user=username,
            password=password,
            database='ara_db'
        )
        if self.db_manager.is_pdf_table_empty():
            self.db_manager.build_pdf_table()
        self.db_manager.update_pdf_locations()
        pdf_locations = self.db_manager.get_pdf_locations()



        # Create buttons for each PDF location
        for i, pdf_location in enumerate(pdf_locations):
            pdf_button = Button(self.root, text=f"pdf {i + 1}", height=1, width=1, padx=50, pady=30,
                                command=lambda loc=pdf_location: self.open_pdf_viewer(loc, None))
            pdf_button.pack(pady=10)

        # Button to navigate back to the login screen
        back_button = Button(self.root, text="back", command=self.back_to_login)
        back_button.pack(pady=30)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.prompt_frame = tk.Frame(self.root)
        self.prompt_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Add a checkbox to toggle prompt visibility
        self.prompt_visibility_var = tk.BooleanVar(value=True)
        self.prompt_visibility_checkbox = tk.Checkbutton(self.root, text="Show Prompts",
                                                         variable=self.prompt_visibility_var,
                                                         command=self.toggle_prompts)
        self.prompt_visibility_checkbox.pack(side="top", padx=10, pady=10)

        # Add a label to display prompts
        self.prompt_label = tk.Label(self.prompt_frame, text="", font=("Arial", 12, "bold"))
        self.prompt_label.pack(side="top", padx=10, pady=5)

    def display_survey_prompt(self):
        messagebox.showinfo("Survey Prompt",
                            "SURVEY: Glance over the headings in the chapter to see the few big points.")
    # Populate the notes menu with notes connected to the selected PDF

    def toggle_prompts(self):
        if self.prompt_visibility_var.get():
            self.show_prompts()
        else:
            self.hide_prompts()

    # Show prompts
    def show_prompts(self):
        self.prompt_frame.pack()

    # Hide prompts
    def hide_prompts(self):
        self.prompt_frame.pack_forget()


    def select_pdf(self, selected_pdf):
        pdf_name = os.path.basename(selected_pdf)
        pdf_id = self.db_manager.get_pdf_id(pdf_name)
        notes = self.db_manager.get_notes(pdf_id)

        self.notes_menu['menu'].delete(0, 'end')  # Clear previous notes
        for note in notes:
            self.notes_menu['menu'].add_command(label=note, command=tk._setit(self.notes_menu_var, note))

    # Navigate back to the login screen
    def back_to_login(self):
        self.root.destroy()
        self.login_root.deiconify()


    # Open a PDF viewer window
    def open_pdf_viewer(self, original_pdf_location, highlighted_pdf_location=None):
        if hasattr(self, 'viewer'):
            self.viewer.destroy()

        self.original_pdf_location = original_pdf_location  # Store the original PDF location

        # Determine the PDF location to display
        if highlighted_pdf_location:
            pdf_location_var = highlighted_pdf_location
            self.show_highlighted_button_text = "Hide Highlighted"
            self.show_highlighted_command = self.hide_highlighted_pdf
        else:
            pdf_location_var = original_pdf_location
            self.show_highlighted_button_text = "Show Highlighted"
            self.show_highlighted_command = lambda: self.show_highlighted_pdf(pdf_name)

        # Create a Toplevel window for the PDF viewer
        self.viewer = Toplevel(self.root)
        self.viewer.title(pdf_location_var)
        self.viewer.minsize(900, 700)  # Adjusted minimum size

        # Create a frame for buttons at the top
        self.button_frame = tk.Frame(self.viewer)
        self.button_frame.pack(side="top", fill="x", padx=10, pady=10)  # Increased padding

        # Create a frame for the notes dropdown menu and other buttons
        self.top_frame = tk.Frame(self.viewer)
        self.top_frame.pack(side="top", fill="x", padx=10, pady=10)  # Increased padding

        # Create a canvas for displaying PDF pages and a vertical scrollbar
        canvas = tk.Canvas(self.viewer, width=800)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)  # padd for pdf
        scrollbar = tk.Scrollbar(self.viewer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", padx=10, pady=10)  # Increased padding
        canvas.configure(yscrollcommand=scrollbar.set)

        # Open the PDF document
        pdf_document = fitz.open(pdf_location_var)

        # Create a frame to hold PDF pages
        pdf_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=pdf_frame, anchor="nw")

        # Display each page of the PDF as an image on the canvas
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            image = page.get_pixmap()
            photo = tk.PhotoImage(data=image.tobytes("ppm"))
            label = Label(pdf_frame, image=photo)
            label.image = photo
            label.pack()

        # Update the canvas scroll region
        pdf_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Bind canvas resize event to update scroll region
        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_canvas_configure)

        # Create frame for notes
        self.notes_frame = tk.Frame(self.viewer)
        self.notes_frame.pack(side="bottom", fill="both", expand=True)  # Increased padding
        self.notes_frame.pack_propagate(0)  # Prevent automatic resizing

        # Create widgets for adding, deleting, and managing notes
        note_name_label = Label(self.top_frame, text="Note Name:")
        note_name_label.pack(side="left", padx=5)
        note_name_entry = Entry(self.top_frame)
        note_name_entry.pack(side="left", padx=5)
        self.note_name_entry = note_name_entry

        pdf_name = os.path.basename(pdf_location_var)
        pdf_id = self.db_manager.get_pdf_id(pdf_name)
        notes = self.db_manager.get_notes(pdf_id)

        self.notes_menu_var = tk.StringVar(self.top_frame)
        self.notes_menu_var.set("Select Note")
        self.notes_menu = tk.OptionMenu(self.top_frame, self.notes_menu_var, "Select Note", *notes)
        self.notes_menu.pack(side="left", padx=5)

        notes_label = Label(self.top_frame, text="Notes")
        notes_label.pack(side="left", padx=5)

        self.notes_text = Text(self.viewer, wrap=tk.WORD, height=50, width=70)  # Adjusted height and width

        # paddy for notes
        self.notes_text.pack(side="bottom", padx=5, pady=5)

        add_note_button = Button(self.top_frame, text="Save Note",
                                 command=lambda: self.add_note_to_db(pdf_id, self.note_name_entry.get(),
                                                                     self.notes_text))
        add_note_button.pack(side="left", padx=5)

        delete_note_button = Button(self.top_frame, text="Delete Note",
                                    command=lambda: self.delete_note_from_db(pdf_id))
        delete_note_button.pack(side="left", padx=5)

        load_note_button = Button(self.top_frame, text="Load Note", command=lambda: self.load_selected_note(pdf_id))
        load_note_button.pack(side="left", padx=5)


        # Create Show/Hide Highlighted button
        self.show_highlighted_button = Button(self.top_frame, text=self.show_highlighted_button_text,
                                              command=self.show_highlighted_command)
        self.show_highlighted_button.pack(side="left", padx=5)

        self.show_hide_notes_button = Button(self.top_frame, text="Hide Notes", command=self.toggle_notes)
        self.show_hide_notes_button.pack(side="left", padx=5)

        add_chapter_button = Button(self.button_frame, text="Add Chapter", command=self.add_chapter)
        add_chapter_button.pack(side="right", padx=5)  # Align to the right

        # Add Section button
        add_section_button = Button(self.button_frame, text="Add Section", command=self.add_section)
        add_section_button.pack(side="right", padx=5)  # Align to the right

        self.section_heading_label = Label(self.top_frame, text="Section Heading:")
        self.section_heading_label.pack(side="left", padx=(0, 5))  # Aligns to the left with some right padding

        self.section_heading_entry = Entry(self.top_frame)
        self.section_heading_entry.pack(side="left")  # Aligns to the left

        self.chapter_title_label = Label(self.top_frame, text="Chapter Title:")
        self.chapter_title_label.pack(side="left", padx=(0, 5))  # Aligns to the left with some right padding

        self.chapter_title_entry = Entry(self.top_frame)
        self.chapter_title_entry.pack(side="left")  # Aligns to the left

        back_button = Button(self.top_frame, text="Back", command=self.viewer.destroy)
        back_button.pack(side="right", padx=5)

        self.viewer.attributes('-topmost', False)

    # Toggle the display of notes
    def toggle_notes(self):
        if self.show_notes_flag:
            self.hide_notes()
            self.show_hide_notes_button.config(text="Show Notes")
            self.show_notes_flag = False
        else:
            self.show_notes()
            self.show_hide_notes_button.config(text="Hide Notes")
            self.show_notes_flag = True




    # Hide the notes
    def hide_notes(self):
        self.notes_text.pack_forget()

    # Show the notes
    def show_notes(self):
        self.notes_text.pack()

    # Add a note to the database
    def add_note_to_db(self, pdf_id, note_name, notes_text):
        note_text = notes_text.get("1.0", tk.END).strip()
        if note_text:
            self.db_manager.add_note(pdf_id, note_name, note_text)
            messagebox.showinfo("Note Added", "Note added successfully!")
            self.refresh_notes(pdf_id)  # Refresh the dropdown menu
        else:
            messagebox.showwarning("Empty Note", "Please enter some text for the note.")

    # Delete the selected note from the database
    def delete_note_from_db(self, pdf_id):
        note_name = self.notes_menu_var.get()  # Get the selected note's name
        if note_name == "Select Note":
            messagebox.showwarning("Select Note", "Please select a note to delete.")
            return

        confirmation = messagebox.askyesno("Delete Note", "Are you sure you want to delete this note?")
        if confirmation:
            # Assuming delete_note method accepts a note ID, and get_note_id is a method to get note ID by name
            note_id = self.db_manager.get_note_id(pdf_id, note_name)
            self.db_manager.delete_note(note_id)
            messagebox.showinfo("Note Deleted", "Note deleted successfully!")
            self.refresh_notes(pdf_id)  # Refresh the dropdown menu
            # Clear the note name entry and notes text
            self.note_name_entry.delete(0, tk.END)
            self.notes_text.delete("1.0", tk.END)

    # Refresh the dropdown menu with the latest notes from the database
    def refresh_notes(self, pdf_id):
        notes = self.db_manager.get_notes(pdf_id)
        menu = self.notes_menu['menu']
        menu.delete(0, 'end')  # Clear previous notes
        for note in notes:
            menu.add_command(label=note, command=tk._setit(self.notes_menu_var, note))
        self.notes_menu_var.set("Select Note")

    # Show the highlighted PDF if available
    def show_highlighted_pdf(self, pdf_name):
        highlighted_folder = "highlighted"
        highlighted_filename = os.path.join(highlighted_folder, pdf_name)
        if os.path.exists(highlighted_filename):
            if hasattr(self, 'highlighted_viewer'):
                self.highlighted_viewer.destroy()
                self.show_highlighted_button.config(text="Show Highlighted",
                                                    command=lambda: self.show_highlighted_pdf(pdf_name))
            else:
                self.open_pdf_viewer(self.original_pdf_location, highlighted_filename)
                self.show_highlighted_button.config(text="Hide Highlighted", command=self.hide_highlighted_pdf)
        else:
            messagebox.showinfo("Highlighted PDF Not Found", "No highlighted version of the PDF found.")

    # Hide the highlighted PDF
    def hide_highlighted_pdf(self):
        if hasattr(self, 'highlighted_viewer'):
            self.highlighted_viewer.destroy()
            self.show_highlighted_button.config(text="Show Highlighted", command=lambda: self.show_highlighted_pdf(
                os.path.basename(self.original_pdf_location)))
        else:
            self.open_pdf_viewer(self.original_pdf_location)

    # Handle closing the window
    def on_closing(self):
        self.root.destroy()
        sys.exit()

    # Load the note associated with the PDF
    def load_note(self, pdf_id):
        # Fetch and display the note associated with the PDF from the database
        note_text = self.db_manager.display_note(pdf_id)
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert(tk.END, note_text if note_text else "No notes available")

    # Load the selected note
    def load_selected_note(self, pdf_id):
        selected_note = self.notes_menu_var.get()  # Get the selected note from the dropdown menu
        if selected_note != "Select Note":
            note_name = selected_note  # Assign the selected note name to a variable
            note_text = self.db_manager.get_note_text(pdf_id, selected_note)  # Retrieve the note text from the database
            if note_text:
                self.notes_text.delete(1.0, tk.END)  # Clear the existing text
                self.notes_text.insert(tk.END, note_text)  # Insert the retrieved note text
                # Load the name of the selected note into the name text field
                self.note_name_entry.delete(0, tk.END)  # Clear the existing text
                self.note_name_entry.insert(tk.END, note_name)  # Insert the selected note name
            else:
                messagebox.showwarning("Note Not Found", "Selected note not found.")
        else:
            messagebox.showwarning("Note Not Selected", "Please select a note to load.")
            messagebox.showwarning("Note Not Selected", "Please select a note to load.")

    def add_chapter(self):
        if hasattr(self, 'viewer'):
            chapter_title = self.chapter_title_entry.get()
            if chapter_title:
                # Calculate the number of spaces needed to center the text
                num_spaces = (self.notes_text['width'] - len(chapter_title)) // 2
                # Add the chapter title with a line above and below it, centered within the notes textbox
                self.notes_text.insert(tk.END, f"{'-' * self.notes_text['width']}\n"
                                               f"{' ' * num_spaces}{chapter_title}\n"
                                               f"{'-' * self.notes_text['width']}\n\n")
                # Inform the user
                messagebox.showinfo("Chapter Added", f"Chapter '{chapter_title}' added to notes successfully!")
            else:
                messagebox.showwarning("Empty Chapter Title", "Please enter a chapter title.")
        else:
            messagebox.showwarning("PDF Viewer Not Active", "Please open a PDF viewer to add a chapter.")

    def add_section(self):
        if hasattr(self, 'viewer'):
            section_heading = self.section_heading_entry.get()
            if section_heading:
                # Add the section heading to the notes textbox
                self.notes_text.insert(tk.END, f"\n\n{section_heading}:\n\n")
                # Inform the user
                messagebox.showinfo("Section Added", "Section '{}' added successfully!".format(section_heading))
            else:
                messagebox.showwarning("Empty Section Heading", "Please enter a section heading.")
        else:
            messagebox.showwarning("PDF Viewer Not Active", "Please open a PDF viewer to add a section.")

    def toggle_prompts(self):
        if self.prompt_visibility_var.get():
            self.show_prompts()
            self.display_random_survey_prompt()  # Display a random prompt when the checkbox is checked
        else:
            self.hide_prompts()

    # Show prompts
    def show_prompts(self):
        self.prompt_frame.pack()

    # Hide prompts
    def hide_prompts(self):
        self.prompt_frame.pack_forget()

    # Display prompts for each step of SQ3R
    def display_random_survey_prompt(self):
        prompts = [
            "SQ3R: Survey - Quickly scan chapter headings and summary paragraph to grasp main ideas.",
            "SQ3R: Question - Formulate questions from headings to focus reading and aid comprehension.",
            "SQ3R: Read - Actively search for answers while reading each section.",
            "SQ3R: Recite - Summarize section content in your own words to reinforce understanding.",
            "SQ3R: Review - Review notes to understand relationships and test memory by recalling main points."
        ]
        random_prompt = random.choice(prompts)  # Select a random prompt from the list
        self.prompt_label.config(text=random_prompt)
    # Main function to start the application



if __name__ == "__main__":
    root = tk.Tk()
    root.login_screen = LoginScreen(root)
    root.mainloop()