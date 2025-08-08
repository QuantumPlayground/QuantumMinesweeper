
from typing import Optional, Tuple, List, Dict
import random
import string

# ----------------------------
# Minesweeper class (from before)
# ----------------------------
class Minesweeper:
    def __init__(self, height=8, width=8, mine_ratio=0.2):
        self.HEIGHT = height
        self.WIDTH = width
        self.MINE_RATIO = mine_ratio
        self.total_cells = self.HEIGHT * self.WIDTH
        self.num_mines = int(self.total_cells * self.MINE_RATIO)

        self.visible = [[None for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.board = None
        self.first_move = True

    def generate_board(self, first_r: int, first_c: int):
        """Generate a board where the first move is guaranteed to be an empty cell (0 adjacent mines)."""
        while True:
            # Start with empty board
            board = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

            # Place mines randomly, excluding the first cell
            excluded = {(first_r, first_c)}
            all_positions = [i for i in range(self.total_cells) if (i // self.WIDTH, i % self.WIDTH) not in excluded]
            mine_positions = random.sample(all_positions, self.num_mines)
            for pos in mine_positions:
                r = pos // self.WIDTH
                c = pos % self.WIDTH
                board[r][c] = -1  # -1 is a mine

            # Fill numbers
            for r in range(self.HEIGHT):
                for c in range(self.WIDTH):
                    if board[r][c] == -1:
                        continue
                    mines_count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.HEIGHT and 0 <= nc < self.WIDTH and board[nr][nc] == -1:
                                mines_count += 1
                    board[r][c] = mines_count

            # Check if the first cell is empty (0 adjacent mines)
            if board[first_r][first_c] == 0:
                return board

    def display_board(self):
        letters = string.ascii_uppercase[:self.WIDTH]
        print("   " + " ".join(letters))
        for r in range(self.HEIGHT):
            row_str = f"{r+1:2} "
            for c in range(self.WIDTH):
                if self.visible[r][c] is None:
                    row_str += ". "
                else:
                    row_str += f"{self.visible[r][c]} "
            print(row_str)

    def reveal(self, r: int, c: int):
        if self.visible[r][c] is not None:
            return
        if self.board[r][c] == -1:
            self.visible[r][c] = "*"
            return

        self.visible[r][c] = str(self.board[r][c])
        if self.board[r][c] == 0:
            self.visible[r][c] = " "
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.HEIGHT and 0 <= nc < self.WIDTH:
                        self.reveal(nr, nc)

    def coords_from_input(self, user_input: str) -> Optional[Tuple[int, int]]:
        user_input = user_input.strip().upper()
        if len(user_input) < 2:
            return None
        col_letter = user_input[0]
        if col_letter not in string.ascii_uppercase[:self.WIDTH]:
            return None
        try:
            row_number = int(user_input[1:])
        except ValueError:
            return None
        if not (1 <= row_number <= self.HEIGHT):
            return None
        r = row_number - 1
        c = string.ascii_uppercase.index(col_letter)
        return r, c

    def is_won(self) -> bool:
        unrevealed = sum(1 for rr in range(self.HEIGHT) for cc in range(self.WIDTH) if self.visible[rr][cc] is None)
        return unrevealed == self.num_mines