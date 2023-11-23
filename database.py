import sqlite3
import pandas as pd
from datetime import date
import tkinter as tk

def create_table():
    # This function creates the database table when requested
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    # Drop the table if it already exists
    c.execute("DROP TABLE IF EXISTS progress")
    c.execute('''CREATE TABLE progress   
                (skill text, hours real, date text)''')
    print("Table is Ready")
    conn.close()

def update_progress_table(progress_tree):
    # This function updates the progress table in the UI
    conn = sqlite3.connect("progress_tracker.db")
    query = """
    SELECT skill, MAX(date) AS date, SUM(hours) AS summed_total_hours
    FROM progress
    GROUP BY skill
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Clear the current table
    progress_tree.delete(*progress_tree.get_children())

    # Add columns for Skill, Total Hours, Date
    progress_tree['columns'] = ("Skill", "Summed Total Hours", "Date")
    progress_tree.heading("Skill", text="Skill")
    progress_tree.heading("Summed Total Hours", text="Summed Total Hours")
    progress_tree.heading("Date", text="Date")

    for _, row in df.iterrows():
        skill = row["skill"]
        total_hours = row["summed_total_hours"]
        date = row["date"]

        progress_tree.insert("", "end", values=(skill, total_hours, date))

    
def add_hours(skill, hours, progress_tree, hours_entry):
    # This function adds hours to the selected skill tothe database table and update the progress table in the UI
    
    if skill and hours > 0:
        conn = sqlite3.connect("progress_tracker.db")
        cursor = conn.cursor()

        # Check if a record with the same skill exists in the past
        cursor.execute("SELECT hours, date FROM progress WHERE skill = ? ORDER BY date DESC LIMIT 1", (skill,))
        existing_data = cursor.fetchone()
        today = date.today().strftime("%Y-%m-%d")
        if existing_data and (existing_data[1] == date.today().strftime("%Y-%m-%d")):
            # If a record exists for today, add the new hours to the existing hours
            new_hours = existing_data[0] + hours
            cursor.execute("UPDATE progress SET hours = ?, date = ? WHERE skill = ?", (new_hours, today, skill))
        else:
            # If no record exists at all or only today, insert a new record with the current date
            today = date.today().strftime("%Y-%m-%d")
            cursor.execute("INSERT INTO progress VALUES (?, ?, ?)", (skill, hours, today))
        conn.commit()
        conn.close()

        # Update the progress table in the UI
        update_progress_table(progress_tree)
        hours_entry.delete(0, tk.END)