import os
import configparser
import subprocess
import re
import time
import win32gui
import win32con
import pyautogui
import pywinauto
from pywinauto import Desktop
import sys

# Set the root directory path
root_directory = os.path.dirname(os.path.abspath(__file__))

print("Welcome to Valouncher!")
print("Created and mainted by ")

# Functions
def create_config_file():
    config = configparser.ConfigParser()
    config.add_section('accounts')

    config_file_path = os.path.join(root_directory, 'accounts.cfg')
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

def store_account():
    config_file_path = os.path.join(root_directory, 'accounts.cfg')

    if not os.path.isfile(config_file_path):
        create_config_file()

    config = configparser.ConfigParser()
    config.read(config_file_path)
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    section_name = f'account{len(config.sections())}'
    config[section_name] = {'username': username, 'password': password}
    
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)
    
    print("Account stored successfully!")

def launch_account():
    config_file_path = os.path.join(root_directory, 'accounts.cfg')

    if not os.path.isfile(config_file_path):
        print("No accounts found. Please add an account.")
        return

    config = configparser.ConfigParser()
    config.read(config_file_path)

    account_count = len(config.sections())
    if account_count == 0:
        print("No accounts found. Please add an account.")
        return

    print("Stored accounts:")
    for i in range(1, account_count):
        section_name = f'account{i}'
        username = config[section_name]['username']
        password = config[section_name]['password']

        print(f"{i}. {username} - {password}")

    account_choice = input("Enter the account number to launch (or '0' to go back): ")
    try:
        account_choice = int(account_choice)
        if account_choice == 0:
            return
        elif 1 <= account_choice <= account_count:
            section_name = f'account{account_choice}'
            username = config[section_name]['username']
            password = config[section_name]['password']
            print(f"Launching Account {account_choice}: {username} - {password}")

            # Launch RiotClientServices.exe
            subprocess.Popen(r'C:\Riot Games\Riot Client\RiotClientServices.exe')

            # Detecting Riot Client Main window
            if wait_for_window("Riot Client Main"):
                # The window is visible and launched, continue with your code here
                while True:
                    try:
                        main_window = Desktop(backend="uia").window(title="Riot Client Main")
                        if main_window.exists():
                            # Extract and input the username and password fields
                            print(f'Credentials for: {username}')
                            username_field = main_window.child_window(title="USERNAME", auto_id="username", control_type="Edit")
                            username_field.set_text(username)
                            password_field = main_window.child_window(title="PASSWORD", auto_id="password", control_type="Edit")
                            password_field.set_text(password)

                            # Click the "Sign in" button
                            sign_in_button = main_window.child_window(title="Sign in", control_type="Button")
                            sign_in_button.click()

                            sys.exit()
                    except Exception as e:
                        print('Exception as e')
                        pass

            else:
                # Timeout occurred, handle the situation accordingly
                print("Timeout: [Riot Client Main] window not found.")
                return
        else:
            print("Invalid account number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def view_accounts():
    config_file_path = os.path.join(root_directory, 'accounts.cfg')

    if not os.path.isfile(config_file_path):
        print("No accounts found.")
        return

    config = configparser.ConfigParser()
    config.read(config_file_path)

    account_count = len(config.sections())
    if account_count == 0:
        print("No accounts found.")
        return

    print("Currently stored accounts:")
    for i in range(1, account_count):
        section_name = f'account{i}'
        username = config[section_name]['username']
        password = config[section_name]['password']

        print(f"Account {i}: {username} - {password}")

def wait_for_window(window_title, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if pyautogui.getWindowsWithTitle(window_title):
            return True
        time.sleep(1)
    return False

# Main loop
while True:
    print("1. Launch Account")
    print("2. Add Account")
    print("3. View Stored Accounts")
    print("0. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        launch_account()
    elif choice == '2':
        store_account()
    elif choice == '3':
        view_accounts()
    elif choice == '0':
        break
    else:
        print("Invalid choice. Please try again.")