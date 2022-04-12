import pygame.draw

GREY = pygame.Color('GREY')
WHITE = pygame.Color('WHITE')
RED = pygame.Color('RED')
BLUE = pygame.Color('BLUE')


def draw_board(n: int):
    ts = 800 / n
    bg = pygame.Surface((n * ts, n * ts))
    bg.fill(GREY)

    for x in range(0, n):
        for y in range(x % 2, n, 2):
            pygame.draw.rect(bg, WHITE, (x * ts, y * ts, ts, ts))
    return bg


def draw_pieces(game, board):
    ts = 800 / game.board_size

    for x, ln in enumerate(game.board):
        for y, marker in enumerate(ln):
            _draw_piece(board, marker, size=ts, position=(x, y))


def _draw_piece(surface, marker, size, position):
    if marker is None:
        return

    color = RED if marker else BLUE
    radius = size * 0.385
    x, y = position
    x, y = (x + 0.5) * size, (y + 0.5) * size
    pygame.draw.circle(surface, color, (x, y), radius)
