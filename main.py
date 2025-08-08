
from minesweeper import Minesweeper
from quantum_minesweeper import QuantumMinesweeperSolver

# ----------------------------
# Example usage (when run directly)
# ----------------------------
if __name__ == "__main__":
    # Example: 8x8 with 20% mines
    g = Minesweeper(height=8, width=8, mine_ratio=0.2)
    solver = QuantumMinesweeperSolver(g, shots=4096)
    result = solver.solve(verbose=True)
    print("Result:", "Win" if result else "Loss")

