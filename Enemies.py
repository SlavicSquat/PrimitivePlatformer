from pygame import Surface
import pygame
from blocks import Platform

clock = pygame.time.Clock()

GRAVITY = 0.35

# Snake parameters
SNAKE_WIDTH = 20
SNAKE_HEIGHT = 50
SNAKE_COLOR = (0, 100, 0)

SNAKE_ANIM = [pygame.image.load(r'data\sprites\snake\snake_1.png'),
             pygame.image.load(r'data\sprites\snake\snake_2.png'),
             pygame.image.load(r'data\sprites\snake\snake_3.png')]

SNAKE_ANIM_COUNT = 0
SNAKE_ANIM_FPS = 10

# m_bandit parameters
M_BANDIT_WIDTH = 20
M_BANDIT_HEIGHT = 50
M_BANDIT_COLOR = (100, 0, 0)
M_BANDIT_SPEED = 5

# a_bandit parameters
A_BANDIT_WIDTH = 20
A_BANDIT_HEIGHT = 50
A_BANDIT_COLOR = (100, 100, 0)

# b_bandit parameters
B_BANDIT_WIDTH = 20
B_BANDIT_HEIGHT = 50
B_BANDIT_COLOR = (100, 0, 100)
B_BANDIT_SPEED = 10


class Snake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((SNAKE_WIDTH, SNAKE_HEIGHT))
        self.image.fill(pygame.Color(SNAKE_COLOR))
        self.rect = pygame.Rect(x, y, SNAKE_WIDTH, SNAKE_HEIGHT)

        self.type = 'snake'

        self.startx = x
        self.starty = y

        self.xvel = 0
        self.yvel = 0
        self.onGround = False

    def collide(self, xvel, yvel, platforms):
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

    def update(self, platforms):
        global SNAKE_ANIM_COUNT
        if SNAKE_ANIM_COUNT >= 29:
            SNAKE_ANIM_COUNT = 0

        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel

        self.image = SNAKE_ANIM[SNAKE_ANIM_COUNT // SNAKE_ANIM_FPS]
        self.image.set_colorkey((255, 255, 255))
        SNAKE_ANIM_COUNT += 1

        self.rect.y += self.yvel
        self.collide(self.xvel, 0, platforms)

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)


class M_bandit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((M_BANDIT_WIDTH, M_BANDIT_HEIGHT))
        self.image.fill(pygame.Color(M_BANDIT_COLOR))
        self.rect = pygame.Rect(x, y, M_BANDIT_WIDTH, M_BANDIT_HEIGHT)

        self.radius = 200
        self.agred = False

        self.type = 'm_bandit'

        self.detectCircle = 2 * 3.14 * 10

        self.startx = x
        self.starty = y

        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self.left = False
        self.right = False

    def collide(self, xvel, yvel, platforms, hero):
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

        if pygame.sprite.collide_circle(self, hero):
            self.agred = True

    def update(self, platforms, hero):
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel

        if self.agred:
            if self.left:
                self.xvel = -M_BANDIT_SPEED
            elif self.right:
                self.xvel = M_BANDIT_SPEED
        if not(self.left or self.right):
            self.xvel = 0

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, hero)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, hero)


class A_bandit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((A_BANDIT_WIDTH, A_BANDIT_HEIGHT))
        self.image.fill(pygame.Color(A_BANDIT_COLOR))
        self.rect = pygame.Rect(x, y, A_BANDIT_WIDTH, A_BANDIT_HEIGHT)

        self.type = 'A_bandit'

        self.startx = x
        self.starty = y


class B_bandit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((B_BANDIT_WIDTH, B_BANDIT_HEIGHT))
        self.image.fill(pygame.Color(B_BANDIT_COLOR))
        self.rect = pygame.Rect(x, y, B_BANDIT_WIDTH, B_BANDIT_HEIGHT)

        self.type = 'B_bandit'

        self.startx = x
        self.starty = y
