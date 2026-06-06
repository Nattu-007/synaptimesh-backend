# app/commands/calculator.py
import subprocess
import time
import pyautogui

pyautogui.FAILSAFE = True

def open_calculator():
    subprocess.Popen(["calc.exe"])
    time.sleep(2)   # Wait for calculator to fully open

def close_calculator():
    pyautogui.hotkey("alt", "F4")

def calculator_clear():
    pyautogui.press("escape")

def calculator_equals():
    pyautogui.press("enter")

def calculator_backspace():
    pyautogui.press("backspace")

def calculator_copy_result():
    pyautogui.hotkey("ctrl", "c")

def calculate_addition():
    """Types 3000 + 457 = in the calculator."""
    time.sleep(0.5)

    open_calculator()                       # Open fresh calculator
    time.sleep(1)

    pyautogui.typewrite("3000", interval=0.1)
    time.sleep(0.3)
    pyautogui.press("add")                 # + key on numpad
    time.sleep(0.3)
    pyautogui.typewrite("457", interval=0.1)
    time.sleep(0.3)
    pyautogui.press("enter")               # = key
    time.sleep(0.5)
    print("[CALCULATOR] Addition: 3000 + 457 = 3457")

def calculate_subtraction():
    """Types 3000 - 457 = in the calculator."""
    pyautogui.hotkey("alt", "F4")          # Close any open calculator first
    time.sleep(0.5)

    open_calculator()                       # Open fresh calculator
    time.sleep(1)

    pyautogui.typewrite("3000", interval=0.1)
    time.sleep(0.3)
    pyautogui.press("subtract")            # - key on numpad
    time.sleep(0.3)
    pyautogui.typewrite("457", interval=0.1)
    time.sleep(0.3)
    pyautogui.press("enter")               # = key
    time.sleep(0.5)
    print("[CALCULATOR] Subtraction: 3000 - 457 = 2543")