import pygame
import random

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)

class Recover_life(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/recover_life2.png').convert()
        self.image.set_colorkey((BLACK))  
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)
            self.speedx = random.randrange(-5, 5)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx