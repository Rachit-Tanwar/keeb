import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Welcome to typing speed test!")
    stdscr.addstr(1, 0, "Select Difficulty : ")
    stdscr.addstr(2, 0, "1. Easy")
    stdscr.addstr(3, 0, "2. Medium")
    stdscr.addstr(4, 0, "3. Hard")
    stdscr.addstr(5, 0, "Press 1, 2, or 3 to start.")
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        match key:
            case '1': return "EASY"
            case '2': return "MEDIUM"
            case '3': return "HARD"


def display_text(stdscr, target, current, wpm=0, accuracy=100):
    stdscr.addstr(target)

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

    stdscr.addstr(20, 0, f"WPM: {wpm} | Accuracy: {accuracy:.2f}%")

def load_txt(difficulty):
    with open('sample.txt', "r") as f:
        lines = [line.strip() for line in f if line.strip()]

        filtered_lines = [line[len(difficulty) + 2:] for line in lines if line.startswith(f"[{difficulty}]")]

        if not filtered_lines:
            return "Error : No text available for this difficulty."
        return random.choice(filtered_lines)

def wpm_test(stdscr, difficulty):
    target_text = load_txt(difficulty)
    current_text = []
    wpm = 0
    total_chars_typed = 0
    start_time = time.time()
    stdscr.nodelay(True)
    curses.curs_set(0)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        correct_chars = sum(1 for i, char in enumerate(current_text) if i < len(target_text) and char == target_text[i])
        total_chars_typed = len(current_text)

        accuarcy = (correct_chars / total_chars_typed) * 100

        stdscr.erase()
        display_text(stdscr, target_text, current_text, wpm, accuracy)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except Exception:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                total_chars_typed += 1
                current_text.pop()
        elif len(current_text) < len(target_text):
            total_chars_typed += 1
            if key == target_text[len(current_text)]:
                correct_chars += 1
            current_text.append(key)

        time.sleep(0.1)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        difficulty = start_screen(stdscr)
        wpm_test(stdscr, difficulty)
        stdscr.addstr(2, 0, "Press ESC to exit or any key to retry")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)
