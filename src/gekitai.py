import pygame as pg
import sys

from logic import GameState
from ui import GameView, MenuView, MenuState, loop


def main():
    pg.init()
    pg.display.set_caption('gekitai')
    screen = pg.display.set_mode(size=(800, 800))
    pg.event.set_allowed(pg.QUIT)

    while loop:
        config = MenuState()
        view = MenuView(config, screen)


        menu = True
        main = True
        rules = False
        size = False
        markers = False
        mode = False
        alg = False



        while menu:

            while main:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            view.selected = (view.selected - 1) % len(view.options)
                        elif event.key == pg.K_DOWN:
                            view.selected = (view.selected + 1) % len(view.options)
                        if event.key == pg.K_RETURN:
                            if view.selected == 0:
                                view.title = 'BOARD SIZE'
                                view.selected = 0
                                view.options = ['6 x 6', '7 x 7', '8 x 8', '9 x 9', '10 x 10', 'BACK']
                                main = False
                                size = True
                            if view.selected == 1:
                                view.title = 'Rules'
                                view.selected = 0
                                view.show_rules = True
                                view.options = ['BACK']
                                main = False
                                rules = True
                            if view.selected == 2:
                                pg.quit()
                                quit()
                    view.render()

            while size:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            view.selected = (view.selected - 1) % len(view.options)
                        elif event.key == pg.K_DOWN:
                            view.selected = (view.selected + 1) % len(view.options)
                        if event.key == pg.K_RETURN:
                            if view.selected == 5:
                                view.title = 'GEKITAI'
                                view.options = ['Play', 'Rules', 'Exit']
                                view.selected = 0
                                size = False
                                main = True
                            else:
                                view.config.size = 6 + view.selected
                                view.title = 'NUMBER OF MARKERS'
                                view.selected = 0
                                view.options = ['5', '6', '7', '8', 'BACK']
                                size = False
                                markers = True
                    view.render()

            while markers:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            view.selected = (view.selected - 1) % len(view.options)
                        elif event.key == pg.K_DOWN:
                            view.selected = (view.selected + 1) % len(view.options)
                        if event.key == pg.K_RETURN:
                            if view.selected == 4:
                                view.title = 'BOARD SIZE'
                                view.options = ['6 x 6', '7 x 7', '8 x 8', '9 x 9', '10 x 10', 'BACK']
                                view.selected = 0
                                markers = False
                                size = True
                            else:
                                view.config.markers = 5 + view.selected
                                view.title = 'MODE'
                                view.options = ['Player vs. PLayer', 'Player vs. Computer', 'Computer vs. Player',
                                                'Computer vs. Computer', 'Back']
                                markers = False
                                mode = True
                    view.render()

            while rules:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            view.selected = (view.selected - 1) % len(view.options)
                        elif event.key == pg.K_DOWN:
                            view.selected = (view.selected + 1) % len(view.options)
                        if event.key == pg.K_RETURN:
                            if view.selected == 0:
                                view.title = 'GEKITAI'
                                view.options = ['Play', 'Rules', 'Exit']
                                view.selected = 0
                                rules = False
                                main = True
                                view.show_rules = False

                    view.render()

            while mode:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            view.selected = (view.selected - 1) % len(view.options)
                        elif event.key == pg.K_DOWN:
                            view.selected = (view.selected + 1) % len(view.options)
                        if event.key == pg.K_RETURN:
                            if view.selected == 4:
                                view.title = 'NUMBER OF MARKERS'
                                view.selected = 0
                                view.options = ['5', '6', '7', '8', 'BACK']
                                mode = False
                                markers = True
                            else:
                                if view.selected == 0:
                                    view.config.config[0]['is_pc'], view.config.config[1]['is_pc'] = False, False

                                if view.selected == 1:
                                    view.config.config[0]['is_pc'], view.config.config[1]['is_pc'] = False, True

                                if view.selected == 2:
                                    view.config.config[0]['is_pc'], view.config.config[1]['is_pc'] = True, False

                                if view.selected == 3:
                                    view.config.config[0]['is_pc'], view.config.config[1]['is_pc'] = True, True

                                view.title = 'ALGORITHMS'
                                view.options = ['MINIMAX VS MINIMAX', 'MINIMAX VS MCTS', 'MCTS VS MINIMAX', 'MCTS VS MCTS',
                                                'BACK']
                                view.selected = 0
                                mode = False
                                alg = True

                    view.render()

            while alg:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_UP:
                            view.selected = (view.selected - 1) % len(view.options)
                        elif event.key == pg.K_DOWN:
                            view.selected = (view.selected + 1) % len(view.options)
                        if event.key == pg.K_RETURN:
                            if view.selected == 4:
                                view.title = 'MODE'
                                view.options = ['Player vs. PLayer', 'Player vs. Computer', 'Computer vs. Player',
                                                'Computer vs. Computer', 'Back']
                                alg = False
                                mode = True
                                view.selected = 0
                            else:
                                if view.selected == 0:
                                    view.config.config[0]['algo'], view.config.config[1]['algo'] = 'Minimax', 'Minimax'

                                if view.selected == 1:
                                    view.config.config[0]['algo'], view.config.config[1]['algo'] = 'Minimax', 'MCTS'

                                if view.selected == 2:
                                    view.config.config[0]['algo'], view.config.config[1]['algo'] = 'MCTS', 'Minimax'

                                if view.selected == 3:
                                    view.config.config[0]['algo'], view.config.config[1]['algo'] = 'MCTS', 'MCTS'
                                main = True
                                alg = False
                                menu = False

                    view.render()

        game = GameState(config.size, config.markers)
        view = GameView(game, screen)

        running = True
        while running:
            if pg.event.peek(pg.QUIT):
                pg.quit()
                sys.exit(1)

            game = loop(game, view, config.config, verbose=True)
            view.render()

            is_over, winner = game.is_over(verbose=True)
            if is_over:
                print(f'Game Over! Player {winner} won!')
                running = False

        pg.time.wait(10_000)



if __name__ == '__main__':
    main()
