# Minesweeper AI

An AI-powered Minesweeper game built using Python and Tkinter. The game simulates human-like logic to clear the board automatically.

<img src="https://i.imgur.com/8JwCyAQ.png" alt="Screenshot on OSX" height="350"/>

## 🔍 Features

-   Classic Minesweeper gameplay
-   AI that simulates human logic and decision-making
-   Built using Python and Tkinter
-   Automatically clicks and flags tiles
-   Customizable game loop speed

## 📂 Project Structure

```
/images/         - Game tile assets
/minesweeper.py  - Main GUI and game logic
/ai.py           - AI logic and gameplay automation
```

## 🚀 Getting Started

1. **Clone the repo:**

    ```bash
    git clone https://github.com/alibadawi25/Mine-Sweeper-Ai.git
    cd Mine-Sweeper-Ai
    ```

2. **Run the game:**
    ```bash
    python minesweeper.py
    ```

## 🧠 AI Logic

The AI plays by:

-   Checking the number of flagged and unclicked tiles around known numbers.
-   Clicking tiles if it's sure they are safe.
-   Flagging tiles if it's sure they are bombs.
-   Guessing randomly only if no safe move is available.

## 🙏 Based On

This project is based on [ripexz/python-tkinter-minesweeper](https://github.com/ripexz/python-tkinter-minesweeper), with substantial modifications including the addition of AI and automation logic.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
