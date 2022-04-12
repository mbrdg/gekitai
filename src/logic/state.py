from __future__ import annotations

Player = bool
Position = tuple[int, int]


class State:
    """
    State class that represents the state of the game.
    """

    def __init__(self, board_size: int = 6):
        self.board_size = board_size
        self.board: list[list[Player | None]] = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.player: Player = False
        self.markers: tuple[int, int] = (8, 8)


def actions(state: State) -> list[Position]:
    return [(i, j) for i, ln in enumerate(state.board) for j, elem in enumerate(ln) if elem is None]


# These masks represent the offsets in each direction of the board
# They allow to generalize the searching code for both winning moves or pushing pieces for all the 8 possible directions
#
# Example: (-1, 0, -2, 0) means that for a given board[i][j], their neighbours which will be visited are:
#
#           - board[i+(-1)][j+0] -> the position in the line above;
#           - board[i+(-2)][j+0] -> the position in the same column but 2 lines above;
_masks = {(-1, 0, -2, 0), (-1, 1, -2, 2), (0, 1, 0, 2), (1, 1, 2, 2),
          (1, 0, 2, 0), (1, -1, 2, -2), (0, -1, 0, -2), (-1, -1, -2, -2)}


def is_over(state: State) -> bool:
    """
    Determines whether the game is over
    :param state: Current state of the game
    :return: True if the game is over, False otherwise
    """
    print(state.markers)
    if not state.markers[not state.player]:
        print(f'No more markers for player {int(not state.player) + 1}')
        return True

    s = state.board_size
    markers = [(i, j) for i in range(s) for j in range(s) if state.board[i][j] is (not state.player)]

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
    s = state.board_size
    i, j = position
    i0, j0, i1, j1 = mask

    try:
        if not (0 <= i+i0 < s and 0 <= j+j0 < s and 0 <= i+i1 < s and 0 <= j+j1 < s):
            raise IndexError
        return state.board[i][j] == state.board[i + i0][j + j0] == state.board[i + i1][j + j1]
    except IndexError:
        return False


def move(state: State, position: Position) -> State:
    """
    Executes a move given a position - note that the state knows who is the current player
    :param state: Current state of the game
    :param position: Position where the current player wants to place its marker
    :return: The new state of the game with the corresponding post-conditions applied
    """
    i, j = position

    if state.board[i][j] is not None:
        return state

    state.board[i][j] = state.player
    m, n = state.markers
    state.markers = (m, n-1) if state.player else (m-1, n)
    state.player = not state.player

    return _push_pieces(state, position)


def _push_pieces(state, position):
    for mask in _masks:
        state = _push_piece(state, position, mask)
    return state


def _push_piece(state, position, mask):
    s = state.board_size
    i, j = position
    i0, j0, i1, j1 = mask

    if not 0 <= i+i0 < s or not 0 <= j+j0 < s:
        return state
    if not 0 <= i+i1 < s or not 0 <= j+j1 < s:
        if state.board[i+i0][j+j0] is not None:
            m, n = state.markers
            state.markers = (m, n+1) if state.board[i+i0][j+j0] else (m+1, n)
        state.board[i+i0][j+j0] = None
        return state

    if state.board[i+i1][j+j1] is not None:
        return state

    state.board[i+i0][j+j0], state.board[i+i1][j+j1] = None, state.board[i+i0][j+j0]
    return state
