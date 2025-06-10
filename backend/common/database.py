import sqlite3
import os

from common.config import MAIN_DATABASE_PATH
from common.logging_config import logger

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
        """CREATE TABLE IF NOT EXISTS calendar(
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
        """CREATE TABLE IF NOT EXISTS dietly(
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
        """CREATE TABLE IF NOT EXISTS garmin(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            steps INT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_meals_table():
    execute_query(
        """CREATE TABLE IF NOT EXISTS meals(
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
    # Add description column to existing tables if it doesn't exist
    try:
        execute_query("ALTER TABLE meals ADD COLUMN description TEXT")
    except:
        # Column already exists, ignore the error
        pass

def create_meals_today_table():
    execute_query(
        """CREATE TABLE IF NOT EXISTS meals_today(
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
            percentage FLOAT DEFAULT 100.0,
            FOREIGN KEY (meal_id) REFERENCES meals(id)
        )"""
    )

def create_notes_table():
    execute_query(
        """CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_edited DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_tasks_table():
    execute_query(
        """CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_edited DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_withings_table():
    execute_query(
        """CREATE TABLE IF NOT EXISTS withings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight FLOAT,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

def create_workouts_table():  # TODO later
    execute_query(
        """CREATE TABLE IF NOT EXISTS workouts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )"""
    )


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

def add_meal_today_from_dietly(dietly_meal_id, percentage):
    # Get the meal data from dietly table
    meal_data = get_dietly_meal_by_id(dietly_meal_id)
    if not meal_data:
        return
    
    meal_id, name, tag, calories, protein, carbs, fat = meal_data
    
    # Calculate actual values based on percentage
    actual_calories = calories * percentage / 100
    actual_protein = protein * percentage / 100
    actual_carbs = carbs * percentage / 100
    actual_fat = fat * percentage / 100
    
    execute_query(
        """INSERT INTO meals_today 
           (meal_id, meal_source, name, tag, calories, protein_grams, carbohydrates_grams, fat_grams, percentage) 
           VALUES (?, 'dietly', ?, ?, ?, ?, ?, ?, ?)""",
        (dietly_meal_id, name, tag, actual_calories, actual_protein, actual_carbs, actual_fat, percentage)
    )

def get_all_dietly_meals():
    return execute_query("SELECT * FROM dietly")
