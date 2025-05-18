import json
from pathlib import Path


DATA_FOLDER = Path("user_data")

def ensure_data_folder():
    if not DATA_FOLDER.exists():
        DATA_FOLDER.mkdir()
        print("Created 'user_data' folder.")

def get_file_path(filename):
    return DATA_FOLDER / filename

def load_json_data(filename):
    ensure_data_folder()
    file_path = get_file_path(filename)

    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump({} if filename == "user_data.json" else [], f)
        print(f"Created '{filename}' file.")

    with open(file_path, "r") as f:
        return json.load(f)

def save_json_data(filename, data):
    ensure_data_folder()
    file_path = get_file_path(filename)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return True
