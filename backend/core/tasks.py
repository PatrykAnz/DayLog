import datetime
from backend.common.print_helpers import print_separator
from backend.common.database import add_task_to_db, get_all_tasks, update_task_in_db, delete_task_from_db
from backend.common.logging_config import logger

def get_tasks():
    choices = {0: "Exit", 1: "Create", 2: "Read", 3: "Update", 4: "Delete"}
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
                    return create_tasks()
                elif user_choice == 2:
                    return read_tasks()
                elif user_choice == 3:
                    return update_tasks()
                elif user_choice == 4:
                    return delete_tasks()
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


def create_tasks():
    task_name = input("Task name: ")
    new_task_tag = input("Tag (You can skip it): ")

    # Save to database instead of JSON
    add_task_to_db(task_name, new_task_tag)
    logger.info(f"Task '{task_name}' created successfully!")


def read_tasks():
    tasks_data = get_all_tasks()

    if not tasks_data:
        logger.warning("No tasks found")
        return

    logger.info("\nTasks:")
    print_separator()
    for i, task in enumerate(tasks_data, 1):
        task_id, name, tag, created_at, last_edited = task
        logger.info(f"\nTask #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        logger.info(f"Created: {created_at}")
        logger.info(f"Last Edited: {last_edited}")
        print_separator()
    input(f"Press Enter to return")


def update_tasks():
    tasks_data = get_all_tasks()

    if not tasks_data:
        logger.warning("No tasks to update!")
        return

    logger.info("\nWhich task would you like to update?")
    print_separator()
    for i, task in enumerate(tasks_data, 1):
        task_id, name, tag, created_at, last_edited = task
        logger.info(f"\nTask #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        print_separator()

    try:
        task_to_update = int(input("Enter task number to update (0 to cancel): ")) - 1
        if task_to_update == -1:
            return
        if 0 <= task_to_update < len(tasks_data):
            selected_task = tasks_data[task_to_update]
            task_id, current_name, current_tag, created_at, last_edited = selected_task
            
            logger.info("\nEnter new information (press Enter to keep current value):")
            new_name = input(f"New name [{current_name}]: ") or current_name
            new_tag = input(f"New tag [{current_tag}]: ") or current_tag

            # Update in database instead of JSON
            update_task_in_db(task_id, new_name, new_tag)
            logger.info(f"\nUpdated task: {new_name}")
        else:
            logger.warning("Invalid task number!")
    except ValueError:
        logger.error("Please enter a valid number!")


def delete_tasks():
    tasks_data = get_all_tasks()

    if not tasks_data:
        logger.warning("No tasks to delete!")
        return

    logger.info("\nWhich task would you like to delete?")
    print_separator()
    for i, task in enumerate(tasks_data, 1):
        task_id, name, tag, created_at, last_edited = task
        logger.info(f"\nTask #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        print_separator()

    try:
        task_to_delete = int(input("Enter task number to delete (0 to cancel): ")) - 1
        if task_to_delete == -1:
            return
        if 0 <= task_to_delete < len(tasks_data):
            selected_task = tasks_data[task_to_delete]
            task_id, name, tag, created_at, last_edited = selected_task
            
            # Delete from database instead of JSON
            delete_task_from_db(task_id)
            logger.info(f"\nDeleted task: {name}")
        else:
            logger.warning("Invalid task number!")
    except ValueError:
        logger.error("Please enter a valid number!")
