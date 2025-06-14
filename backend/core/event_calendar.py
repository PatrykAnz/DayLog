import datetime
from backend.common.database import add_calendar_event_to_db, get_all_calendar_events, update_calendar_event_in_db, delete_calendar_event_from_db
from backend.common.print_helpers import print_separator, cls
from backend.common.logging_config import logger
from backend.common.config import TABLE_CALENDAR

def get_calendar():
    choices = {
        1: "Create", 
        2: "Read", 
        3: "Update", 
        4: "Delete", 
        0: "Exit"
    }
    total_amount = len(choices)
    while True:
        logger.info(f"Choose from 0-{total_amount-1}")
        for key, value in choices.items():
            logger.info(f"{key}. {value}")
        try:
            user_choice = int(input(""))
            if user_choice in choices:
                if user_choice == 0:
                    return
                logger.info(f"{choices[user_choice]}:")
                if user_choice == 1:
                    create_calendar_event()
                elif user_choice == 2:
                    read_calendar_events() 
                elif user_choice == 3:
                    update_calendar_event()
                elif user_choice == 4:
                    delete_calendar_event() 
            else:
                print_separator()
                logger.warning("Invalid choice. Enter a number from the list.")
                print_separator()
        except ValueError as e:
            print_separator()
            logger.error("An error has occurred. Make sure you entered a number")
            logger.error(f"\nError info: \n{e}")
            print_separator() 

def create_calendar_event():
    event_name = input("Event name: ")
    event_tag = input("Tag (You can skip it): ")
    
    current_datetime = datetime.datetime.now()
    
    logger.info("\nEvent date (press Enter to use today's date):")
    
    year_input = input(f"Year (YYYY) [{current_datetime.year}]: ")
    year = current_datetime.year if year_input == '' else int(year_input)
    
    month_input = input(f"Month (1-12) [{current_datetime.month}]: ")
    month = current_datetime.month if month_input == '' else int(month_input)
    
    day_input = input(f"Day (1-31) [{current_datetime.day}]: ")
    day = current_datetime.day if day_input == '' else int(day_input)
    
    logger.info("\nEvent time (press Enter to use current time):")
    
    hour_input = input(f"Hour (0-23) [{current_datetime.hour}]: ")
    hour = current_datetime.hour if hour_input == '' else int(hour_input)
    
    minute_input = input(f"Minute (0-59) [{current_datetime.minute}]: ")
    minute = current_datetime.minute if minute_input == '' else int(minute_input)
    
    description = input("Event description: ")
    
    event_datetime = datetime.datetime(year, month, day, hour, minute)
    
    # Save to database instead of JSON
    add_calendar_event_to_db(event_name, event_tag, description, event_datetime)
    logger.info(f"Event '{event_name}' created successfully!")

def read_calendar_events():
    calendar_data = get_all_calendar_events()
    
    if not calendar_data:
        logger.warning("No events found")
        return
    
    logger.info("\nEvents:")
    print_separator()
    for i, event in enumerate(calendar_data, 1):
        event_id, name, tag, description, event_datetime, created_at, last_edit = event
        logger.info(f"\nEvent #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Date/Time: {event_datetime}")
        logger.info(f"Tag: {tag}")
        logger.info(f"Description: {description or 'None'}")
        logger.info(f"Created: {created_at}")
        logger.info(f"Last Edited: {last_edit}")
        print_separator()
    input(f"Press Enter to return")

def delete_calendar_event():
    calendar_data = get_all_calendar_events()

    if not calendar_data:
        logger.warning("No events to delete!")
        return
    
    logger.info("\nWhich event would you like to delete?")
    print_separator()
    for i, event in enumerate(calendar_data, 1):
        event_id, name, tag, description, event_datetime, created_at, last_edit = event
        logger.info(f"\nEvent #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Date/Time: {event_datetime}")
        logger.info(f"Tag: {tag}")
        print_separator()
    
    try:
        event_to_delete = int(input("Enter event number to delete (0 to cancel): ")) - 1
        
        if event_to_delete == -1:
            return
        
        if 0 <= event_to_delete < len(calendar_data):
            selected_event = calendar_data[event_to_delete]
            event_id, name, tag, description, event_datetime, created_at, last_edit = selected_event
            
            # Delete from database instead of JSON
            delete_calendar_event_from_db(event_id)
            logger.info(f"\nDeleted event: {name}")
        else:
            logger.warning("Invalid event number!")
    
    except ValueError:
        logger.error("Please enter a valid number!")

def update_calendar_event():
    calendar_data = get_all_calendar_events()

    if not calendar_data:
        logger.warning("No events to update!")
        return
    
    logger.info("\nWhich event would you like to update?")
    print_separator()
    for i, event in enumerate(calendar_data, 1):
        event_id, name, tag, description, event_datetime, created_at, last_edit = event
        logger.info(f"\nEvent #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Date/Time: {event_datetime}")
        logger.info(f"Tag: {tag}")
        print_separator()
    
    try:
        event_to_update = int(input("Enter event number to update (0 to cancel): ")) - 1
        
        if event_to_update == -1:
            return
        
        if 0 <= event_to_update < len(calendar_data):
            selected_event = calendar_data[event_to_update]
            event_id, current_name, current_tag, current_description, current_datetime, created_at, last_edit = selected_event
            
            logger.info("\nEnter new information (press Enter to keep current value):")
            
            new_name = input(f"New name [{current_name}]: ") or current_name
            new_tag = input(f"New tag [{current_tag}]: ") or current_tag
            new_desc = input(f"New description [{current_description or 'None'}]: ") or current_description
            
            # For simplicity, ask for new datetime as a string (YYYY-MM-DD HH:MM format)
            new_datetime_str = input(f"New date/time [{current_datetime}] (YYYY-MM-DD HH:MM): ") or current_datetime
            
            # Parse the datetime string
            if isinstance(new_datetime_str, str) and new_datetime_str != current_datetime:
                try:
                    new_datetime = datetime.datetime.strptime(new_datetime_str, "%Y-%m-%d %H:%M")
                except ValueError:
                    logger.warning("Invalid datetime format. Keeping current datetime.")
                    new_datetime = current_datetime
            else:
                new_datetime = current_datetime
            
            # Update in database instead of JSON
            update_calendar_event_in_db(event_id, new_name, new_tag, new_desc, new_datetime)
            logger.info(f"\nUpdated event: {new_name}")
        else:
            logger.warning("Invalid event number!")
    
    except ValueError:
        logger.error("Please enter a valid number!")

def display_upcoming_events(days=7):
    from backend.common.database import execute_query
    
    today = datetime.datetime.now().date()
    end_date = today + datetime.timedelta(days=days)
    
    # Query upcoming events from database
    upcoming_events = execute_query(
        f"SELECT * FROM {TABLE_CALENDAR} WHERE date(datetime) BETWEEN ? AND ? ORDER BY datetime",
        (today, end_date)
    )
    
    return upcoming_events


    