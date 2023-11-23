from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import pandas as pd

def show_history(fig, canvas, axes):
    # This function show the history hours spent on a given skill in a bar graph.
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
        ax.tick_params(axis="x", rotation=0, labelsize=6)
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
            ax.tick_params(axis="x", rotation=0, labelsize=6)
            axes.append(ax)
            # Manually adjust the position of the subplot title
            ax.title.set_position([-0.1, 0.3])


    # Manually adjust the overall layout to provide more space for titles
    fig.subplots_adjust(top=0.92, hspace=1)  # Increase top margin and vertical spacing


    # Update the canvas with the new figure
    canvas.draw()