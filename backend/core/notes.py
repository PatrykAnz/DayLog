import datetime

from backend.common.database import add_note_to_db, get_all_notes, update_note_in_db, delete_note_from_db
from backend.common.logging_config import logger
from backend.common.print_helpers import print_separator


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
    note_name = input("Note name: ")
    new_note_tag = input("Tag (You can skip it): ")

    # Save to database instead of JSON
    add_note_to_db(note_name, new_note_tag)
    logger.info(f"Note '{note_name}' created successfully!")


def read_notes():
    notes_data = get_all_notes()

    if not notes_data:
        logger.warning("No notes found")
        return

    logger.info("\nNotes:")
    print_separator()
    for i, note in enumerate(notes_data, 1):
        note_id, name, tag, created_at, last_edited = note
        logger.info(f"\nNote #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        logger.info(f"Created: {created_at}")
        logger.info(f"Last Edited: {last_edited}")
        print_separator()
    input(f"Press Enter to return")


def update_notes():
    notes_data = get_all_notes()

    if not notes_data:
        logger.warning("No notes to update!")
        return

    logger.info("\nWhich note would you like to update?")
    print_separator()
    for i, note in enumerate(notes_data, 1):
        note_id, name, tag, created_at, last_edited = note
        logger.info(f"\nNote #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        print_separator()

    try:
        note_to_update = int(input("Enter note number to update (0 to cancel): ")) - 1
        if note_to_update == -1:
            return
        if 0 <= note_to_update < len(notes_data):
            selected_note = notes_data[note_to_update]
            note_id, current_name, current_tag, created_at, last_edited = selected_note
            
            logger.info("\nEnter new information (press Enter to keep current value):")
            new_name = input(f"New name [{current_name}]: ") or current_name
            new_tag = input(f"New tag [{current_tag}]: ") or current_tag

            # Update in database instead of JSON
            update_note_in_db(note_id, new_name, new_tag)
            logger.info(f"\nUpdated note: {new_name}")
        else:
            logger.warning("Invalid note number!")
    except ValueError:
        logger.error("Please enter a valid number!")


def delete_notes():
    notes_data = get_all_notes()

    if not notes_data:
        logger.warning("No notes to delete!")
        return

    logger.info("\nWhich note would you like to delete?")
    print_separator()
    for i, note in enumerate(notes_data, 1):
        note_id, name, tag, created_at, last_edited = note
        logger.info(f"\nNote #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        print_separator()

    try:
        note_to_delete = int(input("Enter note number to delete (0 to cancel): ")) - 1
        if note_to_delete == -1:
            return
        if 0 <= note_to_delete < len(notes_data):
            selected_note = notes_data[note_to_delete]
            note_id, name, tag, created_at, last_edited = selected_note
            
            # Delete from database instead of JSON
            delete_note_from_db(note_id)
            logger.info(f"\nDeleted note: {name}")
        else:
            logger.warning("Invalid note number!")
    except ValueError:
        logger.error("Please enter a valid number!")
