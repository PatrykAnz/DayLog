import datetime
from utils.data_operations import load_json_data, save_json_data
import json


def get_clock():
    current_time = datetime.datetime.now()
    user_data = load_json_data("user_data.json")
    
    user_data["Clock"] = {
        "year": current_time.year,
        "month": current_time.month,
        "day": current_time.day,
        "hour": current_time.hour,
        "minute": current_time.minute,
    }
    print(json.dumps(user_data))
    save_json_data("user_data.json", user_data)