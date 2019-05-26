import pygame
import sys
from pygame.locals import *

HEIGHT = 400
WIDTH = 400


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 1
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 65, 0))

    screen.blit(background, (0, 0))
    pygame.display.flip()
    while True:
        pygame.event.pump()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
