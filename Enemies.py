from pygame import Surface
import pygame
from blocks import Platform

clock = pygame.time.Clock()

SNAKE_WIDTH = 30
SNAKE_HEIGHT = 70
SNAKE_COLOR = (0, 100, 0)

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (0, 0, 0)


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((SNAKE_WIDTH, SNAKE_HEIGHT))
        self.image.fill(pygame.Color(SNAKE_COLOR))
        self.rect = pygame.Rect(x, y, SNAKE_WIDTH, SNAKE_HEIGHT)

