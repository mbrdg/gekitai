import numpy as np
from scipy.signal import convolve2d


class GameState:
    """ Game state representation, it holds information about the board, turn and no. of markers """

    def __init__(self, size=6, markers=8):
        self.board = np.zeros(shape=(size, size), dtype=np.uint8)
        self.current_player, self.previous_player = 1, 2
        self.last_move = None
        self._markers = (markers, markers)

    def size(self):
        return self.board.shape[0]

    def swap_player(self):
        self.previous_player, self.current_player = self.current_player, self.previous_player

    def get_markers(self, player: int):
        return self._markers[player - 1]

    def set_markers(self, player: int, delta: int):
        x, y = self._markers
        self._markers = (x + delta, y) if player - 1 else (x, y + delta)

    def actions(self):
        return np.argwhere(self.board == 0)

    def is_over(self, verbose=False):
        # Check if after pushing there are no markers to be placed
        if not self.get_markers(self.previous_player):
            if verbose:
                print(f"No more markers left for player {self.previous_player}.")
            return True, self.previous_player

        # Check if someone has at least 3 markers connected
        kernels = [np.ones(shape=(1, 3)), np.ones(shape=(3, 1)), np.eye(3), np.fliplr(np.eye(3))]
        for kernel in kernels:
            if (convolve2d(self.board == self.previous_player, kernel, mode='valid') == 3).any():
                if verbose:
                    print(f"Player {self.previous_player} has 3 connected markers")
                return True, self.previous_player

            if (convolve2d(self.board == self.current_player, kernel, mode='valid') == 3).any():
                if verbose:
                    print(f"Player {self.previous_player} has 3 connected markers")
                return True, self.current_player

        return False, None
