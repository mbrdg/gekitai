import pygame


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Gekitai')

    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)

    rect = pygame.rect.Rect(10, 10, 100, 100)
    pygame.draw.rect(screen, pygame.color.Color(255, 255, 0), rect)

    running = True
    while running:
        pygame.display.update(rect)
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False

    pygame.quit()
