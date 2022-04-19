import numpy as np
from scipy.signal import convolve2d


def markers_evaluator(game, is_max, *, markers=8):
    """ Evaluation based on the number of markers already placed """
    me = game.curr_player if is_max else game.prev_player
    opponent = game.prev_player if is_max else game.curr_player

    my_placed = np.count_nonzero(game.board == me)
    opponent_placed = np.count_nonzero(game.board == opponent)

    def f(p, m):
        return np.inf if p - m == 0 else -m / (p - m) - 1

    return f(my_placed, markers) - f(opponent_placed, markers)


def combination_evaluator(game, is_max, weight=10.0):
    """ Evaluation of consecutive markers of the same player """
    me = game.curr_player if is_max else game.prev_player
    opponent = game.prev_player if is_max else game.curr_player

    score = 0
    kernels = [np.ones(shape=(1, 2)), np.ones(shape=(2, 1)), np.eye(2), np.fliplr(np.eye(2))]
    for kernel in kernels:
        score += np.count_nonzero(convolve2d(game.board == me, kernel, mode='valid') == 2) * weight
        score -= np.count_nonzero(convolve2d(game.board == opponent, kernel, mode='valid') == 2) * weight

    return score


def mix_evaluator(game, is_max, *, markers=8, weight=10.0):
    """ Better evaluation function that combines the markers already placed and their combinations """
    markers_score = markers_evaluator(game, is_max, markers=markers)
    combination_score = combination_evaluator(game, is_max, weight=weight)

    return markers_score + combination_score
