
import copy
from itertools import combinations
import math

class ClassicalSolver:
    def __init__(self, cols, rows, bombs):
        self.cols = cols
        self.rows = rows
        self.bombs = bombs

        self.arrangements = []
        self.solutions = []

        self.number_of_solutions = self.num_combinations(self.rows, self.cols, self.bombs)

    def num_combinations(self, rows, cols, bombs):
        return math.comb(rows*cols, bombs)

    def generate_boards(self):
        total = self.cols * self.rows
        self.arrangements = list(combinations(range(total), self.bombs))

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
            bomb_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            for dim in arr:
                bomb_board[dim//self.cols][dim%self.cols] = 1

            number_board = [[count_neighbouring_bombs(bomb_board, r, c) for c in range(self.cols)] for r in range(self.rows)]

            base_board = copy.deepcopy(number_board)
            for r in range(self.rows):
                for c in range(self.cols):
                    if bomb_board[r][c] == 1:
                        base_board[r][c] = '*'

            board = tuple(map(tuple, base_board))
            self.solutions.append(board)

    def compare_to_evidence(self, fog_board, board):
        def add_fog(fog_board, base_board):
            def check_fog(r, c):
                if fog_board[r][c] == 1:
                    return '?'
                else: 
                    return base_board[r][c]
                
            board = [[check_fog(r, c) for c in range(self.cols)] for r in range(self.rows)]
            return board

        for i in range(len(self.solutions)-1, -1, -1):
            if add_fog(fog_board, self.solutions[i]) != board:
                self.solutions.pop(i)

        self.number_of_solutions = len(self.solutions)

    def finished(self):
        return len(self.solutions) == 1
    