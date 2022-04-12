import numpy as np


"""
These are the various evaluator functions proposed.

All of the them have something in common, they must give a high (positive) 
value for the maximizing player and a low (negative) to the minimizing player.

As it is expected some of them are better than others...

Basically in the current implemented evaluation functions are:
    - place_all -> Tries to place all the 8 tiles in order to win.
    - consecutive -> Tries to look for consecutive markers of the same player
    - mix -> Combines the both using specified heights
"""


def _neighbours(state, position, layers=1):
    bottom, top = max(0, position[1] - layers), max(0, position[1] + layers + 1)
    left, right = max(0, position[0] - layers), max(0, position[0] + layers + 1)

    return state.board[left:right, bottom:top]


def all_no_opponent(game, is_max):
    score = game.get_markers(game.current_player)

    # Working in a negamax fashion
    return score if is_max else -score


def all_(game, is_max):
    max_player = game.current_player if is_max else game.previous_player
    min_player = game.previous_player if is_max else game.current_player

    return game.get_markers(max_player) - game.get_markers(min_player)


def consecutive_no_opponent(game, is_max):
    player = game.current_player if is_max else game.previous_player
    markers = np.argwhere(game.board == player)
    score = 0

    for m in markers:
        board = _neighbours(game, m, layers=1)
        score += np.count_nonzero(board == game.current_player)

    # Working in a negamax fashion
    return score if is_max else -score


def consecutive(game, is_max):
    max_player = game.current_player if is_max else game.previous_player
    min_player = game.previous_player if is_max else game.current_player

    max_markers = np.argwhere(game.board == max_player)
    min_markers = np.argwhere(game.board == min_player)
    score = 0

    for m in max_markers:
        board = _neighbours(game, m, layers=1)
        score += np.count_nonzero(board == game.current_player)

    for m in min_markers:
        board = _neighbours(game, m, layers=1)
        score -= np.count_nonzero(board == game.previous_player)

    return score


def mix(game, is_max, consecutive_height=1.25, all_height=1.0):
    # TODO: Create an heuristic that changes the heights on the fly
    return consecutive_height * consecutive(game, is_max) + all_height * all_(game, is_max)
