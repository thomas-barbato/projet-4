"""import"""
import os
from time import sleep


def clear_screen(sleep_val: int = 0):
    """_clear_screen_
    Args:
        sleep_val (int, optional): _sleep_val_. Defaults to 0.
    clear screen
    """
    sleep(sleep_val)
    return os.system("cls")


def exit_to_console(sleep_val: int = 0):
    """_exit_
    Args:
        sleep_val (int, optional): _description_. Defaults to 0.
    exit program
    """
    sleep(sleep_val)
    return os.system("exit")
