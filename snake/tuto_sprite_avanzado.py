import pygame
import sys
import os
import random
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


class Apple(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('python_30.png')
        # Update rect to appear in a random position
        self.rect = self.rect.move((random.randint(
            0, WIDTH - self.rect.width), random.randint(0, HEIGHT - self.rect.height)))

    def update(self):
        _pos = (random.randint(0, WIDTH-self.rect.width),
                random.randint(0, HEIGHT-self.rect.height))
        self.rect = pygame.Rect(
            _pos, (self.rect.width, self.rect.height))


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 1
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 65, 0))

    apple = Apple()
    applesprite = pygame.sprite.Group(apple)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        pygame.event.pump()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        applesprite.update()
        screen.blit(background, (0, 0))

        applesprite.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
