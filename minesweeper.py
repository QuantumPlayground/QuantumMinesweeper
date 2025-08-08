
import random
import copy

class Minesweeper:
    def __init__(self, cols, rows, bombs):
        self.cols = cols
        self.rows = rows
        self.bombs = bombs

        self.bomb_board = None
        self.number_board = None
        self.base_board = None
        self.fog_board = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        self.board = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

    
    def index_to_square(self, r=-1, c=-1):
        return chr(ord('A') + c) + str(r+1)

    def square_to_index(self, code='A1'):
        col = ord(code[0]) - ord('A')
        row_from_bottom = int(code[1]) - 1
        row_from_top = (self.rows - 1) - row_from_bottom
        return row_from_top, col 

    def first_move(self, r1, c1):
        self.bomb_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for _ in range(self.bombs):
            r, c = random.randrange(self.rows), random.randrange(self.cols)
            while self.bomb_board[r][c] == 1 or abs(r - r1) <= 1 and abs(c - c1) <= 1:
                r, c = random.randrange(self.rows), random.randrange(self.cols)
            self.bomb_board[r][c] = 1

        def count_neighbouring_bombs(r, c):
            count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if r + i < 0 or r + i >= self.rows or c + j < 0 or c + j >= self.cols:
                        continue
                    if self.bomb_board[r + i][c + j] == 1:
                        count += 1
            return count

        self.number_board = [[count_neighbouring_bombs(r, c) for c in range(self.cols)] for r in range(self.rows)]

        self.base_board = copy.deepcopy(self.number_board)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.bomb_board[r][c] == 1:
                    self.base_board[r][c] = '*'

        self.move(r1, c1)

    def move(self, r, c):

        if self.fog_board[r][c] == 1:
            self.fog_board[r][c] = 0

            if self.number_board[r][c] == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        if r + i < 0 or r + i >= self.rows or c + j < 0 or c + j >= self.cols:
                            continue

                        if self.fog_board[r + i][c + j] == 1:
                            self.move(r + i, c + j)

        return self.bomb_board[r][c] == 1

    def print_board(self):

        for r in range(self.rows):
            for c in range(self.cols):
                if self.fog_board[r][c] == 1:
                    self.board[r][c] = '?'
                else:
                    self.board[r][c] = self.base_board[r][c]

        print()
        print('   ┌' + '─'*(2*self.cols + 1) + '┐')
        for i in range(self.rows):
            print(str(self.rows - i).rjust(2) + ' │ ' + ' '.join(str(x) if x != 0 else ' ' for x in self.board[i]) + ' │')
        print('   └' + '─'*(2*self.cols + 1) + '┘')
        print('     ' + ' '.join(self.index_to_square(c=j)[0] for j in range(self.cols)))
        print()

    def print_solution(self):
        print()
        print('   ┌' + '─'*(2*self.cols + 1) + '┐')
        for i in range(self.rows):
            print(str(self.rows - i).rjust(2) + ' │ ' + ' '.join(str(x) if x != 0 else ' ' for x in self.base_board[i]) + ' │')
        print('   └' + '─'*(2*self.cols + 1) + '┘')
        print('     ' + ' '.join(self.index_to_square(c=j)[0] for j in range(self.cols)))
        print()
