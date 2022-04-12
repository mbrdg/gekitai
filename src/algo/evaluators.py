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


def all_no_opponent(game):
    return game.get_markers(game.previous_player)


def all_(game):
    return game.get_markers(game.previous_player) - game.get_markers(game.current_player)


def consecutive_no_opponent(game):
    markers = np.argwhere(game.board == game.previous_player)
    score = 0

    for m in markers:
        board = _neighbours(game, m, layers=1)
        score += np.count_nonzero(board == game.previous_player)

    return score


def consecutive(game):
    max_player_markers = np.argwhere(game.board == game.previous_player)
    min_player_markers = np.argwhere(game.board == game.current_player)
    score = 0

    for m in max_player_markers:
        board = _neighbours(game, m, layers=1)
        score += np.count_nonzero(board == game.previous_player)

    for m in min_player_markers:
        board = _neighbours(game, m, layers=1)
        score -= np.count_nonzero(board == game.current_player)

    return score


def mix(game, consecutive_height=1.5, all_height=1.0):
    # TODO: Create an heuristic that changes the heights on the fly
    return consecutive_height * consecutive(game) + all_height * all_(game)
