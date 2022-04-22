import pygame as pg
import sys

from logic import GameState
from ui import GameView, start_menu, loop


def main():
    config = start_menu()

    pg.init()
    pg.display.set_caption('gekitai')
    screen = pg.display.set_mode(size=(800, 800))
    pg.event.set_allowed(pg.QUIT)

    game = GameState(size=6, markers=8)
    view = GameView(game, screen)

    running = True
    while running:
        if pg.event.peek(pg.QUIT):
            pg.quit()
            sys.exit(1)

        game = loop(game, view, config, verbose=True)
        view.render()

        is_over, winner = game.is_over(verbose=True)
        if is_over:
            print(f'Game Over! Player {winner} won!')
            running = False

    pg.time.wait(10_000)
    pg.quit()


if __name__ == '__main__':
    main()
