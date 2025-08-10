
from minesweeper import Minesweeper
        
COLS = 5
ROWS = 4
BOMBS = 3
m = Minesweeper(COLS, ROWS, BOMBS)

m.print_board()
user = input("Enter move code: ")
r, c = m.square_to_index(user)
m.first_move(r, c)

game_outcome = True

while m.bomb_board != m.fog_board:
    m.print_board()
    user = input("Enter move code: ")
    r, c = m.square_to_index(user)

    if m.move(r, c):
        game_outcome = False
        break

if game_outcome:
    print("VICTORY")
    m.print_board()
else:
    print("LOSS")
    m.print_solution()
