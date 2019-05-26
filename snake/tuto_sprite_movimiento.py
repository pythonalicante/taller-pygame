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
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.top = random.randint(0, HEIGHT - self.rect.height)

    def update(self):
        self.rect.left=random.randint(0, WIDTH - self.rect.width)
        self.rect.top=random.randint(0, HEIGHT - self.rect.height)


class Snake(pygame.sprite.Sprite):
    STATIC=(0, 0)
    UP=(0, -30)
    DOWN=(0, 30)
    LEFT=(-30, 0)
    RIGHT=(30, 0)

    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect=load_png('box_30.png')

        self.direction=Snake.STATIC

    def move_right(self):
        self.direction=Snake.RIGHT

    def move_left(self):
        self.direction=Snake.LEFT

    def move_up(self):
        self.direction=Snake.UP

    def move_down(self):
        self.direction=Snake.DOWN

    def stop(self):
        self.direction=Snake.STATIC

    def update(self):
        self.rect=self.rect.move(self.direction)


def main():
    screen=pygame.display.set_mode((WIDTH, HEIGHT))
    clock=pygame.time.Clock()
    fps=1
    background=pygame.Surface(screen.get_size())
    background=background.convert()
    background.fill((0, 65, 0))

    apple=Apple()
    applesprite=pygame.sprite.Group(apple)
    snake=Snake()
    snakesprite=pygame.sprite.Group(snake)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        pygame.event.pump()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key in [K_UP, K_w]:
                    snake.move_up()
                if event.key in [K_DOWN, K_s]:
                    snake.move_down()
                if event.key in [K_LEFT, K_a]:
                    snake.move_left()
                if event.key in [K_RIGHT, K_d]:
                    snake.move_right()
            elif event.type == KEYUP:
                if event.key in [K_UP, K_w]:
                    snake.stop()
                if event.key in [K_DOWN, K_s]:
                    snake.stop()
                if event.key in [K_LEFT, K_a]:
                    snake.stop()
                if event.key in [K_RIGHT, K_d]:
                    snake.stop()
        applesprite.update()
        snakesprite.update()
        screen.blit(background, (0, 0))

        applesprite.draw(screen)
        snakesprite.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
