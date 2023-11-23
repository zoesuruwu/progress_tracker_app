## Progress Tracker app in Python

This repo walks through the back-and-forth process of creating a simple progress tracker app with the use of [phind](https://www.phind.com/) and [ChatGPT](https://chat.openai.com/). Parts of conversations and adjustments of the prompt response will be included in this project. 

This app keeps track of the hours spent on learning a skill every day and plots the bar chart over the progress over time. It also allows the user to adjust the hours on a given date and skill.

### Contents

This repo is organized as follows:
```baseh
progress_checker_classes
│   README.md
│   main.py
|   database.py
|   edit_dialog.py
|   plotting.py
|   progress_tracker.py
|   constants.py
|   progress_tracker.db
│   requirements.txt 
|___images
```

### Setup
You can run all the contents of this repo using the packages provided in requirements.txt.

In a new virtualenv, run this:

```python
pip install -r requirements.txt
```

Additionally, this project will create a database with a table in the current directory. Creating a new table is only needed the first time running this app. Please modify the 7th line of code **main.py**  from *True* to *False*, after the first execution of script.

```python
app = ProgressTrackerApp(root, app = ProgressTrackerApp(root, erase_start_over=True))
```

### My experience with phind:

#### Attempt #1

<details>
  <summary>Click me</summary>
  
##### Prompt:

```baseh
How to write an application in python for a progress tracker, the goal of this app is to record how many hours I have spent learning a skill. The specifics of the application include: 

1. The application will show the added-up hours of learning a skill across days after logging hours daily.
2. I can define the skill for this progress and see the title.
```
##### Response:

```baseh
To create a progress tracker application in Python, we can follow these steps:

1. Create a User Interface (UI): We can use a library like Tkinter to create a simple UI that will pop up whenever you open your laptop. The UI will have options to input the skill you are learning, the number of hours spent learning, and a button to log the hours.

2. Store the Data: We can use a database or a simple file to store the data. We can use the sqlite3 module in Python to create a simple SQLite database.

3. Display the Progress: We can create a function to calculate and display the total hours spent on each skill.

Please note that this is a basic implementation and there are many ways to improve it. For example, you could add error checking, allow for editing and deleting of entries, or add a graphical representation of the progress.
```
##### Code snippet:

```python
import tkinter as tk
import sqlite3

def create_table():
   conn = sqlite3.connect('progress_tracker.db')
   c = conn.cursor()
   # Drop the GEEK table if already exists.
   c.execute("DROP TABLE IF EXISTS progress")
   c.execute('''CREATE TABLE progress   
                (skill text, hours real)''')
   print("Table is Ready")
   conn.close()

def log_hours():
   skill = skill_entry.get()
   hours = float(hours_entry.get())
   conn = sqlite3.connect('progress_tracker.db')
   c = conn.cursor()
   c.execute("INSERT INTO progress VALUES (?,?)", (skill, hours))
   conn.commit()
   display_progress()
   conn.close()

def display_progress():
   conn = sqlite3.connect('progress_tracker.db')
   c = conn.cursor()
   c.execute("SELECT skill, SUM(hours) FROM progress GROUP BY skill")
   rows = c.fetchall()
   for row in rows:
       print(f"Skill: {row[0]}, Total Hours: {row[1]}")
   conn.close()


root = tk.Tk()
root.title("Progress Tracker")

skill_label = tk.Label(root, text="Skill")
skill_label.pack()

skill_entry = tk.Entry(root)
skill_entry.pack()

hours_label = tk.Label(root, text="Hours")
hours_label.pack()

hours_entry = tk.Entry(root)
hours_entry.pack()

log_button = tk.Button(root, text="Log Hours", command=log_hours)
log_button.pack()

def main():
    create_table()
    root.mainloop()

if __name__ == "__main__":
    main()

```
##### Result:
![1](/images/phind.png)

##### Reflection

- I noticed that for function **def log_hours()**, it doesn't take into account the requirement of *total hours spent on each skill across days*. Instead, the function tries to overwrite hours with each logging. 
- It suggests further improvements on the functionality of the app which I found useful: 
    1. error checking
    2. allow for editing entries
    3. add a graphical representation of the progress

- The app doesn't show the logged hours for each skill, instead the function **def display_progress()** only prints out the progress in the terminal, therefore I move on to ChatGPT and ask the exactly same question.
</details>

### My experience with ChatGPT:

#### Attempt #1

<details>
  <summary>Click me</summary>

##### Prompt:

```baseh
How to write an application in python for a progress tracker, the goal of this app is to record how many hours I have spent learning a skill. The specifics of the application include: 

1. The application will show the added-up hours of learning a skill across days after logging hours daily.
2. I can define the skill for this progress and see the title.
```

##### Response:
```baseh
Here are the specific features you requested:

- Skill Selection: The user can select a skill they want to track the progress of.

- Record Hours: The user can input the number of hours spent learning the selected skill.

- View Progress: The user can view their progress for each skill, including the total hours spent. 
   1. The progress is stored with the date, and the application accumulates the hours for each skill across days.
   2. The app will show the skill selection, hours input, and progress table

- Store Data: The application should store the data in an SQLite database for persistence.

```
##### Code snippet:
```python
import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
from datetime import date

def create_table():
   conn = sqlite3.connect('progress_tracker.db')
   c = conn.cursor()
   # Drop the GEEK table if already exists.
   c.execute("DROP TABLE IF EXISTS progress")
   c.execute('''CREATE TABLE progress   
                (skill text, hours real)''')
   print("Table is Ready")
   conn.close()

# Function to add hours to the selected skill
def add_hours():
    skill = skill_var.get()
    hours = float(hours_entry.get())

    if skill and hours > 0:
        conn = sqlite3.connect("progress_tracker.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS progress (skill TEXT, hours REAL, date TEXT)")

        today = date.today().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO progress VALUES (?, ?, ?)", (skill, hours, today))
        conn.commit()
        conn.close()

        update_progress_table()
        hours_entry.delete(0, tk.END)

# Function to update the progress table
def update_progress_table():
    conn = sqlite3.connect("progress_tracker.db")
    df = pd.read_sql_query("SELECT skill, SUM(hours) as total_hours FROM progress GROUP BY skill", conn)
    conn.close()

    progress_tree.delete(*progress_tree.get_children())

    for _, row in df.iterrows():
        progress_tree.insert("", "end", values=(row["skill"], row["total_hours"]))

# Create the main window
root = tk.Tk()
root.title("Progress Tracker")
root.geometry("400x400")

# Skill selection
skill_label = tk.Label(root, text="Select Skill:")
skill_label.pack()
skills = ["Python", "Java", "JavaScript", "SQL", "Machine Learning"]
skill_var = tk.StringVar()
skill_combobox = ttk.Combobox(root, textvariable=skill_var, values=skills)
skill_combobox.pack()

# Hours input
hours_label = tk.Label(root, text="Hours Spent:")
hours_label.pack()
hours_entry = tk.Entry(root)
hours_entry.pack()

# Add Hours button
add_button = tk.Button(root, text="Add Hours", command=add_hours)
add_button.pack()

# Progress table
progress_tree = ttk.Treeview(root, columns=("Skill", "Total Hours"))
progress_tree.heading("Skill", text="Skill")
progress_tree.heading("Total Hours", text="Total Hours")

def main():
    create_table()
    # Update the progress table
    update_progress_table()
    root.mainloop()

if __name__ == "__main__":
    main()
```
#### Result:
After clicking Add Hours, an error occurred and the app failed. 

![2](/images/chat_1.png)

#### Reflection: 
1. One thing to take away from this attempt is the drop box of 'Select Skill' that predefined skills of my interest.

2. I found out the reason for this error comes from the created table missing one column 'Date'. The logging hour to database functionality failed, and therefore the anticipated progress bar also didn't pop up. I later added a new column in **def create_table()** myself.

</details>

#### Attempt #2

<details>
  <summary>Click me</summary>

To clarify, I will need two data-presentation for logged_hours. Firstly, I want to be able to add up hours if I log the same skill today(or same day in the future) in a progress table. Secondly, I want a bar chart showing the history of hours spent learning each skill. Some back and forth questions revolve on the bar chart layout, those are elaborated in point 4 and 5 in the following prompt. It took me 2 hours to arrive at a satisfactory result.

##### Prompt:

```baseh
Now I will update the requirements:

1. The application should show the accumulated hours of learning a skill until today in the progress table.

2. In the UI, I want to have a button labeled 'show history'. After hitting the button, show me a bar graph of the past days' hours spent learning the skill, with the x-axis the date and the y-axis the hour. Use subplots to show for each skill, hours spent across dates. The previous plots need to be cleared and updated each time clicking the button.

3. In the function add_hours(), I would like to be able to add hours up if today I have already logged the hours, and now I am doing it a second time, in the evening for example.

4. How to adjust the code such that this will not give an error for plt.subplot if only logged one skill. 

5. If I add the second skill with hours, and click on the button Show History, then the plot still only show the first skill. Tell me what went wrong and how to fix it.

```

##### Response:
```baseh
1. The update_progress_table function will now fetch and display data for skills, total hours, and dates. 

2. We added a "Show History" button that, when clicked, will retrieve the latest unique skills from the database, to accommadate further logging to database. And then plot bar graphs for all unique skills in the database of the past days' hours spent learning. The function will create separate subplots, each containing a bar plot for a specific skill.

3. To add hours to an existing entry for the same day in the add_hours() function, you can first check if a record with the same skill and date already exists in the database. If it does, you can update the existing record by adding the new hours to the previous hours for that day. If no record exists, we insert a new record with the current date.

Now, when you open the application, it will pop up on your laptop screen, and you can log hours, select a skill, and view the history of hours spent in a bar graph by clicking the "Show History" button.

```

##### Code snippet:
```python
import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Function to create the database table
def create_table():
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    # Drop the table if it already exists
    c.execute("DROP TABLE IF EXISTS progress")
    c.execute('''CREATE TABLE progress   
                (skill text, hours real, date text)''')
    print("Table is Ready")
    conn.close()

# Function to update the progress table in the UI
def update_progress_table():
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

    # Add columns for Skill, Total Hours, and Date
    progress_tree['columns'] = ("Skill", "Summed Total Hours", "Date")
    progress_tree.heading("Skill", text="Skill")
    progress_tree.heading("Summed Total Hours", text="Summed Total Hours")
    progress_tree.heading("Date", text="Date")

    for _, row in df.iterrows():
        progress_tree.insert("", "end", values=(row["skill"], row["summed_total_hours"], row["date"]))

# Function to add hours to the selected skill
def add_hours():
    skill = skill_var.get()
    hours = float(hours_entry.get())
    if skill and hours > 0:
        conn = sqlite3.connect("progress_tracker.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS progress (skill TEXT, hours REAL, date TEXT)")

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
        update_progress_table()
        hours_entry.delete(0, tk.END)

# Function to show the history in a bar graph
def show_history():
    conn = sqlite3.connect("progress_tracker.db")
    query = """
    SELECT skill, date, SUM(hours) as total_hours
    FROM progress
    GROUP BY skill, date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Get unique skills
    unique_skills = df["skill"].unique()

    # Clear the previous plots and re-create subplots
    for ax in axes:
        ax.clear()

    if len(unique_skills) == 1:
        # If there's only one skill, create a single subplot
        skill_data = df[df["skill"] == unique_skills[0]]
        ax = fig.add_subplot(111)
        ax.bar(skill_data["date"], skill_data["total_hours"])
        ax.set_ylabel("Hours", fontsize=6)
        ax.set_title(f"Skill: {unique_skills[0]}", fontsize=7)
        ax.tick_params(axis="y", labelsize=6)
        ax.tick_params(axis="x", rotation=45, labelsize=6)
    else:
        # If there are multiple skills, create separate subplots with shared x-axis
        fig.clear()
        axes.clear()
        for i, skill in enumerate(unique_skills):
            ax = fig.add_subplot(len(unique_skills), 1, i + 1)
            skill_data = df[df["skill"] == skill]
            ax.bar(skill_data["date"], skill_data["total_hours"])
            ax.set_ylabel("Hours", fontsize=6)
            ax.set_title(f"Skill: {skill}", fontsize=7)
            ax.tick_params(axis="y", labelsize=6)
            ax.tick_params(axis="x", rotation=45, labelsize=6)
            axes.append(ax)

    # Automatically adjust layout for better readability and increase spacing between subplots
    fig.tight_layout(pad=10.0)

    # Update the canvas with the new figure
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("Progress Tracker")
root.geometry("800x600")

# Skill selection
skill_label = tk.Label(root, text="Select Skill:")
skill_label.pack()
skills = ["Python", "Java", "JavaScript", "SQL", "Machine Learning"]
skill_var = tk.StringVar()
skill_combobox = ttk.Combobox(root, textvariable=skill_var, values=skills)
skill_combobox.pack()

# Hours input
hours_label = tk.Label(root, text="Hours Spent:")
hours_label.pack()
hours_entry = tk.Entry(root)
hours_entry.pack()

# Add Hours button
add_button = tk.Button(root, text="Add Hours", command=add_hours)
add_button.pack()

# Show History button
show_history_button = tk.Button(root, text="Show History", command=show_history)
show_history_button.pack()

# Progress table
progress_tree = ttk.Treeview(root, columns=("Skill", "Total Hours", "Date"))
progress_tree.heading("Skill", text="Skill")
progress_tree.heading("Total Hours", text="Total Hours")
progress_tree.heading("Date", text="Date")
progress_tree.pack()

# Create a global Figure and a Canvas for Matplotlib
fig = Figure(figsize=(25, 20))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create a global list to store subplot axes
axes = []


def main():
    create_table()
    # Update the progress table in the UI
    update_progress_table()

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
```
##### Result:

![Alt text](/images/chat_2.png)

##### Reflection:
1. ChatGPT didn't understand at the first try, the sequence of events that need to happen and coordinate very well when I log new skills and click the button 'Show History', in order to see the updated version of the table in the database.

</details>

#### Attempt #3

<details>
  <summary>Click me</summary>
  
An additional feature to edit data hours for a given skill and date. 
##### Prompt:

```baseh
Now, I want to add a feature that for example, I made a mistake in the hours written. Can you suggest what can be the solution to edit the past logged hours? 

Place the button of 'Edit hours' under the 'Show History' button. After clicking the button, it will pop up another table to show all data entry in the database table where I can modify the data entry and update to the database.
```

##### Response:
```
To allow users to edit past logged hours, you can implement an edit feature in your application.

1. When the user clicks the "Edit" button for a specific entry, open a dialog or a new window that allows them to edit the hours for that entry.

2. After editing, click the "Save" button to update the database and refresh the UI to reflect changes in the progress table.
```

##### Code snippet:
```python
import tkinter as tk
from tkinter import ttk
import sqlite3
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Function to create the database table
def create_table():
    conn = sqlite3.connect('progress_tracker.db')
    c = conn.cursor()
    # Drop the table if it already exists
    c.execute("DROP TABLE IF EXISTS progress")
    c.execute('''CREATE TABLE progress   
                (skill text, hours real, date text)''')
    print("Table is Ready")
    conn.close()

# Function to update the progress table
def update_progress_table():
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

# Function to add hours to the selected skill
def add_hours():
    skill = skill_var.get()
    hours = float(hours_entry.get())
    if skill and hours > 0:
        conn = sqlite3.connect("progress_tracker.db")
        cursor = conn.cursor()

        # cursor.execute("CREATE TABLE IF NOT EXISTS progress (skill TEXT, hours REAL, date TEXT)")

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
        update_progress_table()
        hours_entry.delete(0, tk.END)

# Function to show the history in a bar graph
def show_history():
    conn = sqlite3.connect("progress_tracker.db")
    query = """
    SELECT skill, date, SUM(hours) as total_hours
    FROM progress
    GROUP BY skill, date
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Get unique skills
    unique_skills = df["skill"].unique()

    # Clear the previous plots and re-create subplots
    for ax in axes:
        ax.clear()

    if len(unique_skills) == 1:
        # If there's only one skill, create a single subplot
        skill_data = df[df["skill"] == unique_skills[0]]
        ax = fig.add_subplot(111)
        ax.bar(skill_data["date"], skill_data["total_hours"])
        ax.set_ylabel("Hours", fontsize=6)
        ax.set_title(f"Skill: {unique_skills[0]}", fontsize=7)
        ax.tick_params(axis="y", labelsize=6)
        ax.tick_params(axis="x", rotation=45, labelsize=6)
    else:
        # If there are multiple skills, create separate subplots with shared x-axis
        fig.clear()
        axes.clear()
        for i, skill in enumerate(unique_skills):
            ax = fig.add_subplot(len(unique_skills), 1, i + 1)
            skill_data = df[df["skill"] == skill]
            ax.bar(skill_data["date"], skill_data["total_hours"])
            ax.set_ylabel("Hours", fontsize=6)
            ax.set_title(f"Skill: {skill}", fontsize=7)
            ax.tick_params(axis="y", labelsize=6)
            ax.tick_params(axis="x", rotation=45, labelsize=6)
            axes.append(ax)

    # Automatically adjust layout for better readability and increase spacing between subplots
    fig.tight_layout(pad=10.0)

    # Update the canvas with the new figure
    canvas.draw()

# Function to open the edit dialog
def open_edit_dialog():
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Hours")

    # Fetch all data from the database table
    conn = sqlite3.connect("progress_tracker.db")
    query = "SELECT skill, date, hours FROM progress"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Create a Treeview widget for displaying the data
    edit_tree = ttk.Treeview(edit_window, columns=("Skill", "Date", "Hours"))
    edit_tree.heading("Skill", text="Skill")
    edit_tree.heading("Date", text="Date")
    edit_tree.heading("Hours", text="Hours")
    edit_tree.pack()

    # Insert data into the Treeview
    for _, row in df.iterrows():
        edit_tree.insert("", "end", values=(row["skill"], row["date"], row["hours"]))

    # Create an entry field for editing hours
    tk.Label(edit_window, text="Edit Hours:").pack()
    edited_hours_entry = tk.Entry(edit_window)
    edited_hours_entry.pack()

    # Update selected hours in the database and refresh the UI
    def save_edited_hours():
        selected_item = edit_tree.selection()[0]
        edited_hours = float(edited_hours_entry.get())
        selected_skill = edit_tree.item(selected_item, "values")[0]
        selected_date = edit_tree.item(selected_item, "values")[1]

        conn = sqlite3.connect("progress_tracker.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE progress SET hours = ? WHERE skill = ? AND date = ?", (edited_hours, selected_skill, selected_date))
        conn.commit()
        conn.close()

        edit_window.destroy()
        update_progress_table()

    tk.Button(edit_window, text="Save", command=save_edited_hours).pack()

# Create the main window
root = tk.Tk()
root.title("Progress Tracker")
root.geometry("800x600")

# Skill selection
skill_label = tk.Label(root, text="Select Skill:")
skill_label.pack()
skills = ["Python", "Java", "JavaScript", "SQL", "Machine Learning"]
skill_var = tk.StringVar()
skill_combobox = ttk.Combobox(root, textvariable=skill_var, values=skills)
skill_combobox.pack()

# Hours input
hours_label = tk.Label(root, text="Hours Spent:")
hours_label.pack()
hours_entry = tk.Entry(root)
hours_entry.pack()

# Add Hours button
add_button = tk.Button(root, text="Add Hours", command=add_hours)
add_button.pack()

# Show History button
show_history_button = tk.Button(root, text="Show History", command=show_history)
show_history_button.pack()

# Edit Hours button
edit_hours_button = tk.Button(root, text="Edit Hours", command=open_edit_dialog)
edit_hours_button.pack()

# Progress table
progress_tree = ttk.Treeview(root, columns=("Skill", "Total Hours", "Date"))
progress_tree.heading("Skill", text="Skill")
progress_tree.heading("Total Hours", text="Total Hours")
progress_tree.heading("Date", text="Date")
progress_tree.pack()

# Create a global Figure and a Canvas for Matplotlib
fig = Figure(figsize=(25, 20))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Create a global list to store subplot axes
axes = []

def main():
    # create_table()
    # Update the progress table in the UI
    update_progress_table()

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()

```
##### Result: 
The progress app:

![Alt text](/images/chat_3_progress.png)

Edit hour window after clicking the button 'Edit Hours':

![Alt text](/images/chat_3_edit.png)

##### Reflection:
The bar charts sometimes overlap, and it is hard to read the date and skill. Also, as we have noticed, the script becomes too long and not organized.

</details>

#### Attempt #4 (end)

<details>
  <summary>Click me</summary>


In this attempt, I will break into several scripts and use Object-Oriented-Programming such as classes. Moreover, I will add error checking feature to the function **def log_hours()**.


##### Prompt:

```baseh
1. Suggest how to break this long script into either classes or into different scripts

2. Sugguest ways to add error checking on the function add_hours, to show error for input with empty string and non-numeric and non-positive number.

3. Tidy up the subplots such that the x-axis doesn't overlap with title of above plots. And make the titles of subplots to the left of the y-axis.
```

##### Response:

```baseh
Here's how you can organize your code into separate sections, each corresponding to a specific module or class:

1. Main Application Script (main.py)
2. Progress Tracker Application Class (progress_tracker.py)
3. Database Module (database.py)
4. Graph Plotting Module (plotting.py)
5. Edit Dialog Module (edit_dialog.py)

Next, for error checking:

We check if the skill is a valid string by ensuring it's not empty or consisting of only whitespace characters. If it's not valid, we display an error message and return early.

We try to convert the input hours_str to a float and check if it's a positive number. If the conversion fails (e.g., if the input contains letters), we display an error message for non-numeric input. If the value is not positive, we display an error message for non-positive input.

If the input is valid, the function proceeds with adding the hours and updating the progress table.

If there's an error, we display an error message using tk.messagebox.showerror to inform the user about the issue.
```

##### Code snippet:
Those scripts are in this git repo, I won't explicitly show here.

##### Result:
![Alt text](/images/end_result.png)

When **Hours Spent** is not valid:

![Alt text](/images/end_result_error.png)

##### Reflection:
I have logged hours in two consecutive dates, and it seems to work just fine. Furthermore, improvements for the app such as deletion of data entries will be nice, but not implemented at the moment.

</details>