# quantum_minesweeper.py
import random
import string
from typing import Optional, Tuple, List, Dict

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

from minesweeper import Minesweeper

# ----------------------------
# Quantum Solver
# ----------------------------
class QuantumMinesweeperSolver:
    def __init__(self, game: Minesweeper, shots: int = 4096, simulator: Optional[AerSimulator] = None):
        self.game = game
        self.n = game.total_cells
        self.shots = shots
        self.sim = simulator or AerSimulator()

    @staticmethod
    def _bit_index_to_cell(i: int, width: int) -> Tuple[int, int]:
        return i // width, i % width

    def _build_all_h_circuit(self) -> QuantumCircuit:
        qc = QuantumCircuit(self.n, self.n)
        for q in range(self.n):
            qc.h(q)
        qc.measure(range(self.n), range(self.n))
        return qc

    def _counts_to_marginals_conditioned(self, counts: Dict[str, int]) -> Tuple[List[float], int]:
        """
        Convert Qiskit counts (bitstrings -> counts) into marginal probabilities for each cell,
        after conditioning on the currently revealed visible cells.
        Returns (marginals_list, total_consistent_counts).
        """
        ones_counts = [0] * self.n
        consistent_total = 0

        for bitstr, cnt in counts.items():
            # Qiskit bitstrings are ordered q_{n-1}...q_0, so reverse to get index i -> bitstr_rev[i]
            bitstr_rev = bitstr[::-1]
            # fast check: length should be n (it usually is). If shorter, pad with zeros.
            if len(bitstr_rev) < self.n:
                bitstr_rev = bitstr_rev + "0" * (self.n - len(bitstr_rev))

            # Check consistency with revealed squares
            if not self._sample_consistent_with_visible(bitstr_rev):
                continue

            # If consistent, accumulate counts
            consistent_total += cnt
            for i in range(self.n):
                if bitstr_rev[i] == "1":
                    ones_counts[i] += cnt

        if consistent_total == 0:
            return [0.0] * self.n, 0

        marginals = [ones_counts[i] / consistent_total for i in range(self.n)]
        return marginals, consistent_total

    def _sample_consistent_with_visible(self, bitstr_rev: str) -> bool:
        """
        bitstr_rev is a string length >= n mapping index i -> '0'/'1' for that cell.
        Returns True iff the placement is consistent with all revealed cells in self.game.visible.
        """
        g = self.game
        for i in range(self.n):
            r, c = self._bit_index_to_cell(i, g.WIDTH)
            vis = g.visible[r][c]
            if vis is None:
                continue
            # If a cell was revealed and is not a mine, sample must have 0 at that cell
            if vis == "*":
                # An explicitly revealed mine; consistent only if sample has 1 there (but normally we only see '*' on loss)
                if bitstr_rev[i] != "1":
                    return False
                else:
                    continue
            # vis is ' ' or a number string
            # that means sample must have 0 at that cell
            if bitstr_rev[i] != "0":
                return False
            # Now neighbor count must equal the revealed number
            revealed_number = 0 if vis == " " else int(vis)
            # count neighbors in sample
            neigh_mines = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < g.HEIGHT and 0 <= nc < g.WIDTH:
                        neigh_i = nr * g.WIDTH + nc
                        if bitstr_rev[neigh_i] == "1":
                            neigh_mines += 1
            if neigh_mines != revealed_number:
                return False
        return True

    def _select_highest_prob_cell(self, marginals: List[float], exclude_revealed: bool = True) -> int:
        """Return cell index with highest marginal probability of being a mine among unrevealed cells."""
        g = self.game
        best_prob = -1.0
        best_indices = []
        for i in range(self.n):
            r, c = self._bit_index_to_cell(i, g.WIDTH)
            if exclude_revealed and g.visible[r][c] is not None:
                continue
            prob = marginals[i]
            if prob > best_prob:
                best_prob = prob
                best_indices = [i]
            elif prob == best_prob:
                best_indices.append(i)
        if not best_indices:
            # fallback: choose any unrevealed at random
            unrevealed = [i for i in range(self.n) if g.visible[self._bit_index_to_cell(i, g.WIDTH)[0]][self._bit_index_to_cell(i, g.WIDTH)[1]] is None]
            return random.choice(unrevealed)
        return random.choice(best_indices)

    def solve(self, verbose: bool = True, max_retries_when_empty: int = 3):
        """Run the quantum-sampling solver until win or loss. Prints progress if verbose=True."""
        qc = self._build_all_h_circuit()
        backend = self.sim

        step = 0
        while True:
            step += 1
            # Draw board
            if verbose:
                print("\nStep", step)
                self.game.display_board()

            # Run circuit to get samples
            shots = self.shots
            for attempt in range(max_retries_when_empty + 1):
                job = backend.run(qc, shots=shots)
                res = job.result()
                counts = res.get_counts()
                marginals, consistent_total = self._counts_to_marginals_conditioned(counts)
                if consistent_total > 0:
                    break
                # if no consistent samples, try again with more shots (increase by factor)
                shots *= 2
                if verbose:
                    print(f"No consistent samples found with {shots//2} shots; retrying with {shots} shots...")

            if consistent_total == 0:
                # give up on conditioning: choose random unrevealed cell
                if verbose:
                    print("Failed to find any consistent sample even after retries; selecting random unrevealed cell.")
                unrevealed_indices = [i for i in range(self.n) if self.game.visible[self._bit_index_to_cell(i, self.game.WIDTH)[0]][self._bit_index_to_cell(i, self.game.WIDTH)[1]] is None]
                if not unrevealed_indices:
                    # nothing left
                    if verbose:
                        print("No unrevealed cells left.")
                    break
                chosen_i = random.choice(unrevealed_indices)
            else:
                # choose cell with highest probability of being a bomb (as you requested)
                chosen_i = self._select_highest_prob_cell(marginals)

            r, c = self._bit_index_to_cell(chosen_i, self.game.WIDTH)
            if verbose:
                print(f"Selected cell {string.ascii_uppercase[c]}{r+1} with estimated mine probability {marginals[chosen_i] if consistent_total>0 else 'N/A'}")

            # play move in the game
            if self.game.first_move:
                # generate board with guarantee that the selected cell is empty (0)
                self.game.board = self.game.generate_board(r, c)
                self.game.first_move = False

            if self.game.board[r][c] == -1:
                # reveal all mines and end
                for rr in range(self.game.HEIGHT):
                    for cc in range(self.game.WIDTH):
                        if self.game.board[rr][cc] == -1:
                            self.game.visible[rr][cc] = "*"
                if verbose:
                    self.game.display_board()
                    print("Solver hit a mine. Game over.")
                return False  # lost

            # otherwise reveal and continue
            self.game.reveal(r, c)

            # Check win
            if self.game.is_won():
                if verbose:
                    self.game.display_board()
                    print("Solver cleared the minefield! Victory.")
                return True

            # otherwise loop and re-sample conditioned on new info
