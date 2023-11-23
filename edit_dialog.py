import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
from database import update_progress_table

class EditDialog:
    """
    This class perform the functionality of editing hours given a user's choice of skill and date
    """
    def __init__(self, parent, progress_tree):
        # Function to open the edit dialog
        self.edit_window = tk.Toplevel(parent)
        self.edit_window.title("Edit Hours")
        self.progress_tree = progress_tree

        # Fetch all data from the database table
        conn = sqlite3.connect("progress_tracker.db")
        query = "SELECT skill, date, hours FROM progress"
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Create a Treeview widget for displaying the data
        self.edit_tree = ttk.Treeview(self.edit_window, columns=("Skill", "Date", "Hours"))
        self.edit_tree.heading("Skill", text="Skill")
        self.edit_tree.heading("Date", text="Date")
        self.edit_tree.heading("Hours", text="Hours")
        self.edit_tree.pack()

        # Insert data into the Treeview
        for _, row in df.iterrows():
            self.edit_tree.insert("", "end", values=(row["skill"], row["date"], row["hours"]))

        # Create an entry field for editing hours
        tk.Label(self.edit_window, text="Edit Hours:").pack()
        self.edited_hours_entry = tk.Entry(self.edit_window)
        self.edited_hours_entry.pack()

        # Update selected hours in the database and refresh the UI
        tk.Button(self.edit_window, text="Save", command=self.save_edited_hours).pack()

    def open(self):
        self.edit_window.deiconify()

    def save_edited_hours(self):
        # This function save the changes to hours to the database table
        selected_item = self.edit_tree.selection()[0]
        edited_hours = float(self.edited_hours_entry.get())
        selected_skill = self.edit_tree.item(selected_item, "values")[0]
        selected_date = self.edit_tree.item(selected_item, "values")[1]
        conn = sqlite3.connect("progress_tracker.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE progress SET hours = ? WHERE skill = ? AND date = ?", (edited_hours, selected_skill, selected_date))
        conn.commit()
        conn.close()

        self.edit_window.destroy()
        update_progress_table(self.progress_tree)
        