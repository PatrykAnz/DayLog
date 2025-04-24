from pathlib import Path
import json
import os
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator(): 
    print("-"*50)

def create_user_data():
    data_folder = Path("user_data")
    data_file = data_folder / "user_data.json"

    if not data_folder.exists():
        data_folder.mkdir()
        print("Created 'user_data' folder.")
    
    if not data_file.exists():
        with open(data_file, "w") as f:
            json.dump({},f)
        print("Created 'user_data.json' file.")

def get_user_choice():
    choices={
       1:"Weather",
       2:"Geolocation"
    }
    total_amount = len(choices)
    while True:
        print(f"Choose from 1-{total_amount}")
        for key, value in choices.items():
            print(f"{key}. {value}")
        
        try:
            user_choice = int(input(""))
            if user_choice in choices:
                print(f"{choices[user_choice]}:")
                input("Press enter to return")
                cls()
            else:
                print_separator()
                print("Invalid choice. Enter a number from the list.")
                print_separator()
        except ValueError as e:
            print_separator()
            print("An error has ocurred. Make sure you entered a number")
            print(f"\nError info: \n{e}") 
            print_separator()
if __name__ == "__main__":
    data_folder_path = Path("user_data")
    if not data_folder_path.exists():
        create_user_data() 
    get_user_choice()