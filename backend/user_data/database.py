import sqlite3
import os

from common.config import MAIN_DATABASE_FILE

con = sqlite3.connect(MAIN_DATABASE_FILE)
cur = con.cursor()

def create_meals_table():
    cur.execute(
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

def create_eaten_meals_table():
    cur.execute(
        """CREATE TABLE IF NOT EXISTS eaten_meals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            quantity INT DEFAULT 1,
            FOREIGN KEY (meal_id) REFERENCES meals(id)
            )"""
    )

def add_meal_to_table(name, tag, calories, protein_grams, carbohydrates_grams, fat_grams):
    cur.execute(
        "INSERT INTO meals VALUES (NULL, ?, ?, ?, ?, ?, ?)",
        (name, tag, calories, protein_grams, carbohydrates_grams, fat_grams),
    )
    con.commit()


def get_database():
    create_meals_table()
    create_eaten_meals_table()
    res = cur.execute("SELECT * FROM meals LIMIT 10")
    rows = res.fetchall()
    print(rows)
