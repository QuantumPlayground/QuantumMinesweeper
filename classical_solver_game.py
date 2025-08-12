
from minesweeper import Minesweeper
from solver import ClassicalSolver

COLS = 5
ROWS = 5
BOMBS = ROWS * COLS // 4
game = Minesweeper(COLS, ROWS, BOMBS)


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

def make_uncertain_move(show_move=False):
    square_dists = [[0, 0, 0] for _ in range(ROWS * COLS)]
    min_mines = COLS*ROWS

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

            if min_mines > square_dists[r * COLS + c][0] and square_dists[r * COLS + c][0] != 0:
                min_mines = square_dists[r * COLS + c][0]

    min_mines_square_dists = [(i, square_dists[i][2]/square_dists[i][1]) for i in range(len(square_dists)) if square_dists[i][0] == min_mines]
    best_uncertain_move = min(min_mines_square_dists, key=lambda x: x[1])[0]
    r, c = best_uncertain_move // COLS, best_uncertain_move % COLS

    if show_move:
        print("Choosing best move:", game.index_to_square(r, c), '(' + str(r) + ',' + str(c) + ')')
    return game.move(r, c)


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



solver = ClassicalSolver(COLS, ROWS, BOMBS)

print("GAME START!")
print("All possible configurations:", solver.initial_configs)

solver.generate_boards()
game.print_board()


print("FIRST MOVE")
# user = input("Enter move code: ")
# r, c = game.square_to_index(user)
r, c = ROWS // 2, COLS // 2
# r, c = ROWS -1 , COLS - 1


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
        if make_uncertain_move(show_move=True):
            print()
            print("@ FAILURE: MINE FOUND")
            game.print_solution()
            break
        else:
            game.print_board()

    solver.compare_to_evidence(game.fog_board, game.board)
    print("Solutions after:", len(solver.solutions))
    print()
