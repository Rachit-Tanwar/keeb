# keeb

**keeb** is a terminal-based typing speed test built in Python using `curses`, with features like real-time WPM and accuracy tracking, retry logic, and persistent history logging.

---

## ✨ Features

- Clean CLI interface using `curses`
- Tracks WPM, accuracy, typed characters, words, and mistakes
- Custom word list support via `word_list.txt`
- Timed mode with selectable durations (15, 30, or 60 seconds)
- Retry prompt and history viewer (tabulated via `tabulate`)
- History stored in `keeb_history.csv`

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Rachit-Tanwar/keeb.git
cd keeb
```

Install dependencies using [`uv`](https://github.com/astral-sh/uv):

```bash
uv pip install -r requirements.txt
```

> ⚠️**Note on `curses`:**
>
> * `curses` is included with Python on **Linux/macOS** — **no need to install manually**
> * On **Windows**, install `windows-curses` instead:

```bash
# Windows only
uv pip install windows-curses
```

---

## 🧪 Usage

Run the typing test:

```bash
python main.py
```

Follow the on-screen instructions:

* Choose a time limit
* Start typing the 50 randomly selected words from `word_list.txt`
* Press `h` after the test to view your history, or `y/n` to retry or exit

---

## 🛠 Custom Word List

Edit the `word_list.txt` file to change the vocabulary used for the test.
Make sure the words are **comma-separated**, like:

```
keyboard,terminal,python,project,development,speed,test,...
```

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
