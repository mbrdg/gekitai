import pygame
import time

import logic.state
import ui.ui


def loop(state, ev, surface):
    if ev.type == pygame.MOUSEBUTTONUP:
        mx, my = pygame.mouse.get_pos()

        size = surface.get_width() / len(state.board)
        j, i = int((my / size) % len(state.board)), int((mx / size) % len(state.board))

        state = logic.move(state, position=(i, j))
    return state


def render(game, screen):
    board = ui.draw_board(game.board_size)
    ui.draw_pieces(game, board)
    screen.blit(board, board.get_rect())
    pygame.display.update()

    return board


def main():
    pygame.init()
    pygame.display.set_caption('Gekitai')
    screen = pygame.display.set_mode(size=(800, 800))

    game = logic.State()

    running = True
    while running:

        board = render(game, screen)
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False

        game = loop(game, event, board)
        if logic.is_over(game):
            _ = render(game, screen)
            print(f'Game Over! Player {int(not game.player) + 1} won!')
            running = False
            time.sleep(10)

    pygame.quit()


if __name__ == '__main__':
    main()
