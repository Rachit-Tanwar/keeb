import curses
from curses import wrapper
from tabulate import tabulate
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.nodelay(False)
    curses.flushinp()

    stdscr.addstr(0, 0, "Welcome to typing speed test!")
    stdscr.addstr(1, 0, "Select Difficulty : ")
    stdscr.addstr(2, 0, "1. Easy")
    stdscr.addstr(3, 0, "2. Medium")
    stdscr.addstr(4, 0, "3. Hard") 
    stdscr.refresh()
    
    difficulty = None
    while True:
        try:
            key = stdscr.getkey()
            match key:
                case '1':
                    difficulty = "EASY"
                    break
                case '2':
                    difficulty = "MEDIUM"
                    break
                case '3':
                    difficulty = "HARD"
                    break
                case _ : continue
        except Exception:
            continue

    time_imit:int = 30
    stdscr.clear()
    stdscr.addstr(0, 0, "Select Time Limit (press enter for default 30s) : ")
    stdscr.addstr(1, 0, "1. 15s")
    stdscr.addstr(2, 0, "2. 30s")
    stdscr.addstr(3, 0, "3. 60s") 
    stdscr.refresh()
    
    while True:
        try:
            key = stdscr.getkey()
            match key:
                case '1':
                    time_limit = 15
                    break
                case '2':
                    time_limit = 30
                    break
                case '3':
                    time_limit = 60
                    break
                case _ : continue

        except Exception:
            time_limit = 30

    return difficulty, time_limit


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

def wpm_test(stdscr, difficulty, time_limit:int=30):
    target_text = load_txt(difficulty)
    current_text = []
    wpm = 0
    total_chars_typed = 0
    start_time = time.time()
    stdscr.nodelay(True)
    curses.curs_set(0)

    while True:
        time_elapsed = max(time.time() - start_time, 1)

        if time_elapsed >= time_limit:
            break

        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
        correct_chars = sum(1 for i, char in enumerate(current_text) if i < len(target_text) and char == target_text[i])
        total_chars_typed = max(len(current_text), 1)

        if total_chars_typed == 0:
            accuracy = 0.0

        else:
            accuracy = (correct_chars / total_chars_typed) * 100

        stdscr.erase()
        display_text(stdscr, target_text, current_text, wpm, accuracy)
        stdscr.addstr(21, 0, f"Time left : {int(time_limit - time_elapsed)}s")
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

    stdscr.nodelay(False)
    stdscr.erase()

    final_time = time.time() - start_time
    wpm = round((len(current_text) / (time_elapsed / 60)) / 5)
    correct_chars = sum(1 for i, char in enumerate(current_text) if i < len(target_text) and char == target_text[i])
    total_chars_typed = max(len(current_text), 1)
    accuracy = ((correct_chars / total_chars_typed) * 100) if total_chars_typed > 0 else 0.0

#If i want to display wpm and accuracy in the curses screen
    '''stdscr.addstr(0, 0, "Time finished!!")
    stdscr.addstr(2, 0, f"Your WPM : {wpm}")
    stdscr.addstr(3, 0, f"Your Accuracy :  {accuracy:.2f}%")
    stdscr.addstr(5, 0, "Press any key to continue ...")
    stdscr.refresh()
    stdscr.getkey()
'''
    return wpm, accuracy


def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    #start_screen(stdscr)
    difficulty, time_limit = start_screen(stdscr)
    wpm, accuracy = wpm_test(stdscr, difficulty, time_limit)

    f_wpm = wpm
    f_accuracy = accuracy

    return f_wpm, f_accuracy

if __name__ == "__main__":
    while True:
        wpm, accuracy = wrapper(main)
    
        result_table = [
            ["WPM", wpm],
            ["Accuracy", f"{accuracy:.2f}%"]
        ]

        print("\nTest results : ")
        print(tabulate(result_table, headers=["Metric", "Value"], tablefmt="grid"))

        r = input("Do you want to retry? [y/n]").strip().lower()
        if r != "y":
            break
