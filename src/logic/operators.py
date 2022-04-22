from src.logic import GameState

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


def move(state: GameState, position):
    """ Executes a move given a position and returns the mutated game state """
    i, j = position[0], position[1]

    if state.board[i, j]:
        return state

    state.board[i, j] = state.curr_player
    state.set_markers(player=state.curr_player - 1, delta=-1)
    state.swap_player()
    state.last_move = position

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
            state.set_markers(player, delta=1)

        state.board[i + i0, j + j0] = 0
        return state

    # Can't push the piece on the opposite side
    if state.board[i + i1, j + j1]:
        return state

    state.board[i + i0, j + j0], state.board[i + i1, j + j1] = 0, state.board[i + i0, j + j0]
    return state
