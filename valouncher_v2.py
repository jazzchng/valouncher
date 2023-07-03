import os
import sys
import subprocess
import getpass
import time
import codecs
import webbrowser
import regex

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import configparser
import pyautogui
import requests

from pywinauto import Desktop

# Set the root directory path
root_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
loop = 0

# Load accounts.cfg
config_file_path = os.path.join(root_directory, 'accounts.cfg')
config = configparser.ConfigParser()

# Create the config file with UTF-8 encoding
def create_config_file():
    config = configparser.ConfigParser()
    config['settings'] = {
        'riot_path': r"C:\Riot Games\Riot Client\RiotClientServices.exe",
        'launch_parameters': '--launch-product=valorant --launch-patchline=live'
    }
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        config.write(config_file)

def update_config_file():
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        config.write(config_file)

# Open the config file with UTF-8 encoding
def read_config_file():
    with codecs.open(config_file_path, 'r', encoding='utf-8') as config_file:
        config.read_file(config_file)

if not os.path.isfile(config_file_path):
    create_config_file()

read_config_file()

def list_accounts():
    if not os.path.isfile(config_file_path):
        return 0, None, None  # Return default values if no accounts found
    else:
        read_config_file()

riot_path = config['settings']['riot_path']
launch_parameters = config['settings']['launch_parameters']

joined_path = f'{riot_path} {launch_parameters}'

# Get the username
winuser = getpass.getuser()

# Create the full file path with the username
file_path = os.path.join(rf'C:\Users\{winuser}', 'AppData\Local\Riot Games\Riot Client\Data\RiotGamesPrivateSettings.yaml')

# Check if file exists and delete it
if os.path.exists(file_path):
    os.remove(file_path)

# Check if process is running and terminate it
process_name = 'VALORANT-WIN64-SHIPPING.exe'
output = subprocess.run(['tasklist', '/FI', f'imagename eq {process_name}'], capture_output=True, text=True)
if ':' not in output.stdout:
    subprocess.run(['taskkill', '/F', '/IM', process_name])

# Check if process is running and terminate it
process_name = 'RiotClientServices.exe'
output = subprocess.run(['tasklist', '/FI', f'imagename eq {process_name}'], capture_output=True, text=True)
if ':' not in output.stdout:
    subprocess.run(['taskkill', '/F', '/IM', process_name])

# Create the main window
window = tk.Tk()
window.title("Valouncher")

# Get the screen resolution
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the position of the window to center it
window_width = 615
window_height = 861
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.resizable(width=False, height=False)

# Set the background color to a dark theme color
window.configure(bg='#1f1f1f')

# Create a frame for the disclaimer
disclaimer_frame = ttk.Frame(window)
disclaimer_frame.pack()

# Create a custom style for the disclaimer label
style = ttk.Style()
style.configure("Custom.TLabel", background="#1f1f1f", foreground='white', anchor='w', justify='left', font=('Helvetica', 10))

# Add the disclaimer label
disclaimer_text = '''
Welcome to Valouncher!
Version: 2.0
By Jazz Chng

==========
DISCLAIMER
==========
Educational Purpose Only!

This is a simple Valorant Launcher that stores your username and password in an accounts.cfg file.
Passwords are stored on your local drive and NOT ENCRYPTED! USE AT YOUR OWN RISK!!

This application is provided "as is," and I, Jazz Chng, am not affiliated with Riot Games or Valorant in any way.
By using Valouncher, you acknowledge and accept all risks associated with storing your account information locally.
I will not be held liable for any lost accounts or unauthorized access.
Always prioritize your account security and enable two-factor authentication (2FA) for your Valorant account.

For transparency, the source code is open and available on GitHub:
https://github.com/jazzchng/valouncher/

'''
disclaimer_label = ttk.Label(disclaimer_frame, text=disclaimer_text, style="Custom.TLabel", wraplength=595, justify='left')
disclaimer_label.pack(fill='both', padx=0)

# Create a frame for the Treeview
treeview_frame = ttk.Frame(window)
treeview_frame.pack(fill='both', expand=True, padx=10)

# Configure the button frame
window.style = ttk.Style()
window.style.configure("Button.TFrame", background="#1f1f1f")

# Create a frame for the buttons
button_frame = ttk.Frame(window, padding=(0, 10), style="Button.TFrame")
button_frame.pack()

# Create a frame for the terminal
terminal_frame = ttk.Frame(window, padding=(1, 1))
terminal_frame.pack(padx=10)

# Create the terminal (Text widget)
terminal = tk.Text(terminal_frame, bg='black', fg='white', height=10)
terminal.grid(row=0, column=0, sticky='nsew')

# Create a vertical scrollbar
t_scrollbar = ttk.Scrollbar(terminal_frame, orient="vertical", command=terminal.yview, style='Custom.Vertical.TScrollbar')
t_scrollbar.grid(row=0, column=1, sticky='ns')

# Configure the Text widget to use the scrollbar
terminal.configure(yscrollcommand=t_scrollbar.set)

# Configure the grid weights for terminal_frame to make it expandable
terminal_frame.grid_rowconfigure(0, weight=1)
terminal_frame.grid_columnconfigure(0, weight=1)

# Attach the scrollbar to the right of the terminal widget
terminal.grid_rowconfigure(0, weight=1)
t_scrollbar.grid_rowconfigure(0, weight=1)

# Create a frame for the credits
credits_frame = ttk.Frame(window, padding=(0, 0))
credits_frame.pack()

# Add the credits label
credits_text = "Original version by @jazzchng - Open Source - v2.0"
credits_label = ttk.Label(credits_frame, text=credits_text, style="Custom.TLabel", wraplength=550, justify='center')
credits_label.pack(padx=0, pady=0)

# Create a custom style for the Treeview and the Scrollbar
style.configure('Custom.Treeview', highlightthickness=0, bd=0, font=('Helvetica', 10))
style.configure('Custom.Vertical.TScrollbar', width=10)

# Create the Treeview widget
treeview = ttk.Treeview(treeview_frame, style='Custom.Treeview')

# Define column headings
treeview['columns'] = ('ID', 'Username', 'IGN', 'Rank', 'RR')

# Set column widths
treeview.column('#0',width=0, stretch=tk.NO)
treeview.column('ID', width=50, anchor='center')
treeview.column('Username', width=120, anchor='center')
treeview.column('IGN', width=150, anchor='center')
treeview.column('Rank', width=100, anchor='e')
treeview.column('RR', width=50, anchor='center')

# Create the header row
treeview.heading('ID', text='ID')
treeview.heading('Username', text='Username')
treeview.heading('IGN', text='IGN')
treeview.heading('Rank', text='Rank')
treeview.heading('RR', text='RR')

# Create a vertical scrollbar
tv_scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=treeview.yview, style='Custom.Vertical.TScrollbar')

# Configure the Treeview to use the scrollbar
treeview.configure(yscrollcommand=tv_scrollbar.set)

# Attach the scrollbar to the treeview
tv_scrollbar.pack(side='right', fill='y')

# Add the Treeview to the treeview frame
treeview.pack(side='left', fill='both', expand=True)

def populate_treeview(treeview):
    read_config_file()
    
    # Skip populating if only 'settings' section exists
    if len(config.sections()) == 1 and 'settings' in config.sections():
        return
    
    # Clear the existing data in the treeview
    treeview.delete(*treeview.get_children())

    # Iterate over the sections and populate the rows
    row_id = 1
    for section_name in config.sections():
        if section_name == 'settings':
            continue
        
        account_data = config[section_name]
        username = account_data['username']
        ign = f"{account_data['player_name']}#{account_data['player_tag']}"
        rank = account_data['currenttierpatched']
        rr = account_data['ranking_in_tier']

        if ign == '#':
            ign = ''

        # Insert the row into the Treeview
        treeview.insert('', 'end', values=(row_id, username, ign, rank, rr), tags=('Custom.Treeview.Row',))
        row_id += 1

    # Configure the style for Treeview rows
    treeview.tag_configure('Custom.Treeview.Row', background='#1f1f1f', foreground='white')

def wait_for_window(window_title, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if pyautogui.getWindowsWithTitle(window_title):
            return True
        time.sleep(1)
    return False

def show_centered_message(title, message):
    # Calculate the coordinates to center the message box
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    message_box_width = 150  # Set the width of the message box
    message_box_height = 100  # Set the height of the message box
    x = window.winfo_x() + (window_width - message_box_width) // 2
    y = window.winfo_y() + (window_height - message_box_height) // 2

    # Create a hidden top-level window to act as the parent for the message box
    top = tk.Toplevel(window)
    top.withdraw()

    # Position the top-level window in the center of the main window
    top.geometry(f"{message_box_width}x{message_box_height}+{x}+{y}")

    # Show the message box
    messagebox.showinfo(title, message, parent=top)

# Function to print progress in the terminal
def print_progress(message):
    terminal.insert('end', message + '\n')
    terminal.see('end')  # Scroll to the end of the terminal
    terminal.update_idletasks()  # Update the GUI immediately, this prevents terminal freezing and ensures print while functions are running!

def launch_account():
    selected_item = treeview.selection()
    if selected_item == ():
        messagebox.showinfo("No Account Selected", "Select an Account to Launch!")
        return

    item_values = treeview.item(selected_item)['values']

    # Perform launch account operation using item_values
    account_choice = item_values[0]
    section_name = f'account{account_choice}'
    username = config[section_name]['username']
    password = config[section_name]['password']
    print_progress(f"Launching [account{account_choice}] {username}")

    # Launch RiotClientServices.exe
    print_progress(f"Launching Riot: {riot_path}")
    print_progress(f"Parameters: {launch_parameters}")
    subprocess.Popen(joined_path)

    # Detecting Riot Client Main window
    if wait_for_window("Riot Client Main"):
        # The window is visible and launched, continue with your code here
        while True:
            try:
                main_window = Desktop(backend="uia").window(title="Riot Client Main")
                if main_window.exists():
                    # Extract and input the username and password fields
                    print_progress(f"Credentials for: {username}")
                    username_field = main_window.child_window(title="USERNAME", auto_id="username", control_type="Edit")
                    print_progress(f"Inserting username...")
                    username_field.set_text(username)
                    password_field = main_window.child_window(title="PASSWORD", auto_id="password", control_type="Edit")
                    print_progress(f"Inserting password...")
                    password_field.set_text(password)

                    # Click the "Sign in" button
                    sign_in_button = main_window.child_window(title="Sign in", control_type="Button")
                    sign_in_button.click()

                    sys.exit()
            except Exception as e:
                print_progress(f"Exception: {e}")
                pass
    else:
        # Timeout occurred, handle the situation accordingly
        print_progress(f"Timeout: [Riot Client Main] window not found.")
    print_progress(f"Launching account:", item_values[0])

def count_acounts():
    read_config_file()
    account_count = 0
    for section in config.sections():
        if section.lower().startswith('account'):
            account_count += 1
    return account_count

def add_account():
    account_count = count_acounts()
    # Create a new window for adding an account
    account_window = tk.Toplevel(window)

    # Disable window resizing
    account_window.resizable(False, False)

    account_window.title("Add")
    
    # Calculate the coordinates to center the account_window
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    account_window_width = 220  # Set the width of the account_window
    account_window_height = 240  # Set the height of the account_window
    x = window.winfo_x() + (window_width - account_window_width) // 2
    y = window.winfo_y() + (window_height - account_window_height) // 2

    # Position the account_window in the center of the window
    account_window.geometry(f"{account_window_width}x{account_window_height}+{x}+{y}")

    section_name = f'account{account_count + 1}'

    # Function to handle the Add Account button click
    def handle_add_account():
        username = username_entry.get()
        password = password_entry.get()
        player_name_tag = player_name_tag_entry.get()
        account_description = account_description_entry.get()
        
        status = insert_cfg(section_name, username, password, player_name_tag, account_description)
        if status == True:
            messagebox.showinfo(f"Success", f"Account: {username} Saved!")
        else:
            messagebox.showinfo(f"Failed", f"Please Try Again!")
        populate_treeview(treeview)
        # Close the account window
        account_window.destroy()

    # Username field
    username_label = tk.Label(account_window, text="Username:")
    username_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
    username_entry = tk.Entry(account_window)
    username_entry.grid(row=1, column=0, padx=10, pady=0, sticky="we")

    # Password field
    password_label = tk.Label(account_window, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=0, sticky="w")
    password_entry = tk.Entry(account_window, show="*")
    password_entry.grid(row=3, column=0, padx=10, pady=0, sticky="we")

    # Player Name Tag field
    player_name_tag_label = tk.Label(account_window, text="In Game Name#Tag (Optional):")
    player_name_tag_label.grid(row=4, column=0, padx=10, pady=0, sticky="w")
    player_name_tag_entry = tk.Entry(account_window)
    player_name_tag_entry.grid(row=5, column=0, padx=10, pady=0, sticky="we")

    # Account Description field
    account_description_label = tk.Label(account_window, text="Account Description (Optional):")
    account_description_label.grid(row=6, column=0, padx=10, pady=0, sticky="w")
    account_description_entry = tk.Entry(account_window)
    account_description_entry.grid(row=7, column=0, padx=10, pady=0, sticky="we")

    # Add Account button
    add_button = tk.Button(account_window, text="Add Account", command=handle_add_account)
    add_button.grid(row=8, column=0, padx=10, pady=5, sticky="we")

    # Cancel button
    cancel_button = tk.Button(account_window, text="Cancel", command=account_window.destroy)
    cancel_button.grid(row=9, column=0, padx=10, pady=5, sticky="we")

    # Configure grid row and column weights
    for i in range(10):
        account_window.grid_rowconfigure(i, weight=1)
    account_window.grid_columnconfigure(0, weight=1)

def edit_account():
    selected_item = treeview.selection()
    if selected_item == ():
        messagebox.showinfo("No Account Selected", "Select an Account to Edit!")
        return
    
    item_values = treeview.item(selected_item)['values']
    account_choice = item_values[0]

    # Create a new window for editing an account
    edit_account_window = tk.Toplevel(window)
    
    # Disable window resizing
    edit_account_window.resizable(False, False)

    edit_account_window.title("Edit")
    
    # Calculate the coordinates to center the account_window
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    account_window_width = 220  # Set the width of the account_window
    account_window_height = 240  # Set the height of the account_window
    x = window.winfo_x() + (window_width - account_window_width) // 2
    y = window.winfo_y() + (window_height - account_window_height) // 2

    # Position the account_window in the center of the window
    edit_account_window.geometry(f"{account_window_width}x{account_window_height}+{x}+{y}")
    section_name = f"account{account_choice}"

    # Retrieve values from configuration file
    username_default = config[section_name]['username']
    password_default = config[section_name]['password']
    try:
        player_name = config[section_name]['player_name']
        player_tag = config[section_name]['player_tag']
        player_name_default = f"{player_name}#{player_tag}" if player_name and player_tag else ''
    except KeyError:
        player_name_default = ''

    try:
        account_description_default = config[section_name]['account_description']
    except KeyError:
        account_description_default = ''
        
    # Function to handle the Add Account button click
    def handle_add_account():
        username = username_entry.get()
        password = password_entry.get()
        player_name_tag = player_name_tag_entry.get()
        account_description = account_description_entry.get()
        
        status = insert_cfg(section_name, username, password, player_name_tag, account_description)
        if status == True:
            messagebox.showinfo(f"Success", f"Account: {username} Saved!")
        else:
            messagebox.showinfo(f"Failed", f"Please Try Again!")
        populate_treeview(treeview)
        # Close the account window
        edit_account_window.destroy()

    # Username field
    username_label = tk.Label(edit_account_window, text="Username:")
    username_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
    username_entry = tk.Entry(edit_account_window)
    username_entry.insert(tk.END, username_default)  # Set default value
    username_entry.grid(row=1, column=0, padx=10, pady=0, sticky="we")

    # Password field
    password_label = tk.Label(edit_account_window, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=0, sticky="w")
    password_entry = tk.Entry(edit_account_window, show="*")
    password_entry.insert(tk.END, password_default)  # Set default value
    password_entry.grid(row=3, column=0, padx=10, pady=0, sticky="we")

    # Player Name Tag field
    player_name_tag_label = tk.Label(edit_account_window, text="In Game Name#Tag (Optional):")
    player_name_tag_label.grid(row=4, column=0, padx=10, pady=0, sticky="w")
    player_name_tag_entry = tk.Entry(edit_account_window)
    player_name_tag_entry.insert(tk.END, player_name_default)  # Set default value
    player_name_tag_entry.grid(row=5, column=0, padx=10, pady=0, sticky="we")

    # Account Description field
    account_description_label = tk.Label(edit_account_window, text="Account Description (Optional):")
    account_description_label.grid(row=6, column=0, padx=10, pady=0, sticky="w")
    account_description_entry = tk.Entry(edit_account_window)

    account_description_entry.insert(tk.END, account_description_default)  # Set default value
    account_description_entry.grid(row=7, column=0, padx=10, pady=0, sticky="we")

    # Add Account button
    add_button = tk.Button(edit_account_window, text="Add Account", command=handle_add_account)
    add_button.grid(row=8, column=0, padx=10, pady=5, sticky="we")

    # Cancel button
    cancel_button = tk.Button(edit_account_window, text="Cancel", command=edit_account_window.destroy)
    cancel_button.grid(row=9, column=0, padx=10, pady=5, sticky="we")

    # Configure grid row and column weights
    for i in range(10):
        edit_account_window.grid_rowconfigure(i, weight=1)
    edit_account_window.grid_columnconfigure(0, weight=1)

def insert_cfg(section_name, username, password, player_name_tag, account_description):
    while True:
        if not player_name_tag:
            player_name = ''
            player_tag = ''
            break
        split_player_name_tag = regex.match(r"^([\p{L}\p{N}\s]{3,16})#([\w]{1,5})$", player_name_tag)
        if split_player_name_tag:
            player_name = split_player_name_tag.group(1)
            player_tag = split_player_name_tag.group(2)
            break
        else:
            messagebox.showinfo(f"Error", f"In Game Name#Tag Error!")
            status = False
            return status

    config[section_name] = {
        'username': username,
        'password': password,
        'player_name': player_name,
        'player_tag': player_tag,
        'currenttier': '',
        'currenttierpatched': '',
        'ranking_in_tier': '',
        'mmr_change_to_last_game': '',
        'elo': ''
    }
    if account_description:
        config[section_name]['account_description'] = account_description
    
    update_config_file()
    status = True
    return status

def view_stored_accounts():
    selected_item = treeview.selection()
    if selected_item == ():
        messagebox.showinfo("No Account Selected", "Select an Account to View!")
        return

    # Get the selected item details from the Treeview
    item_values = treeview.item(selected_item)['values']
    account_choice = item_values[0]
    section_name = f'account{account_choice}'
    account_data = config[section_name]
    print_progress(f"Viewing Account: {section_name[7:]}. {account_data['username']}")

    # Create a new window for displaying account details
    account_window = tk.Toplevel()
    account_window.title(f"{section_name[7:]}. {account_data['username']}")
    account_window.geometry("400x200")

    # Disable window resizing
    account_window.resizable(False, False)
    
    # Calculate the coordinates to center the account_window
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    account_window_width = 400  # Set the width of the account_window
    account_window_height = 220  # Set the height of the account_window
    x = window.winfo_x() + (window_width - account_window_width) // 2
    y = window.winfo_y() + (window_height - account_window_height) // 2

    # Position the account_window in the center of the window
    account_window.geometry(f"{account_window_width}x{account_window_height}+{x}+{y}")


    # Create a text widget to display the account details
    account_text = tk.Text(account_window, bg='black', fg='white', height=10)
    account_text.pack(fill='both', expand=True, padx=10, pady=10)

    if selected_item:
        # Append the account details to the text widget
        account_text.insert('end', f"          [account{section_name[7:]}] {account_data['username']}\n")
        account_text.insert('end', 46*"=" + "\n")
        account_text.insert('end', f"                IGN: {account_data['player_name']}#{account_data['player_tag']}\n")
        account_text.insert('end', f"       Current Rank: {account_data['currenttierpatched']}\n")
        account_text.insert('end', f"                 RR: {account_data['ranking_in_tier']}\n")
        account_text.insert('end', f"  RR From Last Game: {account_data['mmr_change_to_last_game']}\n")
        account_text.insert('end', f"                Elo: {account_data['elo']}\n")
        account_text.insert('end', f"       Current Tier: {account_data['currenttier']}\n")
        account_text.insert('end', f"Account Description: {account_data['account_description']}\n")
    else:
        # If no item is selected, display a message
        account_text.insert('end', "No account selected.")

    # Disable editing in the text widget
    account_text.configure(state='disabled')

    # Run the account window main loop
    account_window.mainloop()

def fetch_account_details():
    api_base_url = 'https://api.henrikdev.xyz/valorant/v1/mmr/ap/'

    # Get the total number of accounts
    total_accounts = count_acounts()

    # List all accounts
    for i, section_name in enumerate(config.sections(), start=0):
        if section_name.startswith('account'):
            account_data = config[section_name]
            username = account_data['username']
            player_name = account_data['player_name']
            player_tag = account_data['player_tag']

            if not player_name or not player_tag:
                print_progress(f"No IGN stored for {i}. Skipping account: {username}")
                continue

            # Encode the player name and tag for the API request
            encoded_player_name = requests.utils.quote(player_name)
            encoded_player_tag = requests.utils.quote(player_tag)
            api_url = f'{api_base_url}{encoded_player_name}/{encoded_player_tag}'

            try:
                response = requests.get(api_url)
                response.raise_for_status()  # Check for any errors in the response

                # Parse the API response and retrieve the player information
                player_info = response.json()['data']

                # Update the configuration with the player information
                config[section_name]['currenttier'] = str(player_info.get('currenttier', ''))
                config[section_name]['currenttierpatched'] = player_info.get('currenttierpatched', '')
                config[section_name]['ranking_in_tier'] = str(player_info.get('ranking_in_tier', ''))
                config[section_name]['mmr_change_to_last_game'] = str(player_info.get('mmr_change_to_last_game', ''))
                config[section_name]['elo'] = str(player_info.get('elo', ''))

                update_config_file()
                
                print_progress(f"Retrieved   for   {i}. {player_name}#{player_tag} (Account: {username})")
                
            except requests.exceptions.RequestException as e:
                print_progress(f"Failed to retrieve player information for {player_name}#{player_tag} (Account: {username}): {str(e)}")
    populate_treeview(treeview)

def open_github(event):
    webbrowser.open("https://github.com/jazzchng/valouncher/")

def exit_application():
    window.destroy()

# Populate the treeview
populate_treeview(treeview)
print_progress(f"Activity Log")
print_progress(f"Riot Directory: {riot_path}")
print_progress(f"Parameters: {launch_parameters}")

# Create the buttons
launch_button = ttk.Button(button_frame, text="Launch", command=launch_account)
add_button = ttk.Button(button_frame, text="Add", command=add_account)
edit_button = ttk.Button(button_frame, text="Edit", command=edit_account)
view_button = ttk.Button(button_frame, text="View Details", command=view_stored_accounts)
fetch_button = ttk.Button(button_frame, text="Fetch Details", command=fetch_account_details)
github_button = ttk.Button(button_frame, text="GitHub", command=open_github)
exit_button = ttk.Button(button_frame, text="Exit", command=exit_application)

# Bind the GitHub button to the open_github function
github_button.bind("<Button-1>", open_github)

# Add the buttons to the frame
launch_button.grid(row=0, column=0, padx=5)
add_button.grid(row=0, column=1, padx=5)
edit_button.grid(row=0, column=2, padx=5)
view_button.grid(row=0, column=3, padx=5)
fetch_button.grid(row=0, column=4, padx=5)
github_button.grid(row=0, column=5, padx=5)
exit_button.grid(row=0, column=6, padx=5)

# Set the column weights for center alignment
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(2, weight=1)

# Start the main event loop
window.mainloop()