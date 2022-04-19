import numpy as np
from scipy.signal import convolve2d


def _is_over(is_max):
    """ If the game is over, returns the score depending on the winner """
    return np.NINF if is_max else np.PINF


def _markers_evaluator(game, is_max, markers=8):
    me = game.curr_player if is_max else game.prev_player
    opponent = game.prev_player if is_max else game.curr_player

    my_placed = np.count_nonzero(game.board == me)
    opponent_placed = np.count_nonzero(game.board == opponent)

    def f(p, m):
        return np.inf if p - m == 0 else -m / (p - m) - 1

    return f(my_placed, markers) - f(opponent_placed, markers)


def markers_evaluator(game, is_max, is_over, *, markers=8):
    """ Evaluation based on the number of markers already placed """
    if is_over:
        return _is_over(is_max)
    return _markers_evaluator(game, markers)


def _combination_evaluator(game, is_max, weight=10.0):
    me = game.curr_player if is_max else game.prev_player
    opponent = game.prev_player if is_max else game.curr_player

    score = 0
    kernels = [np.ones(shape=(1, 2)), np.ones(shape=(2, 1)), np.eye(2), np.fliplr(np.eye(2))]
    for kernel in kernels:
        score += np.count_nonzero(convolve2d(game.board == me, kernel, mode='valid') == 2) * weight
        score -= np.count_nonzero(convolve2d(game.board == opponent, kernel, mode='valid') == 2) * weight

    return score


def combination_evaluator(game, is_max, is_over, *, weight=10.0):
    """ Evaluation of consecutive markers of the same player """
    if is_over:
        return _is_over(is_max)
    return _combination_evaluator(game, is_max, weight)


def mix_evaluator(game, is_max, is_over, *, markers=8, weight=10.0):
    """ Better evaluation function that combines the markers already placed and their combinations """
    if is_over:
        return _is_over(is_max)

    markers_score = _markers_evaluator(game, is_max, markers)
    combination_score = _combination_evaluator(game, is_max, weight)

    return markers_score + combination_score
