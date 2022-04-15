import numpy as np
from scipy.signal import convolve2d

# These masks represent the offsets in each direction of the board.
# They allow to generalize the searching code for both winning moves
# or pushing pieces for all the 8 possible directions.
#
# Example: (-1, 0, -2, 0) means that for a given board[i, j],
# their neighbours which will be visited are:
#
#   - board[i+(-1), j+0] -> the position in the line above;
#   - board[i+(-2), j+0] -> the position in the same column but 2 lines above;
MASKS = {(-1, +0, -2, +0), (-1, +1, -2, +2), (+0, +1, +0, +2), (+1, +1, +2, +2),
         (+1, +0, +2, +0), (+1, -1, +2, -2), (+0, -1, +0, -2), (-1, -1, -2, -2)}


class GameState:
    """ State representation for the 'Gekitai' game """

    def __init__(self, size=6, markers=8):
        self.board = np.zeros(shape=(size, size), dtype=np.uint8)
        self.curr_player, self.prev_player = 1, 2
        self.last_move = None
        self._markers = (markers, markers)

    def size(self):
        return self.board.shape[0]

    def swap_player(self):
        self.prev_player, self.curr_player = self.curr_player, self.prev_player

    def get_markers(self, player: int):
        return self._markers[player - 1]

    def set_markers(self, player: int, delta: int):
        x, y = self._markers
        self._markers = (x + delta, y) if player - 1 else (x, y + delta)

    def actions(self):
        return np.argwhere(self.board == 0)

    def is_over(self, verbose=False):
        if not self.get_markers(self.prev_player):
            if verbose:
                print(f"No more markers left for player {self.prev_player}.")
            return True, self.prev_player

        kernels = [np.ones(shape=(1, 3)), np.ones(shape=(3, 1)), np.eye(3), np.fliplr(np.eye(3))]
        for kernel in kernels:
            if (convolve2d(self.board == self.prev_player, kernel, mode='valid') == 3).any():
                return True, self.prev_player
            if (convolve2d(self.board == self.curr_player, kernel, mode='valid') == 3).any():
                return True, self.curr_player
        return False, None


def move(state, position):
    """
    Executes a move given a position
    ---
    :param state: Current state of the game
    :param position: Position where the current player wants to place its marker
    :return: The new state of the game with the corresponding post-conditions applied
    """
    i, j = position[0], position[1]

    if state.board[i, j]:
        return state

    state.board[i, j] = state.curr_player
    state.set_markers(player=state.curr_player - 1, delta=-1)
    state.swap_player()
    state.last_move = position

    # Pieces pushing
    for mask in MASKS:
        state = _push_piece(state, position, mask)
    return state


def _push_piece(state, position, mask):
    s = state.size()
    i, j = position
    i0, j0, i1, j1 = mask

    # Adjacent cell is outside the board
    if not (0 <= i + i0 < s and 0 <= j + j0 < s):
        return state

    # A markers gets dropped out of the board
    if not (0 <= i + i1 < s and 0 <= j + j1 < s):
        if state.board[i + i0, j + j0]:
            player = state.board[i + i0, j + j0] - 1
            state.set_markers(player=player, delta=1)

        state.board[i + i0, j + j0] = 0
        return state

    # Can't push the piece on the opposite side
    if state.board[i + i1, j + j1]:
        return state

    state.board[i + i0, j + j0], state.board[i + i1, j + j1] = 0, state.board[i + i0, j + j0]
    return state
