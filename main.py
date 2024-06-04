import sys
import json
import argparse
from datetime import datetime
from colorama import init, Fore, Style
from csv_generator import generate_csv
from upload import upload_to_staging
from loader import create_loader_job
from auth import save_encrypted_credentials, authenticate

# Initialize colorama
init(autoreset=True)

# Load configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

predefined_objects = config["predefined_objects"]
lifecycle_states = config["lifecycle_states"]
api_info = config["api_info"]

def prompt_user():
    print(Fore.CYAN + "Select an object type to update:")
    for key, value in predefined_objects.items():
        print(Fore.YELLOW + f"{key}: {value}")
    object_choice = input(Fore.GREEN + "Enter the number corresponding to the object type: ")
    object_type = predefined_objects.get(object_choice)

    if not object_type:
        print(Fore.RED + "Invalid object type selected.")
        sys.exit(1)

    print(Fore.CYAN + "Select a lifecycle state:")
    for key, value in lifecycle_states[object_type].items():
        print(Fore.YELLOW + f"{key}: {value}")
    state_choice = input(Fore.GREEN + "Enter the number corresponding to the lifecycle state: ")
    lifecycle_state = lifecycle_states[object_type].get(state_choice)

    if not lifecycle_state:
        print(Fore.RED + "Invalid lifecycle state selected.")
        sys.exit(1)

    while True:
        object_ids = input(Fore.GREEN + "Enter the IDs for the relevant objects, separated by commas: ")
        object_ids_list = [obj_id.strip() for obj_id in object_ids.split(",")]

        # Check for empty IDs and duplicates
        if "" in object_ids_list:
            print(Fore.RED + "Error: One or more IDs are empty. Please enter valid IDs.")
            continue

        if len(object_ids_list) != len(set(object_ids_list)):
            print(Fore.RED + "Error: Duplicate IDs found. Please enter unique IDs.")
            continue

        break

    # Generate the filename based on object, lifecycle state, and current date and time
    current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_path = f"{object_type}_{lifecycle_state}_{current_timestamp}.csv"

    return csv_file_path, object_ids_list, lifecycle_state, object_type

if __name__ == "__main__":
    while True:
        print(Fore.CYAN + "Choose an action:")
        print(Fore.YELLOW + "1: Generate CSV")
        print(Fore.YELLOW + "2: Generate and Upload CSV")
        print(Fore.YELLOW + "3: Save New Credentials")
        print(Fore.YELLOW + "4: Test Authentication")
        print(Fore.YELLOW + "5: Exit")
        action_choice = input(Fore.GREEN + "Enter the number corresponding to the action: ")

        if action_choice == "1":
            csv_file_path, object_ids_list, lifecycle_state, _ = prompt_user()
            generate_csv(csv_file_path, object_ids_list, lifecycle_state)
            print(Fore.CYAN + f"CSV file generated: {csv_file_path}")

        elif action_choice == "2":
            csv_file_path, object_ids_list, lifecycle_state, object_type = prompt_user()
            generate_csv(csv_file_path, object_ids_list, lifecycle_state)
            print(Fore.CYAN + f"CSV file generated: {csv_file_path}")
            try:
                uploaded_file_name = upload_to_staging(csv_file_path)
                create_loader_job(uploaded_file_name, object_type)
            except Exception as e:
                print(Fore.RED + str(e))

        elif action_choice == "3":
            save_encrypted_credentials()

        elif action_choice == "4":
            try:
                session_id = authenticate()
                print(Fore.CYAN + f"Authenticated successfully. Session ID: {session_id}")
            except Exception as e:
                print(Fore.RED + f"Authentication failed: {str(e)}")

        elif action_choice == "5":
            print(Fore.CYAN + "Exiting...")
            sys.exit(0)

        else:
            print(Fore.RED + "Invalid action selected.")