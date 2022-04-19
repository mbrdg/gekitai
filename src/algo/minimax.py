import numpy as np
from copy import deepcopy

from src.logic import move


def minimax(game, evaluator, depth, alpha=np.NINF, beta=np.PINF, *, is_max=True, **kwargs):
    """
    Minimax algorithm implementation with alpha-beta cuts
    ---
    :param game: Current game state
    :param evaluator: Function that evaluates the game state
    :param depth: Number of turns to see ahead
    :param alpha: Current best value for the maximizer
    :param beta: Current best value for the minimizer
    :param is_max: If true tries to maximize the result otherwise tries to minimize
    :return: Best move and the corresponding value according to the algorithm
    """

    if not depth:
        return evaluator(game, is_max, **kwargs), game.last_move

    is_over, winner = game.is_over()
    if is_over:
        score = np.inf if not is_max and winner == game.prev_player else -np.inf
        return score, game.last_move

    if is_max:
        max_v, best_mv = np.NINF, None
        for action in game.actions():
            child = deepcopy(game)
            child = move(child, action)

            v, _ = minimax(child, evaluator, depth - 1, alpha, beta, is_max=False, **kwargs)
            max_v, best_mv = max(max_v, v), action if v > max_v else best_mv

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

            if beta <= alpha:
                break
        return min_v, best_mv
