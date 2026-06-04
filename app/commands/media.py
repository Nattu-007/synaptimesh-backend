# app/commands/media.py
import pyautogui

pyautogui.FAILSAFE = True

def play():
    pyautogui.press("playpause")

def pause():
    pyautogui.press("playpause")

def stop():
    pyautogui.press("stop")

def volume_up():
    pyautogui.press("volumeup")

def volume_down():
    pyautogui.press("volumedown")

def mute():
    pyautogui.press("volumemute")

def next_track():
    pyautogui.press("nexttrack")

def prev_track():
    pyautogui.press("prevtrack")