import tkinter as tk
from minesweeper import Minesweeper  # Your minesweeper code file
import random
import time

def main():
    root = tk.Tk()
    game = Minesweeper(root)
    # root.after(1000, lambda: play_randomly(game))
    root.after(1000, lambda: play_level_1(game, root))
    root.mainloop()


def print_board(game):
    board = game.get_board_state()
    for row in board:
        print(" ".join(str(cell) for cell in row))

def play_randomly(game):
    state = game.get_game_state()
    while state == "playing":
        tilex = random.randint(0, 9)
        tiley = random.randint(0, 9)
        game.click_tile(tilex, tiley)
        state = game.get_game_state()
        print(f"Clicked ({tilex},{tiley}), game state: {state}")

def play_level_1(game, root):
    state = game.get_game_state()    
    print(f"Game state: {state}")
    if state != "playing":
        print(f"Game ended: {state}")
        return

    board = game.get_board_state()
    SIZE_X = len(board)
    SIZE_Y = len(board[0]) if SIZE_X > 0 else 0

    found_move = False
    for x in range(SIZE_X):
        for y in range(SIZE_Y):
            cell = board[x][y]
            if isinstance(cell, int):  # only numbers

                bombs, bombs_pos = check_no_of_bombs_around(x, y, board)  # flagged tiles count as bombs
                no_of_unclicked_around, unclicked_positions = get_no_of_unclicked_around(x, y, board)  # unopened & unflagged

                # If number equals flagged bombs, safe to click unopened neighbors
                if cell == bombs and not found_move:
                    safe_tiles = check_safe_unchecked_tiles_around(x, y, board, bombs_pos)
                    for tile in safe_tiles:
                        tilex, tiley = tile
                        print(f"Clicking safe tile ({tilex},{tiley})")
                        game.click_tile(tilex, tiley)
                        found_move = True
                        break
                # If number equals unopened neighbors count, flag all those unopened neighbors
                elif cell == no_of_unclicked_around and not found_move:
                    for position in unclicked_positions:
                        tilex, tiley = position
                        print(f"Flagging tile ({tilex},{tiley})")
                        game.flag_tile(tilex, tiley)
                        found_move = True
                    break
            if found_move:
                break
        if found_move:
            break
    if not found_move:
        tilex = random.randint(0, 9)
        tiley = random.randint(0, 9)
        game.click_tile(tilex, tiley)

                

    root.after(1000, lambda: play_level_1(game, root))


def get_no_of_unclicked_around(x, y, board):
    SIZE_X = len(board)
    SIZE_Y = len(board[0]) if SIZE_X > 0 else 0
    count = 0
    unopened_positions = []

    if x > 0 and y > 0 and (board[x-1][y-1] == "unopened" or board[x-1][y-1] == "flagged"):
        count += 1
        unopened_positions.append([x-1, y-1])
    if y > 0 and (board[x][y-1] == "unopened" or board[x][y-1] == "flagged"):
        count += 1
        unopened_positions.append([x, y-1])
    if x > 0 and (board[x-1][y] == "unopened" or board[x-1][y] == "flagged"):
        count += 1
        unopened_positions.append([x-1, y])
    if x < SIZE_X - 1 and y < SIZE_Y - 1 and (board[x+1][y+1] == "unopened" or board[x+1][y+1] == "flagged"):
        count += 1
        unopened_positions.append([x+1, y+1])
    if y < SIZE_Y - 1 and (board[x][y+1] == "unopened" or board[x][y+1] == "flagged"):
        count += 1
        unopened_positions.append([x, y+1])
    if x < SIZE_X - 1 and (board[x+1][y] == "unopened" or board[x+1][y] == "flagged"):
        count += 1
        unopened_positions.append([x+1, y])
    if x < SIZE_X - 1 and y > 0 and (board[x+1][y-1] == "unopened" or board[x+1][y-1] == "flagged"):
        count += 1
        unopened_positions.append([x+1, y-1])
    if x > 0 and y < SIZE_Y - 1 and (board[x-1][y+1] == "unopened" or board[x-1][y+1] == "flagged"):
        count += 1
        unopened_positions.append([x-1, y+1])

    return count, unopened_positions



def check_no_of_bombs_around(x, y, board):
    bombs = 0
    bombs_pos = []
    SIZE_X = len(board)
    SIZE_Y = len(board[0]) if SIZE_X > 0 else 0

    if x > 0 and y > 0 and board[x-1][y-1] == "flagged":
        bombs += 1
        bombs_pos.append([x-1, y-1])
    if y > 0 and board[x][y-1] == "flagged":
        bombs += 1
        bombs_pos.append([x, y-1])
    if x > 0 and board[x-1][y] == "flagged":
        bombs += 1
        bombs_pos.append([x-1, y])
    if x < SIZE_X - 1 and y < SIZE_Y - 1 and board[x+1][y+1] == "flagged":
        bombs += 1
        bombs_pos.append([x+1, y+1])
    if y < SIZE_Y - 1 and board[x][y+1] == "flagged":
        bombs += 1
        bombs_pos.append([x, y+1])
    if x < SIZE_X - 1 and board[x+1][y] == "flagged":
        bombs += 1
        bombs_pos.append([x+1, y])
    if x < SIZE_X - 1 and y > 0 and board[x+1][y-1] == "flagged":
        bombs += 1
        bombs_pos.append([x+1, y-1])
    if x > 0 and y < SIZE_Y - 1 and board[x-1][y+1] == "flagged":
        bombs += 1
        bombs_pos.append([x-1, y+1])

    return bombs, bombs_pos

def check_safe_unchecked_tiles_around(x, y, board, unsafe_tiles):
    SIZE_X = len(board)
    SIZE_Y = len(board[0]) if SIZE_X > 0 else 0
    safe_tiles = []

    if x > 0 and y > 0 and board[x-1][y-1] == "unopened" and [x-1, y-1] not in unsafe_tiles:
        safe_tiles.append([x-1, y-1])
    if y > 0 and board[x][y-1] == "unopened" and [x, y-1] not in unsafe_tiles:
        safe_tiles.append([x, y-1])
    if x > 0 and board[x-1][y] == "unopened" and [x-1, y] not in unsafe_tiles:
        safe_tiles.append([x-1, y])
    if x < SIZE_X - 1 and y < SIZE_Y - 1 and board[x+1][y+1] == "unopened" and [x+1, y+1] not in unsafe_tiles:
        safe_tiles.append([x+1, y+1])
    if y < SIZE_Y - 1 and board[x][y+1] == "unopened" and [x, y+1] not in unsafe_tiles:
        safe_tiles.append([x, y+1])
    if x < SIZE_X - 1 and board[x+1][y] == "unopened" and [x+1, y] not in unsafe_tiles:
        safe_tiles.append([x+1, y])
    if x < SIZE_X - 1 and y > 0 and board[x+1][y-1] == "unopened" and [x+1, y-1] not in unsafe_tiles:
        safe_tiles.append([x+1, y-1])
    if x > 0 and y < SIZE_Y - 1 and board[x-1][y+1] == "unopened" and [x-1, y+1] not in unsafe_tiles:
        safe_tiles.append([x-1, y+1])

    return safe_tiles

if __name__ == "__main__":
    main()
