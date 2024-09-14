import pygame

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Configurar la pantalla de Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption('Shooter')
clock = pygame.time.Clock()

# Cargar la imagen de fondo
background = pygame.image.load('assets/background.png').convert()
# Cargar sonido de explosión 
explosion_sound = pygame.mixer.Sound('assets\explosion_sound.wav')
explosion_sound.set_volume(0.15)


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.sysfont.match_font('serif'), size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

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

# Marcador - cargar y reproducir música de fondo
score = 0
pygame.mixer.music.load('assets\game_sound.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

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
        score += 10
        explosion_sound.play()
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

    draw_text(screen, f"Score: {score}", 30, WIDTH // 2, 10)

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)


pygame.quit() 

