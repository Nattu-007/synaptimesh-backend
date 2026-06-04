# app/commands/mouse.py
import pyautogui

pyautogui.FAILSAFE = True

SCROLL_AMOUNT = 5

def scroll_up():
    pyautogui.scroll(SCROLL_AMOUNT)

def scroll_down():
    pyautogui.scroll(-SCROLL_AMOUNT)

def click():
    pyautogui.click()

def right_click():
    pyautogui.rightClick()

def move_left(px: int = 50):
    x, y = pyautogui.position()
    pyautogui.moveTo(max(0, x - px), y, duration=0.2)

def move_right(px: int = 50):
    x, y = pyautogui.position()
    screen_w, _ = pyautogui.size()
    pyautogui.moveTo(min(screen_w, x + px), y, duration=0.2)