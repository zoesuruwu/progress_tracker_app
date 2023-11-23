import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import create_table, update_progress_table, add_hours
from plotting import show_history
from edit_dialog import EditDialog
from constants import APP_TITLE, APP_SIZE, LIST_SKILLS

class ProgressTrackerApp:
    """
    This class stores all attributes in the Progress tracker app(UI), and perform tasks such as 
    1. add hours to a given skill today 
    2. update the progress table in UI to show the summed total hours spent on any skills a user has recorded up to today
    3. show history in a bar chart for the hours spent on each skill
    4. edit hours to make changes to the recorded hours, in the case of revision
    """
    def __init__(self, root, erase_start_over):
        self.root = root
        root.title(APP_TITLE)
        root.geometry(APP_SIZE)

        # skill selection
        self.skill_label = tk.Label(root, text="Select skill:")
        self.skill_label.pack()
        self.skills = LIST_SKILLS
        self.skill_var = tk.StringVar()
        self.skill_combobox = ttk.Combobox(root, textvariable = self.skill_var,values = self.skills )
        self.skill_combobox.pack()

        # Hour input
        self.hours_label = tk.Label(root, text = "Hours Spent:")
        self.hours_label.pack()
        self.hours_entry = tk.Entry(root)
        self.hours_entry.pack()

        # Add Hours button
        self.add_button = tk.Button(root, text = "Add Hours", command = self.add_hours) # add_hours method
        self.add_button.pack()

        # Show History button - plots
        self.show_history_button = tk.Button(root, text = "Show History", command = self.show_history) # show_history method
        self.show_history_button.pack()

        # Edit hours button
        self.edit_hours_button = tk.Button(root, text="Edit Hours", command=self.open_edit_dialog) # open_edit_dialog method
        self.edit_hours_button.pack()

        # Progress table
        self.progress_tree = ttk.Treeview(root, columns = ("Skill", "Total Hours", "Date"))
        self.progress_tree.heading("Skill", text = "Skill")
        self.progress_tree.heading("Total Hours", text = "Total Hours")
        self.progress_tree.heading("Date", text = "Date")
        self.progress_tree.pack()

        # Create a global Figure and a Canvas for Matplotlib
        self.fig = Figure(figsize=(25, 20))
        self.canvas = FigureCanvasTkAgg(self.fig, master = root)
        self.canvas.get_tk_widget().pack()

        # Create a global list to store subplot axes
        self.axes = []

        # Initialize database and setup UI
        if erase_start_over:
            create_table()
        self.update_progress_table()

    def run(self):
        # Start the main event loop
        self.root.mainloop()

    def update_progress_table(self):
        # Function to update the progress table
        update_progress_table(self.progress_tree)
    
    def add_hours(self):
        # Function to add hours to the selected skill
        skill = self.skill_var.get()
        hours_str = self.hours_entry.get()
        
        # Check if the skill is a valid string
        if not skill.strip():
            tk.messagebox.showerror("Error", "Skill must be a non-empty string")
            return

        # Check if hours is a valid positive number
        try:
            hours = float(hours_str)
            add_hours(skill, hours, self.progress_tree, self.hours_entry)
            if hours <= 0:
                tk.messagebox.showerror("Error", "Hours must be a positive number")
                return
        except ValueError:
            tk.messagebox.showerror("Error", "Hours must be a numeric value")
            return
        

    def show_history(self):
        # Function to show the history in a bar graph
        show_history(self.fig, self.canvas, self.axes)

    def open_edit_dialog(self):
        # Function to open the edit dialog
        edit_dialog = EditDialog(self.root, self.progress_tree)
        edit_dialog.open()