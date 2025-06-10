import datetime
from backend.common.data_operations import load_json_data, save_json_data
from backend.common.print_helpers import print_separator, cls
from backend.common.logging_config import logger
from backend.common.config import USER_CALENDAR_FILE

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
    calendar_data = load_json_data(USER_CALENDAR_FILE)
    
    if calendar_data is None:
        calendar_data = []
    
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
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    event_datetime = datetime.datetime(year, month, day, hour, minute)
    event_date_formatted = event_datetime.strftime("%Y-%m-%d")
    event_time_formatted = event_datetime.strftime("%H:%M")
    
    new_event = {
        "name": event_name,
        "date": event_date_formatted,
        "time": event_time_formatted,
        "tag": event_tag,
        "description": description,
        "created_at": current_time,
        "last_edited": current_time
    }
    
    calendar_data.append(new_event)
    save_json_data(USER_CALENDAR_FILE, calendar_data)

def read_calendar_events():
    calendar_data = load_json_data(USER_CALENDAR_FILE)
    
    if not calendar_data:
        logger.warning("No events found")
        return
    
    logger.info("\nEvents:")
    print_separator()
    for i, event in enumerate(calendar_data, 1):
        logger.info(f"\nEvent #{i}")
        logger.info(f"Name: {event['name']}")
        logger.info(f"Date: {event.get('date', 'Not specified')}")
        logger.info(f"Time: {event.get('time', 'Not specified')}")
        logger.info(f"Tag: {event['tag']}")
        logger.info(f"Description: {event.get('description', 'None')}")
        logger.info(f"Created: {event['created_at']}")
        logger.info(f"Last Edited: {event['last_edited']}")
        print_separator()
    input(f"Press Enter to return")

def delete_calendar_event():
    calendar_data = load_json_data(USER_CALENDAR_FILE)

    if not calendar_data:
        logger.warning("No events to delete!")
        return
    
    logger.info("\nWhich event would you like to delete?")
    print_separator()
    for i, event in enumerate(calendar_data, 1):
        logger.info(f"\nEvent #{i}")
        logger.info(f"Name: {event['name']}")
        logger.info(f"Date: {event.get('date', 'Not specified')} {event.get('time', '')}")
        logger.info(f"Tag: {event['tag']}")
        print_separator()
    
    try:
        event_to_delete = int(input("Enter event number to delete (0 to cancel): ")) - 1
        
        if event_to_delete == -1:
            return
        
        if 0 <= event_to_delete < len(calendar_data):
            deleted_event = calendar_data.pop(event_to_delete)
            logger.info(f"\nDeleted event: {deleted_event['name']}")
            save_json_data(USER_CALENDAR_FILE, calendar_data)
        else:
            logger.warning("Invalid event number!")
    
    except ValueError:
        logger.error("Please enter a valid number!")

def update_calendar_event():
    calendar_data = load_json_data(USER_CALENDAR_FILE)

    if not calendar_data:
        logger.warning("No events to update!")
        return
    
    logger.info("\nWhich event would you like to update?")
    print_separator()
    for i, event in enumerate(calendar_data, 1):
        logger.info(f"\nEvent #{i}")
        logger.info(f"Name: {event['name']}")
        logger.info(f"Date: {event.get('date', 'Not specified')} {event.get('time', '')}")
        logger.info(f"Tag: {event['tag']}")
        print_separator()
    
    try:
        event_to_update = int(input("Enter event number to update (0 to cancel): ")) - 1
        
        if event_to_update == -1:
            return
        
        if 0 <= event_to_update < len(calendar_data):
            event = calendar_data[event_to_update]
            
            logger.info("\nEnter new information (press Enter to keep current value):")
            
            new_name = input(f"New name [{event['name']}]: ") or event['name']
            
            date_str = event.get('date', 'Not set')
            new_date = input(f"New date [{date_str}] (YYYY-MM-DD): ") or date_str
            
            time_str = event.get('time', 'Not set')
            new_time = input(f"New time [{time_str}] (HH:MM): ") or time_str
            
            new_tag = input(f"New tag [{event['tag']}]: ") or event['tag']
            
            desc_str = event.get('description', 'None')
            new_desc = input(f"New description [{desc_str}]: ") or desc_str
            
            calendar_data[event_to_update].update({
                "name": new_name,
                "date": new_date,
                "time": new_time,
                "tag": new_tag,
                "description": new_desc,
                "last_edited": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            logger.info(f"\nUpdated event: {new_name}")
            save_json_data(USER_CALENDAR_FILE, calendar_data)
        else:
            logger.warning("Invalid event number!")
    
    except ValueError:
        logger.error("Please enter a valid number!")

def display_upcoming_events(days=7):
    calendar_data = load_json_data(USER_CALENDAR_FILE)
    
    if not calendar_data:
        return []
    
    today = datetime.datetime.now().date()
    end_date = today + datetime.timedelta(days=days)
    
    upcoming = []
    
    for event in calendar_data:
        if 'date' in event:
            try:
                event_date = datetime.datetime.strptime(event['date'], "%Y-%m-%d").date()
                if today <= event_date <= end_date:
                    upcoming.append(event)
            except ValueError:
                pass
    
    return sorted(upcoming, key=lambda x: x['date'])


    