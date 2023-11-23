import tkinter as tk
from progress_tracker import ProgressTrackerApp

if __name__ == "__main__":

    root = tk.Tk()
    app = ProgressTrackerApp(root, erase_start_over=True) # if to create a new table in the database, then set to True
    app.run()