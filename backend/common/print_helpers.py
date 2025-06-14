from os import system, name
from backend.common.logging_config import logger

def print_separator():
     logger.info("-" * 50)

def cls():
    system("cls" if name == "nt" else "clear")