#!/usr/bin/python3
import pygame
import random
import sys
from menu import Button


def get_font(size):
    '''
    Encargado de llamar el estilo de letra.

    parametros:
        size (int): Define el tamano de la letra
    '''
    return pygame.font.SysFont('Cambria', size)


def show_score(color, puntaje):
    '''
    Asigna el color, tamano y ubicacion de las letas para el puntaje.

    parametros:
        color (tuple): Color del font en formato RGB.
        puntaje (int): Puntaje del usuario de la partida.
    '''
    # Definiendo tipo de letra y tamano del puntaje
    puntaje_estilo = get_font(30)

    # Para ensenar cantidad de puntos   REVISAR
    puntaje_msj = puntaje_estilo.render('Puntaje : '
                                        + str(puntaje), True, color
                                        )

    # Cuadro para ensenar texto     REVISAR
    puntaje_cuadro = puntaje_msj.get_rect()

    # Mostrar msj de puntaje    REVISAR
    VENTANA.blit(puntaje_msj, puntaje_cuadro)


def tiempo(seg=0, min=0):
    '''
    Encargado de mostrar el tiempo de la partida.

    parametros:
        seg (int): Segundos de la partida.
        min (int): Minutos de la partida.
    '''
    # Reloj de tiempo durante la partida (solo se incluye min y seg)
    font = get_font(30)
    texto = font.render('{}:{:.2f}'.format(min, seg), True, white)
    textoRect = texto.get_rect()
    textoRect.center = (WIDTH // 2, 10)

    VENTANA.blit(texto, textoRect)


def juego(seg, min, snake_ubicacion=[100, 50],
          snake_cuerpo=[[100, 50], [90, 50], [80, 50], [70, 50]], puntaje=0
          ):
    '''
    Establece la logica del juego y determina el
    tiempo y puntaje cuando se pierde.

    parametros:
        seg (int): Segundos de la partida.
        min (int): Minutos de la partida.
        snake_ubicacion (list): ubicacion del snake (el valor
        predeterminado es la ubicacion inicial).
        snake_cuerpo (list): Define el cuerpo de la culebra.
        puntaje (int): Puntaje del usuario de la partida.
    '''

    # Posicion (x, y) de la comida (aleatorio)
    ubicacion_fruta = [random.randrange(1, (WIDTH // 10)) * 10,
                       random.randrange(1, (HEIGHT // 10)) * 10]

    nacimiento_fruta = True

    # Direccion inicial del snake
    direccion = 'RIGHT'
    change_to = direccion
    
    while True:

        # Manejando eventos para determinar inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        if (snake_ubicacion[0] == ubicacion_fruta[0] and
            snake_ubicacion[1] == ubicacion_fruta[1]):
            sound1.play()
            puntaje += 10
            nacimiento_fruta = False
            
        else:
            snake_cuerpo.pop()

        if not nacimiento_fruta:
            ubicacion_fruta = [random.randrange(1, (WIDTH // 10)) * 10,
                               random.randrange(1, (HEIGHT // 10)) * 10]

        nacimiento_fruta = True
        VENTANA.fill(black)

        for pos in snake_cuerpo:
            pygame.draw.rect(VENTANA, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(VENTANA, white, pygame.Rect
                         (ubicacion_fruta[0], ubicacion_fruta[1], 10, 10))

        # Perder cuando se toca la parte vertical
        if snake_ubicacion[0] < 0 or snake_ubicacion[0] > WIDTH-10:
            snake_cuerpo = [
                            [100, 50],
                            [90, 50],
                            [80, 50],
                            [70, 50]
                            ]
            tiempo_gameover = texto
            main_menu(False, tiempo_gameover, puntaje)
        # Perder cuando se toca la parte horizontal
        if snake_ubicacion[1] < 0 or snake_ubicacion[1] > HEIGHT-10:
            snake_cuerpo = [
                    [100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]
                    ]
            tiempo_gameover = texto
            main_menu(False, tiempo_gameover, puntaje)

        # Game over cuando el snake se toca a si mismo
        for block in snake_cuerpo[1:]:
            if (snake_ubicacion[0] == block[0] and
                    snake_ubicacion[1] == block[1]):
                snake_cuerpo = [
                                [100, 50],
                                [90, 50],
                                [80, 50],
                                [70, 50]
                                ]
                tiempo_gameover = texto
                main_menu(False, tiempo_gameover, puntaje)

        # Mostrar puntaje de forma continua
        show_score(white, puntaje)

        # Frames per second
        fps = pygame.time.Clock()

        # Reloj para contar tiempo
        reloj = fps.tick(velocidad)
        # Contar el tiempo de cada iteracion y convertirlo
        # a segundos basado en el valor de reloj
        seg += reloj / 1000
        if seg >= 60:
            seg = 0
            min += 1
        texto = get_font(30).render('{}:{:.2f}'.format(min, seg), True, white)
        tiempo(seg, min)
        # Actualizando la pantalla
        pygame.display.update()


def main_menu(partida1, tiempo_gameover=0, puntaje=0):
    '''
    Menu principal del juego y tambien pantalla de perdida.

    parametros:
        partida1 (bool): Determina se es la primera partida o no.
        tiempo_gameover (int): Tiempo desde que inicia la
        partida hasta que finaliza.
        puntaje (int): Puntaje del usuario de la partida.
    '''
    # Fondo de menu inicial
    fondo = pygame.image.load('Imagenes/fondo.jpg')

    
    while True:
        VENTANA.blit(fondo, (0, 0))
        # Estilo de letra
        estilo_perdida = get_font(30)

        # Para determinar si hay que mostrar el puntaje/tiempo o no
        if (partida1 is False):
            # Texto a generar
            texto_perdida = estilo_perdida.render(
                'Su puntaje de la partida pasada '
                'es de: ' + str(puntaje), True, white
                )
            # Cuadro para mover el texto
            perdida_cuadro = texto_perdida.get_rect()
            # Ubicacion del cuadro
            perdida_cuadro.center = (450, 400)
            VENTANA.blit(texto_perdida, perdida_cuadro)

            # Mostrar tiempo despues de primera partida
            msj_tiempo = estilo_perdida.render(
                "Su tiempo de la partida anterior es: ", True, white
                )
            tiempo_cuadro = msj_tiempo.get_rect()
            tiempo_cuadro.center = (450, 440)
            VENTANA.blit(msj_tiempo, tiempo_cuadro)

            # Cuadro para mover el texto
            texto_tiempo = tiempo_gameover.get_rect()
            # Ubicacion del cuadro
            texto_tiempo.center = (450, 460)
            # Para mostrar texto
            VENTANA.blit(tiempo_gameover, texto_tiempo)

        # Ubicacion del mouse
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, white)
        MENU_RECT = MENU_TEXT.get_rect(center=(450, 100))

        boton1 = pygame.image.load("Imagenes/boton.png")
        boton1 = pygame.transform.scale(boton1, (300, 100))  # Cambio
        # de tamano del boton

        # Boton para jugar
        PLAY_BUTTON = Button(boton1, pos=(450, 200),
                             text_input="Iniciar", font=get_font(75),
                             base_color=white, hovering_color=black)

        # Boton para salir
        QUIT_BUTTON = Button(boton1, pos=(450, 300),
                             text_input="Salir", font=get_font(75),
                             base_color=white, hovering_color=black)

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
                    juego(0, 0, snake_ubicacion=[100, 50],
                          snake_cuerpo=[
                          [100, 50], [90, 50], [80, 50], [70, 50]
                          ]
                          )
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    # Para inicializar todos los modulos de pygame
    pygame.init()
    WIDTH, HEIGHT = 900, 500

    # Velocidad del snake
    velocidad = 15

     # Musica del menu y sonidos
    pygame.mixer.music.load('Sonidos/musicintro.wav')
    pygame.mixer.music.play(3)
    sound1 = pygame.mixer.Sound('Sonidos/bite.wav')

    # Definiendo colores para usar (RGB)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    green = pygame.Color(0, 255, 0)

    # Tamano de la ventana del juego
    VENTANA = pygame.display.set_mode((WIDTH, HEIGHT))

    # Tamano y posicion inicial del snake
    snake_ubicacion = [100, 50]

    # Para saber que es la primera partida
    partida1 = True

    # El cuerpo del snake, el primer bloque va a
    # ser igual que la ubicacion inicial
    snake_cuerpo = [
                    [100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]
                    ]

    # Llamando funcion de menu principal para iniciar
    main_menu(partida1)
