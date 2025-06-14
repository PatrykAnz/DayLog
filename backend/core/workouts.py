from backend.common.database import add_workout_to_db, get_all_workouts
from backend.common.logging_config import logger
import json


def get_workout():
    choices = {1: "Create", 2: "Read", 0: "Exit"}
    total_amount = len(choices)
    while True:
        logger.info(f"Choose from 0-{total_amount-1}")
        for key, value in choices.items():
            logger.info(f"{key}. {value}")
        try:
            user_choice = int(input(""))
            if user_choice in choices:
                if user_choice == 0:
                    return None
                logger.info(f"{choices[user_choice]}:")
                if user_choice == 1:
                    return create_workout()
                elif user_choice == 2:
                    return read_workouts()
            else:
                logger.warning("Invalid choice. Enter a number from the list.")
        except ValueError as e:
            logger.error("An error has occurred. Make sure you entered a number")
            logger.error(f"\nError info: \n{e}")
            return None


def create_workout():
    workout_name = input("Enter workout name (e.g., Back Pull):\n").strip()
    workout_tag = input("Tag (You can skip it): ").strip()
    
    while True:
        try:
            amount_of_exercises = int(
                input("Enter number of exercises for this day (e.g., 5):\n")
            )
            break
        except ValueError:
            print("Please enter a whole number.")

    exercises = []

    for i in range(1, amount_of_exercises + 1):
        name = input(f"Exercise {i} name:\n").strip()

        while True:
            try:
                sets = int(input("How many sets?\n"))
                break
            except ValueError:
                print("Please enter a whole number.")

        sets_data = []
        for j in range(1, sets + 1):
            while True:
                try:
                    reps = int(input(f"Repetitions in set {j}:\n"))
                    break
                except ValueError:
                    print("Please enter a whole number.")
            sets_data.append({"set": j, "reps": reps})

        exercises.append({"exercise": name, "sets": sets_data})

    workout_data = {"workout_name": workout_name, "exercises": exercises}
    
    # Save to database instead of JSON
    add_workout_to_db(workout_name, workout_tag, json.dumps(workout_data))
    logger.info(f"Workout '{workout_name}' created successfully!")
    
    return workout_data


def read_workouts():
    workouts = get_all_workouts()
    
    if not workouts:
        logger.warning("No workouts found")
        return
    
    logger.info("\nWorkouts:")
    logger.info("-" * 50)
    for i, workout in enumerate(workouts, 1):
        workout_id, name, tag, description, created_at, last_edited = workout
        logger.info(f"\nWorkout #{i}")
        logger.info(f"Name: {name}")
        logger.info(f"Tag: {tag}")
        logger.info(f"Created: {created_at}")
        logger.info(f"Last Edited: {last_edited}")
        
        # Parse workout details from description
        if description:
            try:
                workout_details = json.loads(description)
                if "exercises" in workout_details:
                    logger.info("Exercises:")
                    for exercise in workout_details["exercises"]:
                        logger.info(f"  - {exercise['exercise']}")
                        for set_data in exercise["sets"]:
                            logger.info(f"    Set {set_data['set']}: {set_data['reps']} reps")
            except (json.JSONDecodeError, KeyError):
                logger.info(f"Description: {description}")
        
        logger.info("-" * 50)
    input(f"Press Enter to return")


if __name__ == "__main__":
    get_workout()
