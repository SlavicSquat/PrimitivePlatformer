from pygame import *
import pygame
from Hero import Hero
from blocks import Platform, False_Platform
from Fone import Fone
from Enemies import Snake
from maps import level_1


PLATFORM_WIDTH = 15
PLATFORM_HEIGHT = 15
PLATFORM_COLOR = (0, 0, 20)

jump = left = right = False

if __name__ == '__main__':
    init()
    size = width, height = 1080, 720
    window = display.set_mode(size)
    screen = Surface(size)

    entities = sprite.Group()
    platforms = []
    false_platforms = []
    fire_throwers = []
    fire_sprites = []
    enemies = []

    fone = Fone(r'data\fones\test_bg.png')
    entities.add(fone)

    running = True
    clock = time.Clock()

    simple_theme = pygame.mixer.Sound(r'data\music\test_theme.ogg')

    x = y = 0
    for row in level_1:
        simple_theme.play(-1)
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == '@':
                f_pf = False_Platform(x, y)
                entities.add(f_pf)
                false_platforms.append(f_pf)
            if col == '$':
                snake = Snake(x, y)
                entities.add(snake)
                enemies.append(snake)
            if col == '!':
                hero = Hero(x, y)
                entities.add(hero)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    while running:
        screen.fill((100, 255, 255))
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and (e.key == K_SPACE or e.key == K_w):
                jump = True
            if e.type == KEYUP and (e.key == K_SPACE or e.key == K_w):
                jump = False

            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True

            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False

        entities.draw(screen)
        hero.update(left, right, jump, platforms, false_platforms, enemies)
        window.blit(screen, (0, 0))
        clock.tick(60)
        display.flip()
