import pygame
import time
import random
import sys
from menu import Button

# Para inicializar todos los modulos de pygame
pygame.init()
WIDTH, HEIGHT = 900, 500

velocidad = 15

# Fondo de menu inicial
fondo = pygame.image.load('Imagenes/fondo.jpg')

# Definiendo colores del juego
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Tamano de la ventana del juego
VENTANA = pygame.display.set_mode((WIDTH, HEIGHT))

# Frames per second
fps = pygame.time.Clock()

# Tamano y posicion inicial del snake
snake_ubicacion = [100, 50]

# El cuerpo del snake, el primer bloque va a 
# ser igual que la ubicacion inicial
snake_cuerpo = [  [100, 50],
                [90, 50],
                [80, 50],
                [70, 50]
                ]

# Puntaje inicial
puntaje = 0

def get_font(size):
    return pygame.font.SysFont('Cambria', size)

# Funcion para el puntaje del usuario durante la partida
def show_score(choice, color):
    # Definiendo tipo de letra y tamano del puntaje
    puntaje_estilo = get_font(30)

    # Para ensenar cantidad de puntos   REVISAR
    puntaje_msj = puntaje_estilo.render('Puntaje : ' + str(puntaje), True, color)

    # Cuadro para ensenar texto     REVISAR
    puntaje_cuadro = puntaje_msj.get_rect()

    # Mostrar msj de puntaje    REVISAR
    VENTANA.blit(puntaje_msj, puntaje_cuadro)


# Funcion para pantalla de perdida
def game_over():
    
    # Estilo de letra
    estilo_perdida = get_font(50)

    # Texto a generar   REVISAR
    texto_perdida = estilo_perdida.render('Su puntaje es de : ' + str(puntaje), True, white)

    # Cuadro para ensenar texto
    perdida_cuadro = texto_perdida.get_rect()

    # Ubicacion del cuadro
    perdida_cuadro.midtop = (WIDTH/2, HEIGHT/4)

    # Para mostrar texto    REVISAR
    VENTANA.blit(texto_perdida, perdida_cuadro)

    # Mandar al menu cuando pierde
    # main_menu()



# Funcion para llamar y empezar el juego
def juego():
    global puntaje

    # Posicion (x, y) de la comida (aleatorio) 
    # // se usa para floor division
    ubicacion_fruta = [random.randrange(1, (WIDTH//10)) * 10,
                    random.randrange(1, (HEIGHT//10)) * 10]

    nacimiento_fruta = True

    # Direccion inicial del snake
    direccion = 'RIGHT'
    change_to = direccion

    while True:

        # Manejando eventos para determinar inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Para que no se mueva en 2 direcciones
        if change_to == 'UP' and direccion != 'DOWN':
            direccion = 'UP'
        if change_to == 'DOWN' and direccion != 'UP':
            direccion = 'DOWN'
        if change_to == 'LEFT' and direccion != 'RIGHT':
            direccion = 'LEFT'
        if change_to == 'RIGHT' and direccion != 'LEFT':
            direccion = 'RIGHT'

        # Control de movimiento
        if direccion == 'UP':
            snake_ubicacion[1] -= 10
        if direccion == 'DOWN':
            snake_ubicacion[1] += 10
        if direccion == 'LEFT':
            snake_ubicacion[0] -= 10
        if direccion == 'RIGHT':
            snake_ubicacion[0] += 10

        # Mecanismo para crecimiento despues de comer
        snake_cuerpo.insert(0, list(snake_ubicacion))
        if snake_ubicacion[0] == ubicacion_fruta[0] and snake_ubicacion[1] == ubicacion_fruta[1]:
            puntaje += 10
            nacimiento_fruta = False
        else:
            snake_cuerpo.pop()
            
        if not nacimiento_fruta:
            ubicacion_fruta = [random.randrange(1, (WIDTH//10)) * 10,
                            random.randrange(1, (HEIGHT//10)) * 10]
            
        nacimiento_fruta = True
        VENTANA.fill(black)

        for pos in snake_cuerpo:
            pygame.draw.rect(VENTANA, green, pygame.Rect(
            pos[0], pos[1], 10, 10))
            
        pygame.draw.rect(VENTANA, white, pygame.Rect(
        ubicacion_fruta[0], ubicacion_fruta[1], 10, 10))
        
        # Condiciones cuando se sale del area de juego
        if snake_ubicacion[0] < 0 or snake_ubicacion[0] > WIDTH-10:
            game_over()
        if snake_ubicacion[1] < 0 or snake_ubicacion[1] > HEIGHT-10:
            game_over()
        
        # Game over cuando el snake se toca a si mismo
        for block in snake_cuerpo[1:]:
            if snake_ubicacion[0] == block[0] and snake_ubicacion[1] == block[1]:
                game_over()
        
        # Mostrar puntaje de forma continua
        show_score(1, white)
        
        # Actualizando la pantalla
        pygame.display.update()
    
        # Frame Per Second / Refresh Rate
        fps.tick(velocidad)

# Funcion para menu inicial
def main_menu():
    while True:
        VENTANA.blit(fondo, (50, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, white)
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 100))

        boton1 = pygame.image.load("Imagenes/boton.png")
        boton1 = pygame.transform.scale(boton1, (300, 100))  # Cambio de tamano del boton

        # Boton para jugar
        PLAY_BUTTON = Button(boton1, pos=(450, 200), 
                            text_input="Iniciar", font=get_font(75), base_color=white, hovering_color=black)

        # Boton para salir
        QUIT_BUTTON = Button(boton1, pos=(450, 300), 
                            text_input="Salir", font=get_font(75), base_color=white, hovering_color=black)

        VENTANA.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(VENTANA)
        
        # Que pasa cuando se toca alguno de los 2 botones
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    juego()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

