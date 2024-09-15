import pygame

WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Configurar la pantalla de Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shooter Game')
clock = pygame.time.Clock()

# Cargar la imagen de fondo
background = pygame.image.load('assets/background.jpg').convert()
# Cargar sonido de explosión
explosion_sound = pygame.mixer.Sound('assets\explosion_sound.wav')
explosion_sound.set_volume(0.15)

from models.nave import Nave
from models.meteor import Meteor
from models.bullet import Bullet
from models.recover_life import Recover_life
from models.collision import Collision

# Función para dibujar texto en pantalla
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.sysfont.match_font('serif'), size)
    text_surface = font.render(text, True, WHITE)
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
    pygame.draw.rect(surface, WHITE, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

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

# Función para manejar el menu del juego
def game_over_menu(score):
    screen.blit(background, (0, 0))
    draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, f"Score: {score}", 44, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press R to Restart or Q to Quit", 22, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    run_game()  # Reiniciar el juego
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
#Función para mostrar la pantalla de inicio
def show_start_screen():
    screen.blit(background, (0, 0))
    draw_text(screen, "SHOOTER GAME", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press SPACE to Start", 22, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press P to Paused", 22, WIDTH // 2, HEIGHT // 1.8)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
# Función para pausar el juego
def pause_game():
    draw_text(screen, "PAUSED", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press P to Resume", 22, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

# Función principal para ejecutar el juego
def run_game():
    global all_sprites, bullets, meteor_list, Collision_list, life_list, nave, score

    # Creación de todos los sprites
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    meteor_list = pygame.sprite.Group()
    Collision_list = pygame.sprite.Group()
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
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    nave.shoot(all_sprites, bullets)
                elif event.key == pygame.K_p:
                    pause_game()

        # Actualizar los sprites
        all_sprites.update()

        # Colisiones entre las balas y los meteoros
        hits = pygame.sprite.groupcollide(bullets, meteor_list, True, True)
        for hit in hits:
            score += 10
            explosion_sound.play()
            collision = Collision(hit.rect.center)
            all_sprites.add(collision)
            add_meteor()

        # Colisiones entre la nave y los meteoros
        hits = pygame.sprite.spritecollide(nave, meteor_list, True)
        for hit in hits:
            nave.life -= 20
            add_meteor()
            if nave.life <= 0:
                running = False
    
        # Colisiones entre la nave y los objetos de vida
        hits = pygame.sprite.spritecollide(nave, life_list, True)
        for hit in hits:
            nave.life += 20  
            if nave.life > 100:
                nave.life = 100 

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

    game_over_menu(score) 

show_start_screen() # Mostrar la pantalla de inicio

run_game() # Ejecutar el juego
