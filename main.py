import pygame

WIDTH = 800
HEIGHT = 600

# Inicializar Pygame
pygame.init()

# Configurar la pantalla de Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption('Shooter')
clock = pygame.time.Clock()

# Cargar la imagen de fondo
background = pygame.image.load('assets/background.png').convert()

from models.meteor import Meteor
from models.nave import Nave 
from models.bullet import Bullet

# Creación de todos los sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
for _ in range(8): 
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

# Creación de la instancia Nave y añadirla al grupo de todos los sprites
nave = Nave()
all_sprites.add(nave)

# Bucle principal
running = True
while running:
    clock.tick(60)
    
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nave.shoot(all_sprites, bullets)

    # Actualizar los sprites
    all_sprites.update()

     # Colisiones entre las balas y los meteoros
    hits = pygame.sprite.groupcollide(bullets, meteor_list, True, True)
    for hit in hits:
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # Colisiones entre la nave y los meteoros
    hits = pygame.sprite.spritecollide(nave, meteor_list, False)
    if hits:
        running = False

    # Dibujar en pantalla
    screen.blit(background, [0, 0])  
    all_sprites.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)


pygame.quit() 