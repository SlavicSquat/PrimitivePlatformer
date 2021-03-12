from pygame.sprite import Sprite
from pygame import Surface
import pygame

MOVE_SPEED = 10
WIDTH = 20
HEIGHT = 70
COLOR = (0, 255, 0)
JUMP_POWER = 6.5
GRAVITY = 0.35

ANIM_LEFT = [pygame.image.load(r'data\sprites\Hero\Hero_left_0.png'),
             pygame.image.load(r'data\sprites\Hero\Hero_left_1.png'),
             pygame.image.load(r'data\sprites\Hero\Hero_left_2.png')]
ANIM_RIGHT = [pygame.image.load(r'data\sprites\Hero\Hero_right_0.png'),
              pygame.image.load(r'data\sprites\Hero\Hero_right_1.png'),
              pygame.image.load(r'data\sprites\Hero\Hero_right_2.png')]
ANIM_STANCE = [pygame.image.load(r'data\sprites\Hero\Hero_stance_l.png'),
               pygame.image.load(r'data\sprites\Hero\Hero_stance_r.png')]
ANIM_COUNT = 0
ANIM_FPS = 10


class Hero(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR)
        self.image.set_colorkey(COLOR)
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)

        self.walk_left = False
        self.walk_right = True

        self.startx = x
        self.starty = y

        self.fenita = False

        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self.past_y = 0
        self.past_x = 0
        self.inAir = False

        self.death = False

        self.stamina = 100

    def collide(self, xvel, yvel, platforms, finish, enemies):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                if enemy.type == 'snake' or enemy.type == 'm_bandit':
                    self.death = True

        for fin in finish:
            if pygame.sprite.collide_rect(self, fin):
                self.fenita = True

    def update(self, left, right, jump, shift, platforms, finish, enemies):
        if self.past_y != self.rect.y:
            self.inAir = True
        else:
            self.inAir = False

        if jump:
            if self.onGround:
                self.yvel = -JUMP_POWER
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel

        if left:
            if shift and self.stamina > 3:
                self.xvel = -(MOVE_SPEED + 5)
            else:
                self.xvel = -MOVE_SPEED
        if right:
            if shift and self.stamina > 3:
                self.xvel = MOVE_SPEED + 5
            else:
                self.xvel = MOVE_SPEED
        if not(left or right):
            self.xvel = 0

        if not shift or (shift and self.past_x == self.rect.x):
            if self.stamina < 100:
                self.stamina += 1
        else:
            if self.stamina > 2:
                self.stamina -= 2

        self.past_y = self.rect.y
        self.past_x = self.rect.x

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, finish, enemies)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, finish, enemies)


class Hero_sprite(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR)
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)

        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self.past_y = 0
        self.past_x = 0
        self.inAir = False

    def update(self, mouse_pos, left, right, jump, shift, hero):
        global ANIM_COUNT
        if ANIM_COUNT >= 29:
            ANIM_COUNT = 0

        if self.past_y != self.rect.y:
            self.inAir = True
        else:
            self.inAir = False

        if jump:
            if self.onGround:
                self.yvel = -JUMP_POWER
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False

        # Direction~~~~~~~~~~~~~~~~~~~~~~~~~
        if mouse_pos < self.rect.x + 50:
            self.walk_right = False
            self.walk_left = True
        if mouse_pos > self.rect.x + 50:
            self.walk_right = True
            self.walk_left = False
        if not (left or right):
            if self.walk_right:
                self.image = ANIM_STANCE[1]
            elif self.walk_left:
                self.image = ANIM_STANCE[0]
        else:
            if self.walk_right:
                self.image = ANIM_RIGHT[ANIM_COUNT // ANIM_FPS]
                ANIM_COUNT += 1
            elif self.walk_left:
                self.image = ANIM_LEFT[ANIM_COUNT // ANIM_FPS]
                ANIM_COUNT += 1
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.image.set_colorkey((255, 255, 255))

        self.past_y = self.rect.y
        self.rect.y = hero.rect.y
        self.rect.x = hero.rect.x - 40


class FireBall(Sprite):
    def __init__(self, x, y, left, right):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((10, 10))
        self.image.fill(pygame.Color((200, 0, 0)))
        self.rect = pygame.Rect(x + 10, y + 20, 10, 10)

        self.exist = True

        self.left = left
        self.right = right

    def collide(self, platforms, enemies, entities):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.exist = False

        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                enemies.remove(enemy)
                entities.remove(enemy)
                self.exist = False

    def update(self):
        if self.left:
            self.rect.x -= 20
        if self.right:
            self.rect.x += 20




class StaminaBar(Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((0, 25))
        self.image.fill(pygame.Color((255, 0, 255)))
        self.rect = pygame.Rect(x, y, 100, 25)

    def update(self, hero):
        self.image = Surface((hero.stamina, 25))
