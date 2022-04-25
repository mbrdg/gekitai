import numpy as np
import pygame as pg
import os


class MenuView:
    _CORAL4 = pg.Color('CORAL4')
    _BLACK = pg.Color('BLACK')
    _GREY = pg.Color('GREY')
    _RED = pg.Color('RED')
    _GREEN = pg.Color('GREEN')
    _BLUE = pg.Color('BLUE')
    _ROYALBLUE4 = pg.Color('ROYALBLUE4')

    def __init__(self, config, screen):
        self.config = config
        self._screen = screen
        self.title = 'Gekitai'
        self.options = ['Play', 'Rules', 'Exit']
        self.show_rules = False
        self.rules = ['Gekitai™ (Repel or Push Away) is a 3-in-a-row game played on a 6x6 grid.',
                      'Each player has eight colored markers and takes turns placing them anywhere',
                      'on any open space on the board.When placed, a marker pushes all adjacent pieces',
                      'outwards one space if there is an open space for it to move to (or off the board).',
                      'Pieces shoved off the board are returned to the player.',
                      'If there is not an open space on the opposite side of the pushed piece,',
                      'it does not push (a newly played piece cannot push two or more other lined-up pieces).',
                      'The first player to either line up three of their color in a row at the end of their',
                      'turn (after pushing) OR have all eight of their markers on the board (also after pushing) wins', ]
        self.selected = 0
        self.render()

    def text_format(self, message, textSize, textColor):
        newFont = pg.font.Font(None, textSize)
        newText = newFont.render(message, False, textColor)

        return newText

    def render(self):
        self._screen.fill(self._GREY)
        title = self.text_format(self.title, 90, self._ROYALBLUE4)
        title_rect = title.get_rect()
        self._screen.blit(title, (self._screen.get_width() / 2 - (title_rect[2] / 2), 80))

        if self.show_rules:
            for x in range(0, len(self.rules)):
                text = self.text_format(self.rules[x], 25, self._BLACK)
                text_rect = text.get_rect()
                self._screen.blit(text, (self._screen.get_width() / 2 - (text_rect[2] / 2), 270 + x * 30))

        for x in range(0, len(self.options)):
            if self.selected == x:
                text = self.text_format(self.options[x], 75, self._CORAL4)
            else:
                text = self.text_format(self.options[x], 75, self._BLACK)
            text_rect = text.get_rect()
            self._screen.blit(text, (self._screen.get_width() / 2 - (text_rect[2] / 2), 200 + x * 70))

        pg.display.update()



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
