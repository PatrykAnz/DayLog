

def print_separator(): 
    print("-"*50)
def get_user_choice():
    choices={
        1: "Workout",
        2: "Calorie Counting",
        3: "Calendar", 
        4: "Finance"
        
    }
    total_amount = len(choices)
    while True:
        print(f"Choose from 1-{total_amount}")
        for key, value in choices.items():
            print(f"{key}. {value}")
        
        try:
            user_choice = int(input(""))
            if user_choice in choices:
                print(f"{choices[user_choice]}:")
            else:
                print_separator()
                print("Invalid choice. Enter a number from the list.")
                print_separator()
        except ValueError as e:
            print_separator()
            print("An error has ocurred. Make sure you entered a number")
            print(f"\nError info: \n{e}") 
            print_separator()
if __name__ == "__main__":
    get_user_choice()