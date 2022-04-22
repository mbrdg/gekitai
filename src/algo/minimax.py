import numpy as np
from copy import deepcopy

from src.logic.operators import move


def minimax(game, evaluator, depth, alpha=np.NINF, beta=np.PINF, *, is_max=True, **kwargs):
    """ Minimax algorithm implementation with alpha-beta cuts """

    if not depth:
        return evaluator(game, is_max, **kwargs), game.last_move

    is_over, winner = game.is_over()
    if is_over:
        score = (2 ^ 63 - 1) if not is_max and winner == game.previous_player else -(2 ^ 63 - 1)
        return score, game.last_move

    if is_max:
        max_v, best_mv = -np.inf, None
        for action in game.actions():
            child = deepcopy(game)
            child = move(child, action)

            v, _ = minimax(child, evaluator, depth - 1, alpha, beta, is_max=False, **kwargs)
            max_v, best_mv = max(max_v, v), action if v > max_v else best_mv
            alpha = max(alpha, v)

            if beta <= alpha:
                break
        return max_v, best_mv

    else:
        min_v, best_mv = np.PINF, None
        for action in game.actions():
            child = deepcopy(game)
            child = move(child, action)

            v, _ = minimax(child, evaluator, depth - 1, alpha, beta, is_max=True, **kwargs)
            min_v, best_mv = min(min_v, v), action if v < min_v else best_mv
            beta = min(beta, v)

            if beta <= alpha:
                break
        return min_v, best_mv
