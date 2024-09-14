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

from models.nave import Nave
from models.meteor import Meteor
from models.bullet import Bullet
from models.recover_life import Recover_life

# Función para dibujar texto en pantalla
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.sysfont.match_font('serif'), size)
    text_surface = font.render(text, True, RED)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Función para dibujar la barra de vida
def draw_life_bar(surface, x, y, percent_life):
    if percent_life < 0:
        percent_life = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent_life / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, RED, fill_rect)
    pygame.draw.rect(surface, RED, outline_rect, 2)

# Función para añadir un nuevo meteoro
def add_meteor():
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

# Función para añadir un nuevo objeto de vida
life_timer = 0
life_interval = 5000

def add_life():
    global life_timer
    life_timer += clock.get_time()
    if life_timer >= life_interval:
        life = Recover_life()
        all_sprites.add(life)
        life_list.add(life)
        life_timer = 0

# Creación de todos los sprites
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
life_list = pygame.sprite.Group()
for _ in range(8):
    add_meteor()


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
        add_meteor()

    # Colisiones entre la nave y los meteoros
    hits = pygame.sprite.spritecollide(nave, meteor_list, True)
    for hit in hits:
        nave.life -= 20
        add_meteor()
        print(f"Vida de la nave: {nave.life}")
        if nave.life <= 0:
            running = False
    
     # Colisiones entre la nave y los objetos de vida
    hits = pygame.sprite.spritecollide(nave, life_list, True)
    for hit in hits:
        nave.life += 20  
        if nave.life > 100:
            nave.life = 100  
        print(f"Vida de la nave: {nave.life}")

    add_life() 

    # Dibujar en pantalla
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Dibujar la barra de vida
    draw_life_bar(screen, WIDTH // 2 - 50, 40, nave.life)

    # Dibujar el texto de la vida debajo de la barra de vida
    draw_text(screen, f"Life: {nave.life}", 20, WIDTH // 2, 55)  

    # Dibujar el puntaje
    draw_text(screen, f"Score: {score}", 30, WIDTH // 2, 10)


    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
