import datetime
from utils.user_data_operations import check_and_create_user_data
import json
from pathlib import Path


def get_clock():
    check_and_create_user_data()
    data_folder = Path("user_data")
    data_file = data_folder / "user_data.json"
    current_time = datetime.datetime.now()

    with open(data_file, "r") as f:
        user_data = json.load(f)
    user_data["Clock"] = {
        "year": current_time.year,
        "month": current_time.month,
        "day": current_time.day,
        "hour": current_time.hour,
        "minute": current_time.minute,
    }
    print(json.dumps(user_data))
    with open(data_file, "w") as f:
        json.dump(user_data, f, indent=4)
    print(current_time.year)
