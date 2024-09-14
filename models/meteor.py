import pygame
import random

# Variables globales
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)


class Meteor(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -35 or self.rect.right > WIDTH + 35:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

meteor_images = []
meteor_list = ['assets\meteor_tiny_1.png', 'assets\meteor_tiny_2.png',
                'assets\meteor_small_1.png', 'assets\meteor_small_2.png',
                  'assets\meteor_medium_1.png', 'assets\meteor_medium_2.png', 
                  'assets\meteor_big_1.png', 'assets\meteor_big_2.png', 'assets\meteor_big_3.png', 'assets\meteor_big_4.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())