from os import system, name

def print_separator():
     print("-" * 50)

def cls():
    system("cls" if name == "nt" else "clear")