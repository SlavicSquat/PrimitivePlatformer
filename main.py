from pygame import *
import pygame
from Hero import Hero_sprite, Hero, StaminaBar
from Hero import FireBall
from blocks import Platform, Finish
from Fone import Fone
from Enemies import Snake
from Enemies import M_bandit, B_bandit, A_bandit
from maps import level_1, level_2, level_3


PLATFORM_WIDTH = 15
PLATFORM_HEIGHT = 15
PLATFORM_COLOR = (121, 25, 20)

jump = left = right = shift = False


def keyupdate():
    global event, jump, left, right, shift, mouse_pos_x
    mouse_pos_x = mouse.get_pos()[0]

    if e.type == MOUSEBUTTONDOWN:
        f = FireBall(hero.rect.x, hero.rect.y, hero_sprite.walk_left, hero_sprite.walk_right)
        entities.add(f)
        fires.append(f)

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

    if e.type == KEYDOWN and e.key == K_LSHIFT:
        shift = True
    if e.type == KEYUP and e.key == K_LSHIFT:
        shift = False


def create_level(level):
    global entities, platforms, enemies, fin, hero, hero_sprite, stamina_bar, fires, clock
    entities = sprite.Group()
    platforms = []
    fin = []
    enemies = []

    fires = []

    entities.add(fone)
    clock = time.Clock()
    stamina_bar = StaminaBar(25, 740)
    entities.add(stamina_bar)
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == '$':
                snake = Snake(x, y)
                entities.add(snake)
                enemies.append(snake)
            if col == '!':
                hero_sprite = Hero_sprite(x, y)
                hero = Hero(x, y)
                entities.add(hero_sprite)
                entities.add(hero)
            if col == 'f':
                finish = Finish(x, y)
                entities.add(finish)
                fin.append(finish)
            if col == '%':
                a_bandit = A_bandit(x, y)
                entities.add(a_bandit)
                enemies.append(a_bandit)
            if col == '&':
                m_bandit = M_bandit(x, y)
                entities.add(m_bandit)
                enemies.append(m_bandit)
            if col == '*':
                b_bandit = B_bandit(x, y)
                entities.add(b_bandit)
                enemies.append(b_bandit)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


def game_update(level):
    if hero.death:
        create_level(level)
    entities.draw(screen)
    stamina_bar.update(hero)
    hero_sprite.update(mouse_pos_x, left, right, jump, shift, hero)
    hero.update(left, right, jump, shift, platforms, fin, enemies)

    for fire in fires:
        fire.update()
        fire.collide(platforms, enemies, entities)
        if not fire.exist:
            entities.remove(fire)
            fires.remove(fire)

    for enemy in enemies:
        if enemy.type == 'm_bandit':
            if enemy.agred:
                if enemy.rect.x > hero.rect.x:
                    enemy.left = True
                    enemy.right = False
                if enemy.rect.x < hero.rect.x:
                    enemy.right = True
                    enemy.left = False
            if not enemy.agred:
                enemy.right = False
                enemy.left = False
            enemy.update(platforms, hero)
        if enemy.type == 'snake':
            enemy.update(platforms)
    window.blit(screen, (0, 0))
    clock.tick(60)
    display.flip()


if __name__ == '__main__':
    init()
    size = width, height = 1080, 780
    window = display.set_mode(size)
    screen = Surface(size)

    fone = Fone(r'data\fones\test_bg.png')

    lvl_1 = lvl_2 = lvl_3 = True

    pygame.mixer.music.load(r'data\music\for_game.ogg')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    create_level(level_1)

    while lvl_1:
        screen.fill((100, 255, 255))
        for e in event.get():
            if e.type == QUIT:
                lvl_1 = lvl_2 = lvl_3 = False
            keyupdate()
        if hero.fenita:
            lvl_1 = False
        game_update(level_1)

    create_level(level_2)

    while lvl_2:
        screen.fill((100, 255, 255))
        for e in event.get():
            if e.type == QUIT:
                lvl_1 = lvl_2 = lvl_3 = False
            keyupdate()
        if hero.fenita:
            lvl_2 = False
        game_update(level_2)

    create_level(level_3)

    while lvl_3:
        screen.fill((100, 255, 255))
        for e in event.get():
            if e.type == QUIT:
                lvl_1 = lvl_2 = lvl_3 = False
            keyupdate()
        if hero.fenita:
            lvl_3 = False
        game_update(level_3)

print('Finita...')
