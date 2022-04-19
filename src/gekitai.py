import pygame as pg
from time import perf_counter

from logic import GameState, move
from ui import GameView
from algo import minimax, mcts, board_evaluation


def loop(game, view, is_pc):
    if is_pc:
        start = perf_counter()
        # _, mv = minimax(game, board_evaluation, depth=3)
        mv = mcts(game, iterations=2048)
        elapsed = perf_counter() - start
        # print(f"Minimax: Executed move {mv[0], mv[1]}, took {elapsed:.2f} secs")
        print(f"MCTS: Executed move {mv[0], mv[1]}, took {elapsed:.2f} secs")
    else:
        mv = view.read_mouse_pos()

    game = move(game, position=mv)
    view.render()
    return game


def main():
    pg.init()
    pg.display.set_caption('G e k i t a i')
    pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONUP])

    screen = pg.display.set_mode(size=(800, 800))

    game = GameState()
    view = GameView(game, screen)

    running, is_pc = True, False
    while running:

        if is_pc:
            game = loop(game, view, is_pc)
            is_pc = False

        else:
            event = pg.event.wait()
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                game = loop(game, view, is_pc)
                is_pc = True

        is_over, winner = game.is_over(verbose=True)
        if is_over:
            print(f'Game Over! Player {winner} won!')
            pg.time.wait(3500)
            running = False

    pg.quit()


if __name__ == '__main__':
    main()
