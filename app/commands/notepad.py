# app/commands/notepad.py
import subprocess
import time
import pyautogui

pyautogui.FAILSAFE = True

def open_notepad():
    subprocess.Popen(["notepad.exe"])
    time.sleep(2)   # Wait for notepad to fully open

def close_notepad():
    pyautogui.hotkey("alt", "F4")
    time.sleep(0.5)
    pyautogui.press("tab")                 # Move focus to "Don't Save" button
    pyautogui.press("enter")               # Confirm close without saving

def notepad_save():
    pyautogui.hotkey("ctrl", "s")

def notepad_select_all():
    pyautogui.hotkey("ctrl", "a")

def notepad_undo():
    pyautogui.hotkey("ctrl", "z")

def notepad_new_file():
    pyautogui.hotkey("ctrl", "n")

def notepad_copy():
    pyautogui.hotkey("ctrl", "c")

def notepad_paste():
    pyautogui.hotkey("ctrl", "v")

def notepad_full_automation():
    """
    Full notepad automation sequence:
    1. Opens Notepad
    2. Types a header
    3. Types the automation log line by line
    4. Ends with 'Automation is done'
    5. Saves the file
    """
    open_notepad()
    time.sleep(1)

    lines = [
        "========================================",
        "  SYNAPTIMESH — Desktop Automation Log  ",
        "========================================",
        "",
        "Session   : EEG-Controlled Automation",
        "Headset   : Emotiv EPOC X",
        "Backend   : SynaptiMesh FastAPI Server",
        "",
        "Commands Executed:",
        "  [1] OPEN_NOTEPAD      — Notepad launched",
        "  [2] NOTEPAD_SELECT_ALL — All text selected",
        "  [3] NOTEPAD_COPY      — Text copied",
        "  [4] NOTEPAD_SAVE      — File saved",
        "  [5] OPEN_CALCULATOR   — Calculator launched",
        "  [6] Addition          — 3000 + 457 = 3457",
        "  [7] Subtraction       — 3000 - 457 = 2543",
        "  [8] CLOSE_CALCULATOR  — Calculator closed",
        "",
        "========================================",
        "         Automation is done             ",
        "========================================",
    ]

    for line in lines:
        pyautogui.typewrite(line, interval=0.03)
        pyautogui.press("enter")
        time.sleep(0.1)

    time.sleep(0.5)
    pyautogui.hotkey("ctrl", "s")          # Save the file
    time.sleep(1)

    # Handle "Save As" dialog if it appears (first save)
    pyautogui.typewrite("synaptimesh_automation_log", interval=0.05)
    time.sleep(0.3)
    pyautogui.press("enter")               # Confirm save
    time.sleep(0.5)

    print("[NOTEPAD] Automation log written and saved")
    print("[NOTEPAD] Automation is done")