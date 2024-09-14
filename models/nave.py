import pygame
from models.bullet import Bullet

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Nave(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/nave.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.life = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, all_sprites, bullets):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet) 
        bullets.add(bullet)
        bullet_sound.play()

# Cargar sonido disparo
bullet_sound = pygame.mixer.Sound('assets/laser_sound.ogg')
bullet_sound.set_volume(0.15)


