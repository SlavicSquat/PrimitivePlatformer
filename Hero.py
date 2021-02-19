from pygame.sprite import Sprite
from pygame import Surface
import pygame

MOVE_SPEED = 10
WIDTH = 30
HEIGHT = 70
COLOR = (0, 100, 0)
JUMP_POWER = 10
GRAVITY = 0.35

ANIM_LEFT = [pygame.image.load(r'data\sprites\Hero\Hero_left_0.png'),
             pygame.image.load(r'data\sprites\Hero\Hero_left_1.png'),
             pygame.image.load(r'data\sprites\Hero\Hero_left_2.png')]
ANIM_RIGHT = [pygame.image.load(r'data\sprites\Hero\Hero_right_0.png'),
              pygame.image.load(r'data\sprites\Hero\Hero_right_1.png'),
              pygame.image.load(r'data\sprites\Hero\Hero_right_2.png')]
ANIM_STANCE = [pygame.image.load(r'data\sprites\Hero\Hero_stance_l.png'),
               pygame.image.load(r'data\sprites\Hero\Hero_stance_r.png')]
walk_left = False
walk_right = True
ANIM_COUNT = 0
ANIM_FPS = 10


class Hero(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR)
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.startx = x
        self.starty = y
        self.xvel = 0
        self.yvel = 0
        self.onGround = False

    def collide(self, xvel, yvel, platforms, f_p, enemies):
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

        for p in f_p:
            if pygame.sprite.collide_rect(self, p):
                p.image.set_alpha(0)
                f_p.remove(p)

        for enemy in enemies:
            if pygame.sprite.collide_rect(self, enemy):
                self.rect.x = self.startx
                self.rect.y = self.starty

    def update(self, left, right, jump, platforms, f_p, enemies):
        #global ANIM_COUNT, walk_right, walk_left
        #if ANIM_COUNT >= 29:
        #    ANIM_COUNT = 0
        #self.image.set_colorkey(COLOR)

        if jump:
            if self.onGround:
                self.yvel = -JUMP_POWER
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel

        if left:
            self.xvel = -MOVE_SPEED
            #walk_right = False
            #walk_left = True
            #self.image = ANIM_LEFT[ANIM_COUNT // ANIM_FPS]
            #ANIM_COUNT += 1
        if right:
            self.xvel = MOVE_SPEED
            #walk_right = True
            #walk_left = False
            #self.image = ANIM_RIGHT[ANIM_COUNT // ANIM_FPS]
            #ANIM_COUNT += 1
        if not(left or right):
            self.xvel = 0
            #if walk_right:
            #    self.image = ANIM_STANCE[1]
            #elif walk_left:
            #    self.image = ANIM_STANCE[0]

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, f_p, enemies)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, f_p, enemies)





