import numpy as np
import pygame as pg
from time import perf_counter

from src.logic import move
from src.algo import minimax, mcts, evaluators

# Missing constant from pygame :/
LEFT_BUTTON = 1


def _run(game, algorithm, verbose=True):
    start = perf_counter()
    if algorithm == 'Minimax':
        _, mv = minimax(game, evaluators.mix_evaluator, depth=4)
    elif algorithm == 'MCTS':
        mv = mcts(game, iterations=4096, ci=np.sqrt(2.0))
    else:
        raise RuntimeError
    end = perf_counter()

    if verbose:
        print(f"{algorithm}: executed move {mv}, took {end - start:.2f} secs")
    return mv


def loop(game, view, config, *, verbose=True):
    conf = config[game.current_player - 1]

    if conf['is_pc']:
        mv = _run(game, conf['algo'], verbose)
    else:
        pg.event.set_allowed((pg.KEYUP, pg.MOUSEBUTTONUP))
        event = pg.event.wait()

        if event.type == pg.MOUSEBUTTONUP and event.button == LEFT_BUTTON:
            mv = view.read_mouse_pos()
            if game.board[mv[0], mv[1]]:
                return game

        else:
            if event.type == pg.KEYUP and event.key == pg.K_h:
                help_mv = _run(game, conf['algo'], verbose=False)
                print(f"Hint provided by {conf['algo']}: {help_mv}")
            return game

        pg.event.set_blocked((pg.KEYUP, pg.MOUSEBUTTONUP))
    return move(game, mv)
