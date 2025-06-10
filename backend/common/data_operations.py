import json
from pathlib import Path

from backend.common.logging_config import logger
from backend.common.config import USER_DATA_FILE

DATA_FOLDER = Path("user_data")


def ensure_data_folder():
    if not DATA_FOLDER.exists():
        DATA_FOLDER.mkdir()
        logger.info("Created 'user_data' folder.")


def get_file_path(filename):
    return DATA_FOLDER / filename


def check_and_create_user_data():
    ensure_data_folder()
    file_path = get_file_path(USER_DATA_FILE)
    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump({}, f)
        logger.info(f"Created '{USER_DATA_FILE}' file.")


def load_json_data(filename):
    ensure_data_folder()
    file_path = get_file_path(filename)

    if not file_path.exists():
        with open(file_path, "w") as f:
            json.dump({} if filename == USER_DATA_FILE else [], f)
        logger.info(f"Created '{filename}' file.")

    with open(file_path, "r") as f:
        content = f.read()
        if not content.strip():
            logger.info(f"Skipping empty file: {filename}")
            return {} if filename == USER_DATA_FILE else []
        return json.loads(content)


def save_json_data(filename, data):
    ensure_data_folder()
    file_path = get_file_path(filename)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Saved data to '{filename}' file.")
