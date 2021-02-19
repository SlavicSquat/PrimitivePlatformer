from pygame import *
import pygame
from Hero import Hero
from blocks import Platform, False_Platform
from Camera import Camera
from Fone import Fone
from Enemies import Snake
from maps import level_1


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+width / 2, -t+height / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-width), l)       # Не движемся дальше правой границы
    t = max(-(camera.height-height), t)     # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


PLATFORM_WIDTH = 30
PLATFORM_HEIGHT = 30
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

    fone = Fone(r'data\fones\simple_bg.png')
    entities.add(fone)

    running = True
    clock = time.Clock()

    simple_theme = pygame.mixer.Sound(r'data\music\theme.ogg')

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

    total_level_width = len(level_1[0]) * PLATFORM_WIDTH
    total_level_height = len(level_1) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    while running:
        screen.fill((100, 255, 255))
        for e in event.get():
            if e.type == QUIT:
                running = False
            if e.type == KEYDOWN and e.key == K_SPACE:
                jump = True
            if e.type == KEYUP and e.key == K_SPACE:
                jump = False

            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True

            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False

        for e in entities:
            screen.blit(e.image, camera.apply(e))
        hero.update(left, right, jump, platforms, false_platforms, enemies)
        camera.update(hero)
        window.blit(screen, (0, 0))
        clock.tick(60)
        display.flip()
