import numpy as np
import pygame as pg


class GameView:

    _GREY = pg.Color('GREY')
    _WHITE = pg.Color('WHITE')
    _RED = pg.Color('RED')
    _BLUE = pg.Color('BLUE')

    def __init__(self, state, screen):
        self._state = state
        self._screen = screen
        self.render()

    def render(self):
        board, ts = self._render_board()
        self._render_pieces(board, ts)
        self._screen.blit(board, board.get_rect())
        pg.display.update()

    def _render_board(self):
        n = self._state.size()
        ts = self._screen.get_width() / n

        bg = pg.Surface((ts * n, ts * n))
        bg.fill(self._WHITE)

        for x in range(0, n):
            for y in range(x % 2, n, 2):
                pg.draw.rect(bg, self._GREY, (x * ts, y * ts, ts, ts))
        return bg, ts

    def _render_pieces(self, board, ts):
        pieces = np.argwhere(self._state.board)

        for position in pieces:
            i, j = position[0], position[1]
            marker = self._state.board[i, j]
            color = self._BLUE if marker == 1 else self._RED

            radius = ts * .385
            x, y = (i + .5) * ts, (j + .5) * ts
            pg.draw.circle(board, color, (x, y), radius)

    def read_mouse_pos(self):
        n = self._state.size()
        ts = self._screen.get_width() / n

        mv = np.array(pg.mouse.get_pos()) / ts % n
        return np.floor(mv).astype(np.uint8)