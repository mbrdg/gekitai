import numpy as np


class State:
    def __init__(self, board_size: int = 6):
        self.board = np.zeros(shape=(board_size, board_size), dtype='b')
        self._markers = (8, 8)
        self.player = 1

    def get_board_size(self):
        return self.board.shape[0]

    def get_markers(self, i: int):
        return self._markers[i]

    def set_markers(self, i: int, delta: int):
        x, y = self._markers
        self._markers = (x + delta, y) if i else (x, y + delta)

    def swap_player(self):
        self.player = 2 if self.player == 1 else 1

    def actions(self):
        return np.argwhere(self.board == 0)


# These masks represent the offsets in each direction of the board.
# They allow to generalize the searching code for both winning moves
# or pushing pieces for all the 8 possible directions.
#
# Example: (-1, 0, -2, 0) means that for a given board[i][j],
# their neighbours which will be visited are:
#
#   - board[i+(-1), j+0] -> the position in the line above;
#   - board[i+(-2), j+0] -> the position in the same column but 2 lines above;
_masks = {(-1, +0, -2, +0), (-1, +1, -2, +2), (+0, +1, +0, +2), (+1, +1, +2, +2),
          (+1, +0, +2, +0), (+1, -1, +2, -2), (+0, -1, +0, -2), (-1, -1, -2, -2)}


def is_over(state: State) -> bool:
    """
    Determines whether the game is over
    :param state: Current state of the game
    :return: True if the game is over, False otherwise
    """
    if not state.get_markers(i=state.player - 1):
        print(f'No more markers for player {state.player - 1}')
        return True

    markers = np.argwhere(state.board)
    if not markers.size:
        return False

    for position in markers:
        if _position_has_win(state, position):
            return True
    return False


def _position_has_win(state, position):
    for mask in _masks:
        if _position_against_mask(state, position, mask):
            return True
    return False


def _position_against_mask(state, position, mask):
    s = state.get_board_size()
    print(position)
    i, j = position[0], position[1]
    i0, j0, i1, j1 = mask

    try:
        if not (0 <= i+i0 < s and 0 <= j+j0 < s and 0 <= i+i1 < s and 0 <= j+j1 < s):
            raise IndexError
        return state.board[i, j] == state.board[i+i0, j+j0] == state.board[i+i1, j+j1]
    except IndexError:
        return False


def move(state, position):
    """
    Executes a move given a position - note that the state knows who is the current player
    :param state: Current state of the game
    :param position: Position where the current player wants to place its marker
    :return: The new state of the game with the corresponding post-conditions applied
    """
    i, j = position[0], position[1]

    if state.board[i, j]:
        return state

    state.board[i, j] = state.player
    state.set_markers(i=state.player - 1, delta=-1)
    state.swap_player()

    return _push_pieces(state, position)


def _push_pieces(state, position):
    for mask in _masks:
        state = _push_piece(state, position, mask)
    return state


def _push_piece(state, position, mask):
    s = state.get_board_size()
    i, j = position
    i0, j0, i1, j1 = mask

    if not 0 <= i+i0 < s or not 0 <= j+j0 < s:
        return state

    if not 0 <= i+i1 < s or not 0 <= j+j1 < s:
        if state.board[i+i0, j+j0]:
            k = state.board[i+i0, j+j0] - 1
            state.set_markers(i=k, delta=1)
        state.board[i+i0, j+j0] = 0
        return state

    if state.board[i+i1, j+j1]:
        return state

    state.board[i+i0, j+j0], state.board[i+i1, j+j1] = 0, state.board[i+i0, j+j0]
    return state
