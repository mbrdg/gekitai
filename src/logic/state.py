from __future__ import annotations

Player = bool
Position = tuple[int, int]
Empty = None


class State:
    """
    State class that represents the state of the game.
    """

    def __init__(self):
        self.board: list[list[Player | Empty]] = [[Empty for _ in range(6)] for _ in range(6)]
        self.player: Player = False
        self.markers: tuple[int, int] = 8, 8
        self.last_move: Position | Empty = Empty


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
    if not state.markers[state.player]:
        return True

    markers = [(i, j) for i, ln in enumerate(state.board) for j, elem in enumerate(ln) if elem is state.player]
    for position in markers:
        if _position_has_win(state, position):
            return True
    return False


def _position_has_win(state: State, position: Position) -> bool:
    for mask in _masks:
        if _position_against_mask(state, position, mask):
            return True
    return False


def _position_against_mask(state: State, position: Position, mask: tuple[int, int, int, int]) -> bool:
    i, j = position
    i0, j0, i1, j1 = mask

    try:
        if not (0 <= i+i0 < 6 and 0 <= j+j0 < 6 and 0 <= i+i1 < 6 and 0 <= j+j1 < 6):
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

    state.last_move = position
    state.board[i][j] = state.player
    state.markers[state.player] -= 1
    state.player = not state.player
    return _push_pieces(state, position)


def _push_pieces(state: State, position: Position) -> State:
    for mask in _masks:
        state = _push_piece(state, position, mask)
    return state


def _push_piece(state: State, position: Position, mask: tuple[int, int, int, int]) -> State:
    i, j = position
    i0, j0, i1, j1 = mask

    if not 0 < i+i0 < 6 or not 0 < j+j0 < 6:
        return state
    if not 0 < i+i1 < 6 or not 0 < j+j1 < 6:
        state.markers[state.board[i+i0][j+j0]] += 1
        state.board[i+i0][j+j0] = Empty

    if state.board[i+i1][j+j1] is not Empty:
        return state

    state.board[i+i0][j+j0], state.board[i+i1][j+j1] = Empty, state.board[i+i0][j+j0]
    return state
