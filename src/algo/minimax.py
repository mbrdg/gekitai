import numpy as np

from src.logic import *


def minimax(game, evaluator, depth, is_max, alpha=np.PINF, beta=np.NINF):
    """
    Minimax algorithm implementation with alpha-beta cuts
    ---
    :param game: Current game state
    :param evaluator: Function that evaluates the game state
    :param depth: Number of turns to see ahead
    :param is_max: If true tries to maximize the result otherwise tries to minimize
    :param alpha: Current best value for the maximizer
    :param beta: Current best value for the minimizer
    :return: Best move and the corresponding value according to the algorithm
    """

    if not depth or game.is_over():
        return evaluator(game, is_max), game.last_move

    v, mv = np.PINF if is_max else np.NINF, None

    for action in game.actions():
        child = move(game, action)

        if is_max:
            max_v, max_m = minimax(child, evaluator, depth - 1, False, alpha, beta)
            v, mv = max(v, max_v), max_m if max_v > v else mv
            alpha = max(alpha, v)

            if beta <= alpha:
                break

        else:
            min_v, min_m = minimax(child, evaluator, depth - 1, True, alpha, beta)
            v, mv = min(v, min_v), min_m if min_v < v else mv
            beta = min(beta, v)

            if alpha <= beta:
                break

    return v, mv
