import sqlite3
import os

from common.config import MAIN_DATABASE_FILE

con = sqlite3.connect(MAIN_DATABASE_FILE)
cur = con.cursor()


def create_meals_table():
    cur.execute(
        """CREATE TABLE IF NOT EXISTS meals(
            id INT PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tag TEXT,
            calories INT,
            protein_grams INT,
            arbohydrates_grams INT,
            fat_grams INT
            )"""
    )


def add_meal_to_database(
    name, tag, calories, protein_grams, carbohydrates_grams, fat_grams
):
    cur.execute(
        "INSERT INTO meals VALUES (?, ?, ?, ?, ?, ?)",
        (name, tag, calories, protein_grams, carbohydrates_grams, fat_grams),
    )
    con.commit()


def get_database():
    create_meals_table()


if __name__ == "__main__":
    create_meals_table()
    add_meal_to_table("chicken", "Meal", 500, 400, 200, 100)
    res = cur.execute("SELECT * FROM meals")
    rows = res.fetchall()
    print(rows)
