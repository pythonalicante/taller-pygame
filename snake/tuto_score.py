#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import random
import pygame
from pygame.locals import *


WIDTH = 640
HEIGHT = 480


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


def draw_score(font, score, screen, image):
    score_text = font.render(f": {score}", True, (0, 0, 0))
    screen.blit(image, (WIDTH-90, 5))
    screen.blit(score_text, (WIDTH-60, 5))


def increase_difficulty(difficulty):
    difficulty += 0.5
    if difficulty > 10:
        difficulty = 10
    return difficulty


class Apple(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('python_30.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        # Update rect to appear in a random position
        self.rect = self.rect.move((random.randint(
            0, WIDTH - self.rect.width), random.randint(0, HEIGHT - self.rect.height)))

    def is_eaten(self, snake):
        for i in range(0, snake.length):
            if self.rect.colliderect(snake.tail[i]):
                return True
        return False

    def update(self):
        _pos = (random.randint(0, WIDTH-self.rect.width),
                random.randint(0, HEIGHT-self.rect.height))
        self.rect = pygame.Rect(
            _pos, (self.rect.width, self.rect.height))


class Snake(pygame.sprite.Sprite):
    UP = (0, -30)
    DOWN = (0, 30)
    LEFT = (-30, 0)
    RIGHT = (30, 0)

    def __init__(self, *args, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('box_30.png')
        self.image_tail, self.rect_tail = load_png('tail_30.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.initial_length = 3
        self.length = self.initial_length
        self.direction = Snake.RIGHT

        self.tail = [self.rect.move(60, 60), self.rect.move(
            30, 60), self.rect.move(0, 60)]
        for i in range(0, 2000):
            self.tail.append(pygame.Rect((-100, -100), (30, 30)))

    def move_right(self):
        self.direction = Snake.RIGHT

    def move_left(self):
        self.direction = Snake.LEFT

    def move_up(self):
        self.direction = Snake.UP

    def move_down(self):
        self.direction = Snake.DOWN

    def is_dead(self):
        # Check if the head collides with borders
        if not self.area.contains(self.tail[0]):
            return True
        # Check if the head collides with itself
        for i in range(2, self.length):
            if self.tail[0].colliderect(self.tail[i]):
                return True
        return False

    def update(self):
        # update previous positions
        for i in range(self.length - 1, 0, -1):
            self.tail[i] = self.tail[i - 1]

        # update position of head of snake
        self.tail[0] = self.tail[0].move(self.direction)

    def draw(self, screen):

        for i in range(0, self.length):
            if i >= self.initial_length:
                screen.blit(self.image_tail, self.tail[i])
            else:
                screen.blit(self.image, self.tail[i])

    def apple_eaten(self):
        self.length += 1


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    f = pygame.font.SysFont('Arial', 30)
    score = 0
    pygame.display.set_caption("Pruebas Pygame")

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    clock = pygame.time.Clock()

    fps = 1

    effect = pygame.mixer.Sound('./assets/eat.ogg')

    apple = Apple()
    applesprite = pygame.sprite.Group(apple)
    snake = Snake()

    draw_score(f, score, screen, apple.image)
    screen.blit(background, (0, 0))

    pygame.display.flip()
    a = True
    while a:
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key in [K_SPACE]:
                    a = False

    while True:
        pygame.event.pump()
        # FPS
        clock.tick(fps)
        # Eventos
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
        # Delete previous positions
        screen.blit(background, (0, 0))  # No optimized
        # screen.blit(background, snake.rect, snake.rect)
        # screen.blit(background, t.get_rect(), t.get_rect())
        # Update positions
        if apple.is_eaten(snake):
            effect.play()
            fps = increase_difficulty(fps)
            score += 1
            snake.apple_eaten()
            apple.update()

        snake.update()
        if snake.is_dead():
            t = f.render(f"GAME OVER", True, (0, 0, 0))
            screen.blit(t, ((WIDTH / 2) - (t.get_rect().w/2), HEIGHT / 2))
            pygame.display.flip()
            time.sleep(2)
            exit(0)
        # Draw new positions
        applesprite.draw(screen)
        snake.draw(screen)
        draw_score(f, score, screen, apple.image)
        pygame.display.flip()
    return 0


if __name__ == '__main__':
    pygame.init()
    main()
