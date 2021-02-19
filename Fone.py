import pygame


class Fone(pygame.sprite.Sprite):
    def __init__(self, FONE_PATH):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(FONE_PATH)
        self.image = pygame.transform.scale(self.image, (2970, 780))
        self.rect = pygame.Rect(30, 30, 2970, 820)
