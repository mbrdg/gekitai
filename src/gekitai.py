import pygame as pg

from logic import *
from ui import *


def loop(game, surface):
    mx, my = pg.mouse.get_pos()
    size = surface.get_width() / game.size()
    j, i = int((my / size) % game.size()), int((mx / size) % game.size())

    return move(game, position=(i, j))


def main():
    pg.init()
    pg.display.set_caption('G e k i t a i')
    pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONUP])

    screen = pg.display.set_mode(size=(800, 800))

    game = GameState()
    view = GameView(game, screen)

    running = True
    while running:
        board = view.render()

        event = pg.event.wait()
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            game = loop(game, board)

            if game.is_over():
                print(f'Game Over! Player {game.previous_player} won!')
                _ = view.render()
                pg.time.wait(3500)
                running = False

    pg.quit()


if __name__ == '__main__':
    main()
