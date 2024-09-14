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

from models.meteor import Meteor, meteor_list
from models.nave import Nave 

# Crear el grupo de todos los sprites y añadir los meteoros
all_sprites = pygame.sprite.Group()
for meteor in meteor_list:
    all_sprites.add(meteor)

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

    # Actualizar los sprites
    all_sprites.update()

    # Dibujar en pantalla
    screen.blit(background, [0, 0])  
    all_sprites.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()