import datetime

from common.data_operations import load_json_data, save_json_data
from common.logging_config import logger
from common.print_helpers import print_separator

USER_NOTES_FILE = "user_notes.json"


def get_notes():
    choices = {1: "Create", 2: "Read", 3: "Update", 4: "Delete", 0: "Exit"}
    total_amount = len(choices)
    while True:
        logger.info(f"Choose from 0-{total_amount-1}")
        for key, value in choices.items():
            logger.info(f"{key}. {value}")
        try:
            user_choice = int(input(""))
            if user_choice in choices:
                if user_choice == 0:
                    return None
                logger.info(f"{choices[user_choice]}:")
                if user_choice == 1:
                    return create_notes()
                elif user_choice == 2:
                    return read_notes()
                elif user_choice == 3:
                    return update_notes()
                elif user_choice == 4:
                    return delete_notes()
            else:
                print_separator()
                logger.warning("Invalid choice. Enter a number from the list.")
                print_separator()
        except ValueError as e:
            print_separator()
            logger.error("An error has occurred. Make sure you entered a number")
            logger.error(f"\nError info: \n{e}")
            print_separator()
            return None


def create_notes():
    notes_data = load_json_data(USER_NOTES_FILE)
    note_name = input("Note name: ")
    new_note_tag = input("Tag (You can skip it): ")
    new_note_create_date = datetime.datetime.now()

    new_note = {
        "name": note_name,
        "tag": new_note_tag,
        "created_at": new_note_create_date.strftime("%Y-%m-%d %H:%M"),
        "last_edited": new_note_create_date.strftime("%Y-%m-%d %H:%M"),
    }
    notes_data.append(new_note)

    save_json_data(USER_NOTES_FILE, notes_data)


def read_notes():
    notes_data = load_json_data(USER_NOTES_FILE)

    if not notes_data:
        logger.warning("No notes found")
        return

    logger.info("\nNotes:")
    print_separator()
    for i, note in enumerate(notes_data, 1):
        logger.info(f"\nNote #{i}")
        logger.info(f"Name: {note['name']}")
        logger.info(f"Tag: {note['tag']}")
        logger.info(f"Created: {note['created_at']}")
        logger.info(f"Last Edited: {note['last_edited']}")
        print_separator()
    input(f"Press Enter to return")


def update_notes():
    notes_data = load_json_data(USER_NOTES_FILE)

    if not notes_data:
        logger.warning("No notes to update!")
        return

    logger.info("\nWhich note would you like to update?")
    print_separator()
    for i, note in enumerate(notes_data, 1):
        logger.info(f"\nNote #{i}")
        logger.info(f"Name: {note['name']}")
        logger.info(f"Tag: {note['tag']}")
        print_separator()

    try:
        note_to_update = int(input("Enter note number to update (0 to cancel): ")) - 1
        if note_to_update == -1:
            return
        if 0 <= note_to_update < len(notes_data):
            logger.info("\nEnter new information (press Enter to keep current value):")
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

            logger.info(f"\nUpdated note: {new_name}")
            save_json_data(USER_NOTES_FILE, notes_data)
        else:
            logger.warning("Invalid note number!")
    except ValueError:
        logger.error("Please enter a valid number!")


def delete_notes():
    notes_data = load_json_data(USER_NOTES_FILE)

    if not notes_data:
        logger.warning("No notes to delete!")
        return

    logger.info("\nWhich note would you like to delete?")
    print_separator()
    for i, note in enumerate(notes_data, 1):
        logger.info(f"\nNote #{i}")
        logger.info(f"Name: {note['name']}")
        logger.info(f"Tag: {note['tag']}")
        print_separator()

    try:
        note_to_delete = int(input("Enter note number to delete (0 to cancel): ")) - 1
        if note_to_delete == -1:
            return
        if 0 <= note_to_delete < len(notes_data):
            deleted_note = notes_data.pop(note_to_delete)
            logger.info(f"\nDeleted note: {deleted_note['name']}")
            save_json_data(USER_NOTES_FILE, notes_data)
        else:
            logger.warning("Invalid note number!")
    except ValueError:
        logger.error("Please enter a valid number!")
