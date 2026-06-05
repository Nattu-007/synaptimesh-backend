# app/commands/mouse.py
import pyautogui

pyautogui.FAILSAFE = True

SCROLL_AMOUNT      = 500
SCROLL_AMOUNT_FAST = 1500

def scroll_up():
    pyautogui.scroll(SCROLL_AMOUNT)

def scroll_down():
    pyautogui.scroll(-SCROLL_AMOUNT)

def scroll_up_fast():
    pyautogui.scroll(SCROLL_AMOUNT_FAST)

def scroll_down_fast():
    pyautogui.scroll(-SCROLL_AMOUNT_FAST)

def click():
    pyautogui.click()

def right_click():
    pyautogui.rightClick()

def move_left(px: int = 250):
    x, y = pyautogui.position()
    pyautogui.moveTo(max(0, x - px), y, duration=0.2)          # clamp left edge

def move_right(px: int = 250):
    x, y = pyautogui.position()
    screen_w, _ = pyautogui.size()
    pyautogui.moveTo(min(screen_w, x + px), y, duration=0.2)   # clamp right edge

def move_up(px: int = 250):
    x, y = pyautogui.position()
    pyautogui.moveTo(x, max(0, y - px), duration=0.2)           # clamp top edge

def move_down(px: int = 250):
    x, y = pyautogui.position()
    _, screen_h = pyautogui.size()
    pyautogui.moveTo(x, min(screen_h, y + px), duration=0.2)    # clamp bottom edge