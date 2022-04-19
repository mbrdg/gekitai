import numpy as np
from scipy.signal import convolve2d


def board_evaluation(game, is_over, is_max):
    """ Evaluator function for the board """

    # If the game is over just return the best value according to the game winner
    # If the game is over the winner is the previous player
    if is_over:
        return np.NINF if is_max else np.PINF

    me = game.curr_player if is_max else game.prev_player
    opponent = game.prev_player if is_max else game.curr_player

    # Evaluation of the number of markers already placed
    my_placed = np.count_nonzero(game.board == me)
    opponent_placed = np.count_nonzero(game.board == opponent)
    score = (-8 / (my_placed - 8.01) - 1) - (-8 / (opponent_placed - 8.01) - 1)

    # Evaluation of the number of consecutive markers
    kernels = [np.ones(shape=(1, 2)), np.ones(shape=(2, 1)), np.eye(2), np.fliplr(np.eye(2))]
    for kernel in kernels:
        score += np.count_nonzero(convolve2d(game.board == me, kernel, mode='valid') == 2) * 10.0
        score -= np.count_nonzero(convolve2d(game.board == opponent, kernel, mode='valid') == 2) * 10.0

    return score
