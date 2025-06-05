from common.data_operations import ensure_data_folder, get_file_path, load_json_data, save_json_data


def get_workout():
    ensure_data_folder()
    file_path = get_file_path("user_workouts.json")
    workouts = load_json_data("user_workouts.json")
    if workouts is None:
        workouts = []
    
    new_workout = create_workout()
    workouts.append(new_workout)
    save_json_data("user_workouts.json", workouts)
    return new_workout


def create_workout():
    workout_name = input("Enter workout name (e.g., Back Pull):\n").strip()
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

    return {"workout_name": workout_name, "exercises": exercises}


if __name__ == "__main__":
    print("starting")
    get_workout()
