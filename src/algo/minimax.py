import numpy as np
import pickle

from src.logic import move


def minimax(game, evaluator, depth, is_max=True, alpha=np.NINF, beta=np.PINF):
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
        return evaluator(game), game.last_move

    parent = pickle.dumps(game, protocol=-1)
    if is_max:
        max_v, best_mv = np.NINF, None
        for action in game.actions():
            child = pickle.loads(parent)
            child = move(child, action)

            v, mv = minimax(child, evaluator, depth - 1, False, alpha, beta)
            max_v, best_mv = max(max_v, v), action if v > max_v else best_mv

            if beta <= alpha:
                break
        return max_v, best_mv

    else:
        min_v, best_mv = np.PINF, None
        for action in game.actions():
            child = pickle.loads(parent)
            child = move(child, action)

            v, mv = minimax(child, evaluator, depth - 1, True, alpha, beta)
            min_v, best_mv = min(min_v, v), action if v < min_v else best_mv

            if beta <= alpha:
                break
        return min_v, best_mv
