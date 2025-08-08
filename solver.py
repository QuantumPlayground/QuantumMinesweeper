
import copy

class ClassicalSolver:
    def __init__(self, cols, rows, bombs):
        self.cols = cols
        self.rows = rows
        self.bombs = bombs

        self.arrangements = []
        self.boards = []

    def generate_arrangements(self):
        for i in range(self.cols*self.rows-2):
            for j in range(i+1, COLS*ROWS-1):
                for k in range(j+1, COLS*ROWS):
                    self.arrangements.append((i, j, k))

        def count_neighbouring_bombs(bomb_board, r, c):
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if r + i < 0 or r + i >= len(bomb_board) or c + j < 0 or c + j >= len(bomb_board[0]):
                        continue
                    if bomb_board[r + i][c + j] == 1:
                        count += 1
            return count

        for arr in self.arrangements:
            bomb_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            for dim in arr:
                bomb_board[dim//COLS][dim%COLS] = 1

            number_board = [[count_neighbouring_bombs(bomb_board, r, c) for c in range(COLS)] for r in range(ROWS)]

            base_board = copy.deepcopy(number_board)
            for r in range(ROWS):
                for c in range(COLS):
                    if bomb_board[r][c] == 1:
                        base_board[r][c] = '*'

            board = tuple(map(tuple, base_board))
            self.boards.append(board)



COLS = 5
ROWS = 4
BOMBS = 3

c = ClassicalSolver(COLS, ROWS, BOMBS)
c.generate_arrangements()
print(c.boards[1069])
