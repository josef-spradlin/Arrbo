import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import sqlite3
import subprocess

# Function to update Deff_Eff table
def update_deff_eff():
    try:
        subprocess.run(["python", "deff_eff.py"], check=True)
        messagebox.showinfo("Success", "Deff_Eff table updated successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error updating Deff_Eff table: {e}")

# Function to update Positions table
def update_positions():
    try:
        subprocess.run(["python", "positions.py"], check=True)
        messagebox.showinfo("Success", "Positions table updated successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error updating Positions table: {e}")

# Function to update Usage table

def update_usage():
    try:
        subprocess.run(["python", "usage.py"], check=True)
        messagebox.showinfo("Success", "Usage table updated successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error updating Usage table: {e}")

def get_team_data(team1_name, team2_name):
    try:
        # Connect to the database
        conn = sqlite3.connect('arrbo.db')
        cursor = conn.cursor()

        # Fetch team ids based on team names
        cursor.execute('''SELECT team_id FROM nba_teams WHERE team_name = ?''', (team1_name,))
        team1_id = cursor.fetchone()
        cursor.execute('''SELECT team_id FROM nba_teams WHERE team_name = ?''', (team2_name,))
        team2_id = cursor.fetchone()

        if not team1_id or not team2_id:
            messagebox.showerror("Error", "Data not found for selected teams!")
            return

        team1_id = team1_id[0]
        team2_id = team2_id[0]

        # Fetch top 2 usage players for team1
        cursor.execute('''SELECT player1_name, player1_usage, player2_name, player2_usage
                          FROM top_usage_players
                          WHERE team_id = ?''', (team1_id,))
        team1_data = cursor.fetchone()

        # Fetch top 2 usage players for team2
        cursor.execute('''SELECT player1_name, player1_usage, player2_name, player2_usage
                          FROM top_usage_players
                          WHERE team_id = ?''', (team2_id,))
        team2_data = cursor.fetchone()

        if not team1_data or not team2_data:
            messagebox.showerror("Error", "Data not found for selected teams!")
            return

        # Fetch defensive efficiency data for both teams (player positions not included)
        cursor.execute('''SELECT pg_efficiency, sg_efficiency, sf_efficiency, pf_efficiency
                          FROM defensive_efficiency
                          WHERE team_id = ?''', (team1_id,))
        team1_def_eff = cursor.fetchone()

        cursor.execute('''SELECT pg_efficiency, sg_efficiency, sf_efficiency, pf_efficiency
                          FROM defensive_efficiency
                          WHERE team_id = ?''', (team2_id,))
        team2_def_eff = cursor.fetchone()

        if not team1_def_eff or not team2_def_eff:
            messagebox.showerror("Error", "Defensive efficiency data not found!")
            return

        # Define a function to get the defensive efficiency for a player position
        def get_def_eff(position, def_eff):
            if position == 'PG':
                return def_eff[0]  # PG Efficiency
            elif position == 'SG':
                return def_eff[1]  # SG Efficiency
            elif position == 'SF':
                return def_eff[2]  # SF Efficiency
            elif position == 'PF':
                return def_eff[3]  # PF Efficiency
            elif position == 'G':  # Guard - Average PG and SG
                return (def_eff[0] + def_eff[1]) / 2
            elif position == 'F':  # Forward - Average SF and PF
                return (def_eff[2] + def_eff[3]) / 2
            return 0  # Default in case of error

        # Define a function to fetch player positions using their name from positions table
        def get_player_position(player_name, team_id):
            # Fetch player position from the positions table (we join with top_usage_players to determine the team)
            cursor.execute('''SELECT p.player_position
                              FROM positions p
                              JOIN top_usage_players tup ON p.player_name = tup.player1_name OR p.player_name = tup.player2_name
                              WHERE tup.team_id = ? AND (p.player_name = ? OR p.player_name = ?)''', (team_id, player_name, player_name))
            player_position = cursor.fetchone()
            return player_position[0] if player_position else None

        # Now process the analysis for both teams
        team1_analysis = []
        team2_analysis = []

        # Analyzing team 1 players
        for player_name, player_usage in [(team1_data[0], team1_data[1]), (team1_data[2], team1_data[3])]:
            player_position = get_player_position(player_name, team1_id)
            if player_position:
                # Get defensive efficiency of team2 against this player's position
                team2_def_eff_value = get_def_eff(player_position, team2_def_eff)
                team1_analysis.append(f"{player_name} ({player_position}) - Usage: {player_usage}% | Defensive Efficiency: {team2_def_eff_value:.2f}")
            else:
                team1_analysis.append(f"{player_name} (No Position Found) - Usage: {player_usage}% | Defensive Efficiency: N/A")

        # Analyzing team 2 players
        for player_name, player_usage in [(team2_data[0], team2_data[1]), (team2_data[2], team2_data[3])]:
            player_position = get_player_position(player_name, team2_id)
            if player_position:
                # Get defensive efficiency of team1 against this player's position
                team1_def_eff_value = get_def_eff(player_position, team1_def_eff)
                team2_analysis.append(f"{player_name} ({player_position}) - Usage: {player_usage}% | Defensive Efficiency: {team1_def_eff_value:.2f}")
            else:
                team2_analysis.append(f"{player_name} (No Position Found) - Usage: {player_usage}% | Defensive Efficiency: N/A")

        # Close the database connection
        conn.close()

        # Display results in the message box
        messagebox.showinfo("Analysis Result",
            f"Team 1 Analysis:\n" + "\n".join(team1_analysis) + "\n\n"
            f"Team 2 Analysis:\n" + "\n".join(team2_analysis)
        )

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data from database: {e}")


# Create the main window (root)
root = tk.Tk()
root.title("ARRBO - Sports Betting Companion")

# Set full-screen mode
root.attributes('-fullscreen', True)

# Set background color to dark
root.config(bg="#2E2E2E")  # Dark gray background

# Styling for buttons and comboboxes
style = ttk.Style()
style.configure("TButton", font=("Arial", 14), padding=10, relief="flat", background="#008080", foreground="black", width=20)
style.map("TButton", background=[('active', '#006666')], relief=[('pressed', 'groove')])

style.configure("TCombobox", font=("Arial", 12), padding=5, width=18, background="#333333", foreground="black")

# Label for the title
title_label = tk.Label(root, text="ARRBO", font=("Arial", 32, "bold"), fg="white", bg="#2E2E2E")
title_label.pack(pady=20)

# Label for the subtitle
subtitle_label = tk.Label(root, text="Sports Betting Companion", font=("Arial", 18), fg="white", bg="#2E2E2E")
subtitle_label.pack(pady=10)

# Buttons with rounded corners and improved UI
btn_deff_eff = ttk.Button(root, text="Populate Deff_Eff Table", command=update_deff_eff, style="TButton")
btn_deff_eff.pack(pady=15)

btn_positions = ttk.Button(root, text="Populate Positions Table", command=update_positions, style="TButton")
btn_positions.pack(pady=15)

btn_usage = ttk.Button(root, text="Populate Usage Table", command=update_usage, style="TButton")
btn_usage.pack(pady=15)

# Dropdown for Team 1
team1_label = tk.Label(root, text="Select Team 1:", font=("Arial", 18, "bold"), fg="white", bg="#2E2E2E")
team1_label.pack(pady=10)

team1_combo = ttk.Combobox(root, values=["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"], style="TCombobox")
team1_combo.pack(pady=10)

# "VS" label between the dropdowns
vs_label = tk.Label(root, text="VS", font=("Arial", 24, "bold"), fg="white", bg="#2E2E2E")
vs_label.pack(pady=10)

# Dropdown for Team 2
team2_label = tk.Label(root, text="Select Team 2:", font=("Arial", 18, "bold"), fg="white", bg="#2E2E2E")
team2_label.pack(pady=10)

team2_combo = ttk.Combobox(root, values=["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "LA Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"], style="TCombobox")
team2_combo.pack(pady=10)

# Button to analyze the selected teams
btn_analyze = ttk.Button(root, text="Analyze Teams", command=lambda: get_team_data(team1_combo.get(), team2_combo.get()), style="TButton")
btn_analyze.pack(pady=30)

# Data display section (placeholder)
result_label = tk.Label(root, text="Analysis Results will appear here", font=("Arial", 16), fg="white", bg="#2E2E2E")
result_label.pack(pady=20)

# Exit button
btn_exit = ttk.Button(root, text="Exit", command=root.quit, style="TButton")
btn_exit.pack(pady=20)

# Run the GUI
root.mainloop()