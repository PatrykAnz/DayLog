from pathlib import Path
import json

data_folder = Path("user_data")
data_file = data_folder / "user_data.json"


def check_and_create_user_data():
    if not data_folder.exists():
        data_folder.mkdir()
        print("Created 'user_data' folder.")

    if not data_file.exists():
        with open(data_file, "w") as f:
            json.dump({}, f)
        print("Created 'user_data.json' file.")
