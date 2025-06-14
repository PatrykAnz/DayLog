import sqlite3
import os
import json
from datetime import datetime

from backend.common.config import (
    TABLE_NOTES,
    TABLE_TASKS,
    TABLE_CALENDAR,
    TABLE_WORKOUTS,
    TABLE_MEALS,
    TABLE_MEALS_TODAY,
    TABLE_DIETLY,
    TABLE_GELOCATION,
    TABLE_WEATHER,
    TABLE_GARMIN,
    TABLE_WITHINGS,
    TABLE_API_TOKENS,
    MAIN_DATABASE_PATH
)
from backend.common.logging_config import logger

# COMMON USAGE
def get_connection():
    return sqlite3.connect(MAIN_DATABASE_PATH)


def get_cursor():
    con = get_connection()
    return con, con.cursor()


def execute_query(query, params=()):
    con, cur = get_cursor()
    try:
        cur.execute(query, params)
        con.commit()
        return cur.fetchall()
    finally:
        con.close()


# CREATE TABLES
def create_calendar_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_CALENDAR}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            description TEXT,
            datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_edit DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_dietly_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_DIETLY}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            calories INT,
            protein_grams INT,
            carbohydrates_grams INT,
            fat_grams INT
        )"""
    )

def create_garmin_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_GARMIN}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            steps INT,
            sleep INT,
            awake INT,
            date DATE DEFAULT CURRENT_DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_meals_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_MEALS}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            description TEXT,
            calories INT,
            protein_grams INT,
            carbohydrates_grams INT,
            fat_grams INT,
            mass_grams INT
        )"""
    )


def create_meals_today_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_MEALS_TODAY}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INT,
            meal_source TEXT DEFAULT 'manual',
            name TEXT NOT NULL,
            tag TEXT,
            calories FLOAT,
            protein_grams FLOAT,
            carbohydrates_grams FLOAT,
            fat_grams FLOAT,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            grams_consumed FLOAT DEFAULT 0.0,
            FOREIGN KEY (meal_id) REFERENCES {TABLE_MEALS}(id)
        )"""
    )

def create_notes_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_NOTES}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_edited DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_tasks_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_TASKS}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_edited DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_withings_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_WITHINGS}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            weight FLOAT,
            date DATE DEFAULT CURRENT_DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_workouts_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_WORKOUTS}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_edited DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_weather_data_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_WEATHER}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            temperature FLOAT,
            description TEXT,
            humidity INT,
            wind_speed FLOAT,
            weather_data TEXT,
            date DATE DEFAULT CURRENT_DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_geolocation_data_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_GELOCATION}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude FLOAT,
            longitude FLOAT,
            address TEXT,
            city TEXT,
            country TEXT,
            date DATE DEFAULT CURRENT_DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_api_tokens_table():
    execute_query(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_API_TOKENS}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service TEXT NOT NULL UNIQUE,
            token_data TEXT NOT NULL,
            expires_at DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

# DATABASE OPERATIONS FOR EACH TABLE

# Notes operations
def add_note_to_db(name, tag):
    execute_query(
        f"INSERT INTO {TABLE_NOTES} (name, tag) VALUES (?, ?)",
        (name, tag)
    )

def get_all_notes():
    return execute_query(f"SELECT * FROM {TABLE_NOTES} ORDER BY created_at DESC")

def update_note_in_db(note_id, name, tag):
    execute_query(
        f"UPDATE {TABLE_NOTES} SET name = ?, tag = ?, last_edited = CURRENT_TIMESTAMP WHERE id = ?",
        (name, tag, note_id)
    )

def delete_note_from_db(note_id):
    execute_query(f"DELETE FROM {TABLE_NOTES} WHERE id = ?", (note_id,))

# Tasks operations
def add_task_to_db(name, tag):
    execute_query(
        "INSERT INTO tasks (name, tag) VALUES (?, ?)",
        (name, tag)
    )

def get_all_tasks():
    return execute_query("SELECT * FROM tasks ORDER BY created_at DESC")

def update_task_in_db(task_id, name, tag):
    execute_query(
        "UPDATE tasks SET name = ?, tag = ?, last_edited = CURRENT_TIMESTAMP WHERE id = ?",
        (name, tag, task_id)
    )

def delete_task_from_db(task_id):
    execute_query("DELETE FROM tasks WHERE id = ?", (task_id,))

# Calendar operations
def add_calendar_event_to_db(name, tag, description, event_datetime):
    execute_query(
        "INSERT INTO calendar (name, tag, description, datetime) VALUES (?, ?, ?, ?)",
        (name, tag, description, event_datetime)
    )

def get_all_calendar_events():
    return execute_query("SELECT * FROM calendar ORDER BY datetime DESC")

def update_calendar_event_in_db(event_id, name, tag, description, event_datetime):
    execute_query(
        "UPDATE calendar SET name = ?, tag = ?, description = ?, datetime = ?, last_edit = CURRENT_TIMESTAMP WHERE id = ?",
        (name, tag, description, event_datetime, event_id)
    )

def delete_calendar_event_from_db(event_id):
    execute_query("DELETE FROM calendar WHERE id = ?", (event_id,))

# Workouts operations
def add_workout_to_db(name, tag, description):
    execute_query(
        "INSERT INTO workouts (name, tag, description) VALUES (?, ?, ?)",
        (name, tag, description)
    )

def get_all_workouts():
    return execute_query("SELECT * FROM workouts ORDER BY created_at DESC")

def update_workout_in_db(workout_id, name, tag, description):
    execute_query(
        "UPDATE workouts SET name = ?, tag = ?, description = ?, last_edited = CURRENT_TIMESTAMP WHERE id = ?",
        (name, tag, description, workout_id)
    )

def delete_workout_from_db(workout_id):
    execute_query("DELETE FROM workouts WHERE id = ?", (workout_id,))

# API Data operations
def save_garmin_data(steps, sleep, awake):
    # Check if data for today already exists
    today = datetime.now().date()
    existing = execute_query("SELECT id FROM garmin_data WHERE date = ?", (today,))
    
    if existing:
        execute_query(
            "UPDATE garmin_data SET steps = ?, sleep = ?, awake = ? WHERE date = ?",
            (steps, sleep, awake, today)
        )
    else:
        execute_query(
            "INSERT INTO garmin_data (steps, sleep, awake, date) VALUES (?, ?, ?, ?)",
            (steps, sleep, awake, today)
        )

def get_latest_garmin_data():
    result = execute_query("SELECT * FROM garmin_data ORDER BY date DESC LIMIT 1")
    return result[0] if result else None

def save_withings_data(weight):
    today = datetime.now().date()
    existing = execute_query("SELECT id FROM withings_data WHERE date = ?", (today,))
    
    if existing:
        execute_query(
            "UPDATE withings_data SET weight = ? WHERE date = ?",
            (weight, today)
        )
    else:
        execute_query(
            "INSERT INTO withings_data (weight, date) VALUES (?, ?)",
            (weight, today)
        )

def get_latest_withings_data():
    result = execute_query("SELECT * FROM withings_data ORDER BY date DESC LIMIT 1")
    return result[0] if result else None

def save_weather_data(location, temperature, description, humidity, wind_speed, weather_data):
    today = datetime.now().date()
    execute_query(
        "INSERT INTO weather_data (location, temperature, description, humidity, wind_speed, weather_data, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (location, temperature, description, humidity, wind_speed, json.dumps(weather_data), today)
    )

def save_geolocation_data(latitude, longitude, address, city, country):
    today = datetime.now().date()
    execute_query(
        "INSERT INTO geolocation_data (latitude, longitude, address, city, country, date) VALUES (?, ?, ?, ?, ?, ?)",
        (latitude, longitude, address, city, country, today)
    )

def save_api_token(service, token_data, expires_at=None):
    existing = execute_query("SELECT id FROM api_tokens WHERE service = ?", (service,))
    
    if existing:
        execute_query(
            "UPDATE api_tokens SET token_data = ?, expires_at = ?, updated_at = CURRENT_TIMESTAMP WHERE service = ?",
            (json.dumps(token_data), expires_at, service)
        )
    else:
        execute_query(
            "INSERT INTO api_tokens (service, token_data, expires_at) VALUES (?, ?, ?)",
            (service, json.dumps(token_data), expires_at)
        )

def get_api_token(service):
    result = execute_query("SELECT token_data, expires_at FROM api_tokens WHERE service = ?", (service,))
    if result:
        token_data, expires_at = result[0]
        return json.loads(token_data), expires_at
    return None, None

def add_meal_to_table(name, tag, description, calories, protein_grams, carbohydrates_grams, fat_grams, mass_grams):
    execute_query(
        "INSERT INTO meals (name, tag, description, calories, protein_grams, carbohydrates_grams, fat_grams, mass_grams) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (name, tag, description, calories, protein_grams, carbohydrates_grams, fat_grams, mass_grams,)
    )

def update_meal_in_table(meal_id, name, tag, description, calories, protein_grams, carbohydrates_grams, fat_grams, mass_grams):
    execute_query(
        "UPDATE meals SET name = ?, tag = ?, description = ?, calories = ?, protein_grams = ?, carbohydrates_grams = ?, fat_grams = ?, mass_grams = ? WHERE id = ?",
        (name, tag, description, calories, protein_grams, carbohydrates_grams, fat_grams, mass_grams, meal_id)
    )

def get_meal_by_id(meal_id):
    result = execute_query("SELECT * FROM meals WHERE id = ?", (meal_id,))
    return result[0] if result else None

def delete_meal_from_table(meal_id):
    execute_query("DELETE FROM meals WHERE id = ?", (meal_id,))

def read_last_rows_from_table(table_name):
    last_rows = execute_query(f"SELECT * FROM {table_name} LIMIT 5")
    return last_rows

def check_name_from_table(table_name, name):
    return execute_query(
        f"SELECT * FROM {table_name} WHERE name = ? LIMIT 10", (name,)
    )

def get_database():
    create_calendar_table()
    create_dietly_table()
    create_garmin_table()
    create_meals_table()
    create_meals_today_table()
    create_notes_table()
    create_tasks_table()
    create_withings_table()
    create_workouts_table()
    create_weather_data_table()
    create_geolocation_data_table()
    create_api_tokens_table()

def add_dietly_meal_to_table(name, tag, calories, protein_grams, carbohydrates_grams, fat_grams):
    execute_query(
        "INSERT INTO dietly (name, tag, calories, protein_grams, carbohydrates_grams, fat_grams) VALUES (?, ?, ?, ?, ?, ?)",
        (name, tag, calories, protein_grams, carbohydrates_grams, fat_grams)
    )

def check_dietly_meal_exists(name):
    result = execute_query("SELECT * FROM dietly WHERE name = ?", (name,))
    return result[0] if result else None

def get_dietly_meal_by_id(meal_id):
    result = execute_query("SELECT * FROM dietly WHERE id = ?", (meal_id,))
    return result[0] if result else None

def add_meal_today_from_dietly(dietly_meal_id, grams_consumed):
    meal_data = get_dietly_meal_by_id(dietly_meal_id)
    if not meal_data:
        return
    
    meal_id, name, tag, calories, protein, carbs, fat = meal_data
    
    if tag == "100g":
        actual_calories = calories * grams_consumed / 100
        actual_protein = protein * grams_consumed / 100
        actual_carbs = carbs * grams_consumed / 100
        actual_fat = fat * grams_consumed / 100
    else:
        actual_calories = calories
        actual_protein = protein
        actual_carbs = carbs
        actual_fat = fat
    
    execute_query(
        """INSERT INTO meals_today 
           (meal_id, meal_source, name, tag, calories, protein_grams, carbohydrates_grams, fat_grams, grams_consumed) 
           VALUES (?, 'dietly', ?, ?, ?, ?, ?, ?, ?)""",
        (dietly_meal_id, name, tag, actual_calories, actual_protein, actual_carbs, actual_fat, grams_consumed)
    )

def get_all_dietly_meals():
    return execute_query("SELECT * FROM dietly")
