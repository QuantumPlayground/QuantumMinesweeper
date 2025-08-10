
from minesweeper import Minesweeper
from solver import ClassicalSolver

COLS = 5
ROWS = 4
BOMBS = 4
game = Minesweeper(COLS, ROWS, BOMBS)

solver = ClassicalSolver(COLS, ROWS, BOMBS)
solver.generate_boards()



def make_certain_moves():
    number_of_moves = 0

    for r in range(ROWS):
        for c in range(COLS):
            mine_possible = False
            for board in solver.solutions:
                if board[r][c] == '*':
                    mine_possible = True
                    break
            if not mine_possible and game.fog_board[r][c] == 1:
                game.move(r, c)
                number_of_moves += 1
                
    return number_of_moves

def make_uncertain_move():
    square_dists = [[0, 0, 0] for _ in range(ROWS * COLS)]
    number_of_moves = 0

    for r in range(ROWS):
        for c in range(COLS):
            for board in solver.solutions:
                match board[r][c]:
                    case '*':
                        square_dists[r * COLS + c][0] += 1
                    case 0:
                        square_dists[r * COLS + c][2] += 1
                    case _:
                        square_dists[r * COLS + c][1] += 1
                
            # print("Cell:", r * COLS + c, "- Dist:", square_dists[r * COLS + c])
            if square_dists[r * COLS + c][0] == 0 and game.fog_board[r][c] == 1:
                game.move(r, c)
                number_of_moves += 1

def check_victory():

    if solver.finished():
        print("SOLUTION FOUND!")
        solution = solver.solutions[0]
        for r in range(ROWS):
            for c in range(COLS):
                if solution[r][c] != '*':
                    game.move(r, c)

        game.print_board()
        print('VICTORY!')
    return solver.finished()



print("GAME START!")
print("All possible configurations:", len(solver.solutions))

game.print_board()
# r, c = ROWS // 2, COLS // 2
r, c = ROWS -1 , COLS - 1

print("FIRST MOVE")
game.first_move(r, c)
game.print_board()
solver.compare_to_evidence(game.fog_board, game.board)
print("Possible solutions:", len(solver.solutions))
print()

print("### BEGINNING ALGORITHM ###")
while not check_victory():
    print("CERTAIN MOVES")
    print("Solutions before:", len(solver.solutions))
    n_moves = make_certain_moves()
    print("Number of Certain Moves:", n_moves)
    game.print_board()

    if n_moves == 0:
        print("NO CERTAIN MOVES LEFT!!!")
        break

    solver.compare_to_evidence(game.fog_board, game.board)
    print("Solutions after:", len(solver.solutions))
    print()
