import sqlite3
import os

from common.config import MAIN_DATABASE_FILE

#COMMON USAGE
def get_connection():
    return sqlite3.connect(MAIN_DATABASE_FILE)


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


#CREATE TABLES
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
            calories INT,
            protein_grams INT,
            carbohydrates_grams INT,
            fat_grams INT
        )"""
    )

def create_meals_today_table():
    execute_query(
        """CREATE TABLE IF NOT EXISTS meals_today(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INT NOT NULL,
            time DATETIME DEFAULT CURRENT_TIMESTAMP,
            quantity INT DEFAULT 1,
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

def create_workouts_table():#TODO later
    execute_query(
        """CREATE TABLE IF NOT EXISTS workouts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )"""
    )

def add_meal_to_table(
    name, tag, calories, protein_grams, carbohydrates_grams, fat_grams
):
    execute_query(
        "INSERT INTO meals (name, tag, calories, protein_grams, carbohydrates_grams, fat_grams) VALUES (?, ?, ?, ?, ?, ?)",
        (name, tag, calories, protein_grams, carbohydrates_grams, fat_grams),
    )


def get_database():
    create_meals_table()
    create_meals_today_table()
    add_meal_to_table("test", "tag", "calories", 100, 20, 30, 40)
    con, cur = get_cursor()
    cur.execute("SELECT * FROM meals_today LIMIT 10")
    print(row)
    cur.execute("SELECT * FROM meals LIMIT 10")
    print(rows)
