import pygame
import sys
import os
from pygame.locals import *

HEIGHT = 400
WIDTH = 400


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('assets', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 1
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 65, 0))
    sprite, rect = load_png('python_30.png')
    screen.blit(background, (0, 0))
    screen.blit(sprite, rect)
    pygame.display.flip()
    while True:
        pygame.event.pump()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        screen.blit(background, (0, 0))

        screen.blit(sprite, rect)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
