import datetime
from pathlib import Path
import json


def create_calendar_events():
    print("Create Events:")
    data_folder = Path("user_data")
    calendar_file = data_folder / "user_calendar.json"
    with open(calendar_file, "r") as f:
        user_calendar = json.load(f)


def read_calendar_events():
    print("Read Events")
    data_folder = Path("user_data")
    notes_file = data_folder / "user_notes.json"
    with open(notes_file, "r") as f:
        notes_data = json.load(f)


def delete_calendar_events():
    print("delete events")
    data_folder = Path("user_data")
    calendar_file = data_folder / "user_calendar.json"
    with open(calendar_file, "r") as f:
        user_calendar = json.load(f)


def update_calendar_events():
    print("update events")
    data_folder = Path("user_data")
    calendar_file = data_folder / "user_calendar.json"
    with open(calendar_file, "r") as f:
        user_calendar = json.load(f)