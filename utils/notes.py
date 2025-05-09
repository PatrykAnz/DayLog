import json
import datetime
from pathlib import Path
from utils.print_helpers import print_separator

def get_notes():
    choices = {0: "Exit", 1: "Create", 2: "Read", 3: "Update", 4: "Delete"}
    total_amount = len(choices)
    while True:
        print(f"Choose from 0-{total_amount-1}")
        for key, value in choices.items():
            print(f"{key}. {value}")
        try:
            user_choice = int(input(""))
            if user_choice in choices:
                if user_choice == 0:
                    return
                print(f"{choices[user_choice]}:")
                if user_choice == 1:
                    create_notes()
                elif user_choice == 2:
                    read_notes()
                elif user_choice == 3:
                    update_notes()
                elif user_choice == 4:
                    delete_notes()
            else:
                print_separator()
                print("Invalid choice. Enter a number from the list.")
                print_separator()
        except ValueError as e:
            print_separator()
            print("An error has occurred. Make sure you entered a number")
            print(f"\nError info: \n{e}")
            print_separator()


def create_notes():
    print("create notes")
    data_folder = Path("user_data")
    notes_file = data_folder / "user_notes.json"
    with open(notes_file, "r") as f:
        notes_data = json.load(f)
    new_note = input("Note name: ")
    new_note_tag = input("Tag (You can skip it): ")
    new_note_create_date = datetime.datetime.now()

    new_note = {
        "name": new_note,
        "tag": new_note_tag,
        "created_at": new_note_create_date.strftime("%Y-%m-%d %H:%M"),
        "last_edited": new_note_create_date.strftime("%Y-%m-%d %H:%M"),
    }
    notes_data.append(new_note)

    with open(notes_file, "w") as f:
        json.dump(notes_data, f, indent=4)


def read_notes():
    data_folder = Path("user_data")
    notes_file = data_folder / "user_notes.json"
    with open(notes_file, "r") as f:
        notes_data = json.load(f)

    if not notes_data:
        print("No notes found")
        return

    print("\nNotes:")
    print("-" * 50)
    for i, note in enumerate(notes_data, 1):
        print(f"\nNote #{i}")
        print(f"Name: {note['name']}")
        print(f"Tag: {note['tag']}")
        print(f"Created: {note['created_at']}")
        print(f"Last Edited: {note['last_edited']}")
        print("-" * 50)
    input(f"Press Enter to return")


def update_notes():
    data_folder = Path("user_data")
    notes_file = data_folder / "user_notes.json"
    with open(notes_file, "r") as f:
        notes_data = json.load(f)

    if not notes_data:
        print("No notes to update!")
        return

    print("\nWhich note would you like to update?")
    print("-" * 50)
    for i, note in enumerate(notes_data, 1):
        print(f"\nNote #{i}")
        print(f"Name: {note['name']}")
        print(f"Tag: {note['tag']}")
        print("-" * 50)

    try:
        note_to_update = int(input("Enter note number to update (0 to cancel): ")) - 1
        if note_to_update == -1:
            return
        if 0 <= note_to_update < len(notes_data):
            print("\nEnter new information (press Enter to keep current value):")
            new_name = (
                input(f"New name [{notes_data[note_to_update]['name']}]: ")
                or notes_data[note_to_update]["name"]
            )
            new_tag = (
                input(f"New tag [{notes_data[note_to_update]['tag']}]: ")
                or notes_data[note_to_update]["tag"]
            )

            notes_data[note_to_update].update(
                {
                    "name": new_name,
                    "tag": new_tag,
                    "last_edited": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
            )

            print(f"\nUpdated note: {new_name}")
            with open(notes_file, "w") as f:
                json.dump(notes_data, f, indent=4)
        else:
            print("Invalid note number!")
    except ValueError:
        print("Please enter a valid number!")


def delete_notes():
    data_folder = Path("user_data")
    notes_file = data_folder / "user_notes.json"
    with open(notes_file, "r") as f:
        notes_data = json.load(f)

    if not notes_data:
        print("No notes to delete!")
        return

    print("\nWhich note would you like to delete?")
    print("-" * 50)
    for i, note in enumerate(notes_data, 1):
        print(f"\nNote #{i}")
        print(f"Name: {note['name']}")
        print(f"Tag: {note['tag']}")
        print("-" * 50)

    try:
        note_to_delete = int(input("Enter note number to delete (0 to cancel): ")) - 1
        if note_to_delete == -1:
            return
        if 0 <= note_to_delete < len(notes_data):
            deleted_note = notes_data.pop(note_to_delete)
            print(f"\nDeleted note: {deleted_note['name']}")
            with open(notes_file, "w") as f:
                json.dump(notes_data, f, indent=4)
        else:
            print("Invalid note number!")
    except ValueError:
        print("Please enter a valid number!")
