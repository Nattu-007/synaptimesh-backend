# app/commands/browser.py
import subprocess
import platform
import pyautogui

pyautogui.FAILSAFE = True

def open_browser():
    os_name = platform.system()
    if os_name == "Windows":
        subprocess.Popen(["start", "chrome"], shell=True)
    elif os_name == "Darwin":
        subprocess.Popen(["open", "-a", "Google Chrome"])
    else:
        subprocess.Popen(["xdg-open", "https://www.google.com"])

def close_browser():
    pyautogui.hotkey("alt", "F4")

def new_tab():
    pyautogui.hotkey("ctrl", "t")

def close_tab():
    pyautogui.hotkey("ctrl", "w")