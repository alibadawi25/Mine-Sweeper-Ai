from tkinter import *
import tkinter.messagebox as tkMessageBox
from tkinter import simpledialog
from collections import deque
import random
import platform
from datetime import datetime

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

window = None
SIZE_X = 10  # Default values, will be overwritten
SIZE_Y = 10

class Minesweeper:
    def __init__(self, tk):
        global SIZE_X, SIZE_Y

        self.game_state = "playing"  # "playing", "won", "lost"


        # import images
        self.images = {
            "plain": PhotoImage(file="images/tile_plain.gif"),
            "clicked": PhotoImage(file="images/tile_clicked.gif"),
            "mine": PhotoImage(file="images/tile_mine.gif"),
            "flag": PhotoImage(file="images/tile_flag.gif"),
            "wrong": PhotoImage(file="images/tile_wrong.gif"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(PhotoImage(file=f"images/tile_{i}.gif"))

        self.tk = tk
        self.frame = Frame(self.tk)
        self.frame.pack()

        # set up labels/UI
        self.labels = {
            "time": Label(self.frame, text="00:00:00"),
            "mines": Label(self.frame, text="Mines: 0"),
            "flags": Label(self.frame, text="Flags: 0")
        }

        
        colspan_time = max(SIZE_Y, 7)  # minimum 5 columns span for timer label
        colspan_half = max(int(SIZE_Y / 2), 2)  # minimum 2 for mines and flags

        self.labels["time"].grid(row=0, column=0, columnspan=colspan_time)
        self.labels["mines"].grid(row=SIZE_X + 1, column=0, columnspan=colspan_half)
        self.labels["flags"].grid(row=SIZE_X + 1, column=colspan_half, columnspan=colspan_half)


        self.restart()
        self.updateTimer()

    def setup(self):
        global SIZE_X, SIZE_Y
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None

        self.tiles = dict({})
        self.mines = 0

        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                if y == 0:
                    self.tiles[x] = {}

                id = f"{x}_{y}"
                isMine = random.uniform(0.0, 1.0) < 0.1
                if isMine:
                    self.mines += 1

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {"x": x, "y": y},
                    "button": Button(self.frame, image=self.images["plain"]),
                    "mines": 0
                }

                tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y))
                tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y))
                tile["button"].grid(row=x+1, column=y)
                self.tiles[x][y] = tile

        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                mc = sum(1 for n in self.getNeighbors(x, y) if n["isMine"])
                self.tiles[x][y]["mines"] = mc

    def restart(self):
        self.setup()
        self.game_state = "playing"
        self.refreshLabels()

    def refreshLabels(self):
        self.labels["flags"].config(text=f"Flags: {self.flagCount}")
        self.labels["mines"].config(text=f"Mines: {self.mines}")

    def gameOver(self, won):
        global SIZE_X, SIZE_Y
        self.game_state = "won" if won else "lost"

        for x in range(SIZE_X):
            for y in range(SIZE_Y):
                tile = self.tiles[x][y]
                if not tile["isMine"] and tile["state"] == STATE_FLAGGED:
                    tile["button"].config(image=self.images["wrong"])
                if tile["isMine"] and tile["state"] != STATE_FLAGGED:
                    tile["button"].config(image=self.images["mine"])
        self.game_state = "won" if won else "lost"

        self.tk.update()
        msg = "You Win! Play again?" if won else "You Lose! Play again?"
        if tkMessageBox.askyesno("Game Over", msg):
            self.restart()
        else:
            self.tk.quit()

    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0]
            if delta.total_seconds() < 36000:
                ts = "0" + ts
        self.labels["time"].config(text=ts)
        self.frame.after(100, self.updateTimer)

    def getNeighbors(self, x, y):
        coords = [
            {"x": x-1, "y": y-1}, {"x": x-1, "y": y}, {"x": x-1, "y": y+1},
            {"x": x, "y": y-1}, {"x": x, "y": y+1},
            {"x": x+1, "y": y-1}, {"x": x+1, "y": y}, {"x": x+1, "y": y+1},
        ]
        neighbors = []
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    def onClickWrapper(self, x, y):
        return lambda event: self.onClick(self.tiles[x][y])

    def onRightClickWrapper(self, x, y):
        return lambda event: self.onRightClick(self.tiles[x][y])

    def onClick(self, tile):
        if self.startTime is None:
            self.startTime = datetime.now()

        if tile["isMine"]:
            self.gameOver(False)
            return

        if tile["mines"] == 0:
            tile["button"].config(image=self.images["clicked"])
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image=self.images["numbers"][tile["mines"]-1])

        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1

        if self.clickedCount == (SIZE_X * SIZE_Y) - self.mines:
            self.gameOver(True)

    def onRightClick(self, tile):
        if self.startTime is None:
            self.startTime = datetime.now()

        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image=self.images["flag"])
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            if tile["isMine"]:
                self.correctFlagCount += 1
            self.flagCount += 1
            self.refreshLabels()
        elif tile["state"] == STATE_FLAGGED:
            tile["button"].config(image=self.images["plain"])
            tile["state"] = STATE_DEFAULT
            tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            if tile["isMine"]:
                self.correctFlagCount -= 1
            self.flagCount -= 1
            self.refreshLabels()

    def clearSurroundingTiles(self, id):
        queue = deque([id])
        while queue:
            x, y = map(int, queue.popleft().split("_"))
            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image=self.images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image=self.images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1


    def get_board_state(self):
        board = []
        for x in range(SIZE_X):
            row = []
            for y in range(SIZE_Y):
                tile = self.tiles[x][y]
                state = tile["state"]
                if state == STATE_DEFAULT:  # unopened
                    val = "unopened"
                elif state == STATE_FLAGGED:
                    val = "flagged"
                elif state == STATE_CLICKED:
                    if tile["isMine"]:
                        val = "mine"
                    else:
                        val = tile["mines"] if tile["mines"] > 0 else "empty"
                else:
                    val = "unknown"  # fallback
                row.append(val)
            board.append(row)
        return board

    def get_game_state(self):
        return self.game_state

    def click_tile(self, x, y):
        print(f"Clicking tile ({x},{y})")
        tile = self.tiles[x][y]

        if tile["state"] == STATE_CLICKED or tile["state"] == STATE_FLAGGED:
            print("Tile already revealed or flagged")
            return

        if tile["isMine"]:
            self.gameOver(False)
            return
        self.onClick(tile)
        
    def flag_tile(self, x, y):
        print(f"Flagging tile ({x},{y})")
        tile = self.tiles[x][y]

        if tile["state"] == STATE_CLICKED:
            print("Tile already revealed, cannot flag")
            return
        if tile["state"] == STATE_FLAGGED:
            print("Tile already flagged")
            return

        self.onRightClick(tile)




### MAIN ENTRY POINT ###

def main():
    global SIZE_X, SIZE_Y

    # Initial hidden window to ask user input
    input_root = Tk()
    input_root.withdraw()

    SIZE_X = simpledialog.askinteger("Grid Height", "Enter number of rows (e.g. 10–30):", minvalue=5, maxvalue=50)
    SIZE_Y = simpledialog.askinteger("Grid Width", "Enter number of columns (e.g. 10–30):", minvalue=5, maxvalue=50)

    if SIZE_X is None or SIZE_Y is None:
        print("Game cancelled.")
        return

    input_root.destroy()

    window = Tk()
    window.title("Minesweeper")
    minesweeper = Minesweeper(window)
    window.mainloop()

if __name__ == "__main__":
    main()
