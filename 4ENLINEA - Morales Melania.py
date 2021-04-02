

#-----------------------------Variables globales-----------------------------
import numpy as np
import pygame
import math
import sys
import random
import copy
#-----------------------------Varios-----------------------------
#E: una matriz
#S: una matriz
#D: retorna la matriz girada en la direccion derecha

def girarMatrizDer (matriz, res=[]):
    for i in range (0,len(matriz[0])):
        lineaNueva=[]
        for j in range (0,len(matriz)):
            lineaNueva=[matriz[j][i]]+lineaNueva
        res=res+[lineaNueva]
        lineaNueva=[]
    return res

matriz=([[0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]])
nuevaMatriz = []
game_over= False
game_over2 = False
turno = 0
turno2 = 0
partidasGuardadas=[]

#-------------------------Contadores desplazamiento------------------------
contadorDer=0
contadorAr=0
#-------------------------Jugadores y puntuaciones------------------------
nombreJ1=""
nombreJ2=""
puntuacionJ1=0
puntuacionJ2=0
listadoPuntuaciones=[]
#--------------------------------Colores----------------------------------
AZUL=(0,0,255)
NEGRO=(0,0,0)
CYAN= (255,0,255)
VERDE= (0,255,0)
ROJO= (255, 0, 0)
WHITE= (255,255,255)
#-----------------------------Índices Lógicos Interfaz-----------------------------
indicesAImprimirFila=[1,2, 3, 4, 5, 6]
indicesAImprimirColumna=[1, 2, 3, 4, 5, 6, 7]
#-----------------------------Índices Intefaz-----------------------------
indiceEnPantallaCol=0
indiceEnPantallaFila=0
#-----------------------------Carga de Archivos-----------------------------
partidaGuardaCarga=[]

# D: Metodo para grabar un mapa en el archivo
# E: El path del archivo, un string con formato de lista
# S: Ninguna

def guardar (archivo, strLista):
        fo = open(archivo, "w")
        fo.write(strLista)
        fo.close()

# D: Metodo para leer una archivo
# E: El path del archivo
# S: Un string con el contenido del archivo

def leer (archivo):
        fo = open(archivo, "r")            
        resultado = fo.read()
        fo.close()
        return resultado

# D: Cargar archivo
# E: Lee un archivo y hace las validaciones para colocarlo en la lista
# S: Retorna una lista de lo leido

def cargarArchivo(archivo):
        strResultado = leer(archivo)
        if strResultado != "":
                return eval(strResultado)
        else:
                return []

#-----------------------------Creación de la Matriz Infinita-----------------------------
#E: ninguna
#S: ninguna, solo actualiza la matriz
#D: dada la matriz original la actualiza como la matriz resultante de crecer 7 espacios hacia la derecha
            
def crearMatrizNuevaDer ():
    global matriz,indiceEnPantallaCol
    nuevaMatriz=np.zeros((len(matriz),7),dtype = np.int)
    matriz=np.concatenate((matriz,nuevaMatriz),axis=1)
    indiceEnPantallaCol+=7
    cuadroDeJuego(matriz)
    indicesActDerechaC ()

#E: ninguna
#S: ninguna, solo actualiza la matriz
#D: dada la matriz original la actualiza como la matriz resultante de crecer 7 espacios hacia la izquierda
    
def crearMatrizNuevaIzq ():
    global matriz,indiceEnPantallaCol
    nuevaMatriz=np.zeros((len(matriz),7),dtype = np.int)
    matriz=np.concatenate((nuevaMatriz,matriz),axis=1)
    indiceEnPantallaCol=0
    cuadroDeJuego(matriz)
    indicesActIzquierdaC ()
    
#E: ninguna
#S: ninguna, solo actualiza la matriz
#D: dada la matriz original la actualiza como la matriz resultante de crecer 6 espacios hacia la arriba
    
def creceHaciaArriba ():
    global matriz,indiceEnPantallaFila
    nuevaMatriz=np.zeros((6,len(matriz[0])),dtype = np.int)
    matriz=np.vstack((nuevaMatriz,matriz))
    cuadroDeJuego(matriz)
    indicesActArriba()

#E: la matriz y el indice de columna donde desea preguntar
#S: bool, True or False
#D: dada la matriz averigua si la columna donde el jugador desea colocar la ficha esta llena o no
def columnaLlena (matriz,col):
    for i in range (0,len(matriz)-1):
        if matriz[i][col]==0:
            return False
    return True
#-----------------------------Movimiento en la Matriz Infinita-----------------------------

#E: ninguna
#S: ninguna, solo actualiza los índices para poder moverse
#D: dado el indice de las columnas revisa la posicion en la que se encuentra y se mueve entres las ventanas disponibles
    
def moverDerecha ():
    global matriz,indiceEnPantallaCol
    indiceEnPantallaCol+=7
    indicesActDerechaC ()
    if indiceEnPantallaCol<len(matriz[0]):
        cuadroDeJuego(matriz)
        fichasEnTablero (matriz)
    else:
        indiceEnPantallaCol=indiceEnPantallaCol-7
        indicesActIzquierdaC ()

#E: ninguna
#S: ninguna, solo actualiza los índices para poder moverse
#D: dado el indice de las columnas revisa la posicion en la que se encuentra y se mueve entres las ventanas disponibles
        
def moverIzquierda ():
    global matriz,indiceEnPantallaCol
    indiceEnPantallaCol=indiceEnPantallaCol-7
    indicesActIzquierdaC ()
    if indiceEnPantallaCol>=0:
        cuadroDeJuego(matriz)
        fichasEnTablero (matriz)
    else:
        indiceEnPantallaCol+=7
        indicesActDerechaC ()

#E: ninguna
#S: ninguna, solo actualiza los índices para poder moverse
#D: dado el indice de las filas revisa la posicion en la que se encuentra y se mueve entres las ventanas disponibles
        
def moverArriba ():
    global matriz,indiceEnPantallaFila
    indiceEnPantallaFila=indiceEnPantallaFila-6
    indicesActArriba()
    if indiceEnPantallaFila>=0:
        cuadroDeJuego(matriz)
        fichasEnTablero (matriz)
    else:
        indiceEnPantallaFila=indiceEnPantallaFila+6
        indicesActAbajo()
    cuadroDeJuego(matriz)
    fichasEnTablero (matriz)

#E: ninguna
#S: ninguna, solo actualiza los índices para poder moverse
#D: dado el indice de las filas revisa la posicion en la que se encuentra y se mueve entres las ventanas disponibles
    
def moverAbajo ():
    global matriz,indiceEnPantallaFila
    indiceEnPantallaFila=indiceEnPantallaFila+6
    indicesActAbajo()
    if indiceEnPantallaFila<len(matriz):
        cuadroDeJuego(matriz)
        fichasEnTablero (matriz)
    else:
        indiceEnPantallaFila=indiceEnPantallaFila-6
        indicesActArriba()

#-------------------------IndicesEnMatriz----------------------
pygame.font.init ()
myfont3 = pygame.font.SysFont("agencyfb", 20)

#FILAS

#E: ninguna
#S: ninguna, solo actualiza los índices que muestra en pantalla al moverse hacia arriba
#D: al moverse o crecer hacia arriba los indices que se muestran en pantalla son actualizados

def indicesActArriba(): 
     global indicesAImprimirFila
     listaSuma = []

     for num in indicesAImprimirFila:

          listaSuma += [num+6]


     indicesAImprimirFila = listaSuma
     return

#E: ninguna
#S: ninguna, solo actualiza los índices que muestra en pantalla al moverse hacia arriba
#D: al moverse hacia abajo los indices que se muestran en pantalla son actualizados

def indicesActAbajo():
     global indicesAImprimirFila
     listaResta = []

     for num in indicesAImprimirFila:


          listaResta += [num-6]

     indicesAImprimirFila = listaResta
     return

#COLUMNAS

#E: ninguna
#S: ninguna, solo actualiza los índices que muestra en pantalla al moverse hacia arriba
#D: al moverse o crecer hacia la derecha los indices que se muestran en pantalla son actualizados
    
def indicesActDerechaC(): 
     global indicesAImprimirColumna
     listaSuma = []

     for num in indicesAImprimirColumna:

          listaSuma += [num+7]


     indicesAImprimirColumna = listaSuma


#E: ninguna
#S: ninguna, solo actualiza los índices que muestra en pantalla al moverse hacia arriba
#D: al moverse o crecer hacia la izquierda los indices que se muestran en pantalla son actualizados
     
def indicesActIzquierdaC():
     global indicesAImprimirColumna
     listaResta = []

     for num in indicesAImprimirColumna:


          listaResta += [num-7]

     indicesAImprimirColumna = listaResta

#IMPRESION
     
#E: ninguna
#S: imprime los indices en pantalla
#D: toma la global de indices de las filas y los imprime en pantalla
     
def imprimirIndicesFilas():

     global indicesAImprimirFila
     coordX = 715
     coordY = 635

     for num in indicesAImprimirFila:
        
        label1 =  myfont2.render((str(num)), 1, WHITE)
        screen.blit(label1,(coordX,coordY))
        
        coordY -= 100
        
#E: ninguna
#S: imprime los indices en pantalla
#D: toma la global de indices de las columnas y los imprime en pantalla

def imprimirIndicesColumnas():

     global indicesAImprimirColumna
     coordX = 10
     coordY = 97

     for num in indicesAImprimirColumna:
        
        label1 =  myfont3.render((str(num)), 1, WHITE)
        screen.blit(label1,(coordX,coordY))
        
        coordX += 100

#---------------------------Validación de espacio en matriz y colocación de ficha-----------------------------
#E: un número entero
#S: bool, True or False
#D: retorna True si el espacio [i][j] de la matriz según la columna dada tal que j=columna está vacío, es decir, en 0. De no ser así
#   retorna False
    
def espacioVacio (col):
    global matriz
    if matriz [len(matriz)-1][col]==0:
        return True
    else:
        return False

#E: un número entero
#S: un número entero
#D: dado el número de columna tal que [i][j] con j = columna busca la ficha vacía más cercana para colocar la ficha según dicha columna

def colocaEnFila (col):
    global matriz
    largo=len(matriz)-1
    while largo>=0: 
        if matriz [largo][col]==0:
            return largo
        largo=largo-1
        
#E: 3 números enteros
#S: ninguna, simplemente actualiza la matriz
#D: dado el número de fila, columna y ficha actualiza la matriz en esa posicion al número de ficha dado

def colocaFicha (matriz,fila,col,ficha): #NECESITA TENER MATRIZ COMO PARAMETRO SI O SI CAMBIAR ESO EN EL RESTO DEL CODIGO
    matriz[fila][col]=ficha

#-----------------------------Condiciones del gane del jugador-----------------------------
#E: un número entero
#S: un bool, True or False
#D: dada una ficha revisa si en algún lugar de la matriz hay 4 fichas seguidas que se consideran como un gane (horizaontales,
#   verticales, diagonal drecha y diagonal izquierda)

def ganeDeJugador (ficha):
    global matriz
    for i in range(0,len(matriz[0])-3): #gane horizontal
        for j in range(0,len(matriz)):
            if matriz [j][i] == ficha and matriz [j][i+1] == ficha and matriz [j][i+2] == ficha and matriz [j][i+3] == ficha:
                return True
    for i in range(0,len(matriz[0])): #gane vertical
        for j in range(0,len(matriz)-3):
            if matriz [j][i] == ficha and matriz [j+1][i] == ficha and matriz [j+2][i] == ficha and matriz [j+3][i] == ficha:
                return True
    for i in range(0,len(matriz[0])-3): #gane diagonal derecha
        for j in range(0,len(matriz)-3):
            if matriz [j][i] == ficha and matriz [j+1][i+1] == ficha and matriz [j+2][i+2] == ficha and matriz [j+3][i+3] == ficha:
                return True
    for i in range(0,len(matriz)-3): #gane diagonal izquierda
        for j in range(3,len(matriz[0])):
            if matriz [i][j] == ficha and matriz [i+1][j-1] == ficha and matriz [i+2][j-2] == ficha and matriz [i+3][j-3] == ficha:
                return True
    return False

#-----------------------------Dibujo de tablero y sus fichas-----------------------------

#E: una matriz
#S: dibujo en pantalla según parámetros
#D: dada una matriz la utiliza para dibujar el tablero de nuestro juego

def cuadroDeJuego (matriz):
    for i in range(7):
        for j in range (7):
            pygame.draw.rect(screen, AZUL,(i*SQUARESIZE,j*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,NEGRO,(int(i*SQUARESIZE+SQUARESIZE/2),int(j*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),radio)

#E: una matriz
#S: colocación de las fichas en pantalla según parámetros
#D: dado una matriz coloca una ficha de un color u otro dependiendo a los números que haya dentro de ella
            
def fichasEnTablero (matriz):
    global indiceEnPantallaCol,indiceEnPantallaFila
    for i in range(indiceEnPantallaCol,(indiceEnPantallaCol+7)):
        for j in range(indiceEnPantallaFila,(indiceEnPantallaFila+6)):
            if matriz[j][i] == 1:
                pygame.draw.circle(screen, CYAN, (int((i-indiceEnPantallaCol)*SQUARESIZE+SQUARESIZE/2), 150+100*(j-indiceEnPantallaFila)),radio)
                print((int(i*SQUARESIZE+SQUARESIZE/2), 150+100*j))
            elif matriz[j][i] == 2:
                pygame.draw.circle(screen, VERDE, (int((i-indiceEnPantallaCol)*SQUARESIZE+SQUARESIZE/2), 150+100*(j-indiceEnPantallaFila)),radio)
                print((int(i*SQUARESIZE+SQUARESIZE/2), 150+100*j))
    pygame.display.update()


#-----------------------------Puntuaciones y Ranking-----------------------------

#E: un string
#S: atualizacion del archivo "listaPuntuaciones.txt"
#D: toma el string del nombre del jugador ganador y busca en la lista de puntuaciones si ya habia jugado para sumarle un punto,
#   de no ser asi lo añade a la lista y le suma un punto
    
def listaConPuntuaciones (ganador):
    global listadoPuntuaciones
    listadoPuntuaciones=cargarArchivo("listaPuntuaciones.txt")
    if listadoPuntuaciones==[]:
        listadoPuntuaciones+=[[ganador,1]]
        guardar("listaPuntuaciones.txt", str(listadoPuntuaciones))
    else:
        for i in range (0,len(listadoPuntuaciones)):
            if listadoPuntuaciones [i][0]==ganador:
                listadoPuntuaciones[i]=[ganador, listadoPuntuaciones[i][1]+1]
                guardar("listaPuntuaciones.txt", str(listadoPuntuaciones))
                return
        listadoPuntuaciones+=[[ganador,1]]
        guardar("listaPuntuaciones.txt", str(listadoPuntuaciones))
        return

#E: ninguna
#S: una lista
#D: tomando la variable global del listado de todas las puntaciones las ordena y las retorna de orden descendente según sus ganes
def ordenaPuntuaciones ():
    global listadoPuntuaciones
    listadoPuntuaciones=cargarArchivo("listaPuntuaciones.txt")
    listaOrdenada=[]
    contador=1
    while len(listaOrdenada)!=len(listadoPuntuaciones):
        for elem in listadoPuntuaciones:
            if elem[1]==contador:
                listaOrdenada=[elem]+listaOrdenada
        contador+=1
    return listaOrdenada

#E: ninguna
#S: impresión de labels en pantalla
#D: tomando la lista de puntuaciones ordenada la imprime en pantalla
pygame.font.init ()
myfont2 = pygame.font.SysFont("agencyfb", 30)

def imprimirRanking ():
    global listadoPuntuaciones
    listadoPuntuaciones=ordenaPuntuaciones()
    contadorx=90
    contadory=200
    texto1=""
    texto2=""
    for elem in listadoPuntuaciones:
        texto1=str(elem[0])
        texto2=str(elem[1])
        label1=myfont2.render((texto1),1,NEGRO)
        screen.blit(label1,(contadorx,contadory))
        label2=myfont2.render((texto2),1,ROJO)
        screen.blit(label2,(contadorx*4+40,contadory))
        contadory+=35


#---------------------------GUARDAR Y CARGAR PARTIDA-----------------------

#E: matriz
#S: guarda las variables globales en el txt "partidasGuardadas"
#D: guarda la informacion indispensable de las variables globales de una partida en el txt "partidasGuardadas"

def guardarPartida(matriz): 
     global partidaGuardaCarga, nombreJ1, nombreJ2,indiceEnPantallaFila, indiceEnPantallaCol,turno, indicesAImprimirFila, indicesAImprimirColumna
     if type(matriz)!=list:
         partidaGuardaCarga = [matriz.tolist(), nombreJ1, nombreJ2, indiceEnPantallaFila, indiceEnPantallaCol,indicesAImprimirFila, indicesAImprimirColumna,turno]
     else:
         partidaGuardaCarga = [matriz, nombreJ1, nombreJ2, indiceEnPantallaFila, indiceEnPantallaCol,indicesAImprimirFila, indicesAImprimirColumna,turno]
     print (partidaGuardaCarga)
     guardar("partidasGuardadas.txt", str(partidaGuardaCarga))
     partidaGuardaCarga = []

#E: ninguna
#S: toma la informacion del txt "partidasGuardadas" y la importa en el program
#D: toma la informacion de una partida que habiamos guardado anteriormente en el txt "partidasGuardadas" y carga la informacion
#   al programa para ejecutar el juego tal y como fue dejado

def cargarPartidaTXT():
     global partidaGuardaCarga, nombreJ1, nombreJ2, matriz,indiceEnPantallaFila, indiceEnPantallaCol,turno, indicesAImprimirFila, indicesAImprimirColumna
     partidaGuardaCarga = cargarArchivo("partidasGuardadas.txt")
     print (partidaGuardaCarga)
     if partidaGuardaCarga==[]:
         print ("No hay partida guardada.")
         return False
     else:
         matrizL = partidaGuardaCarga[0]
         matrizA = np.asarray(matrizL)
         matriz = matrizA
         nombreJ1 = str(partidaGuardaCarga[1])
         nombreJ2 = str(partidaGuardaCarga[2])
         indiceEnPantallaFila = partidaGuardaCarga[3]
         indiceEnPantallaCol = partidaGuardaCarga[4]
         indicesAImprimirFila = partidaGuardaCarga[5]
         indicesAImprimirColumna = partidaGuardaCarga[6] 
         turno = partidaGuardaCarga[7]

         partidaGuardaCarga =[]
         return True

     
#-----------------------------Juego principal - PYGAME-----------------------------
#PANTALLA Y TIPOGRAFÍA
pygame.init ()
SQUARESIZE = 100
width = 10*SQUARESIZE
height = 7*SQUARESIZE
size = (width, height)
radio = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode (size)
pygame.display.update ()
pygame.font.init ()
myfont = pygame.font.SysFont("agencyfb", 75)
myfont4 = pygame.font.SysFont("agencyfb", 35)

#CARGA DE IMÁGENES
flechaAbajoD=pygame.image.load ("flechaAbajoD.png")
flechaArribaC=pygame.image.load ("flechaArribaC.png")
flechaArribaD=pygame.image.load ("flechaArribaD.png")
flechaDerechaC=pygame.image.load ("flechaDerechaC.png")
flechaDerechaD=pygame.image.load ("flechaDerechaD.png")
flechaIzquierdaC=pygame.image.load ("flechaIzquierdaC.png")
flechaIzquierdaD=pygame.image.load ("flechaIzquierdaD.png")
cuadroDecoracion=pygame.image.load ("cuadro4.png")
tituloDesplazamiento=pygame.image.load ("tituloDesplazamiento.png")
tituloCrecimiento=pygame.image.load ("tituloCrecimiento.png")
guardarPartidaBoton=pygame.image.load ("guardarPartidaBoton.png")
menuB=pygame.image.load ("menu.png")
ganador1IA = pygame.image.load ("ganador1IA.png")

#E: ninguna
#S: cada uno de los turnos del juego
#D: función pricipal y base del juego donde todo comienza
#   En esta funcion se toman los turnos, se controla el posicionamiento de fichas y la actualizacion de la matriz
def turnos ():
    global matriz, game_over,turno,screen,nombreJ1,nombreJ2,indicesAImprimirFila,indicesAImprimirColumna,indiceEnPantallaCol,indiceEnPantallaFila
    pygame.mixer.music.load("partida.mp3")
    pygame.mixer.music.play (-1)
    screen2 = pygame.display.set_mode (size)
    cuadroDeJuego (matriz)
    imprimirIndicesFilas()
    imprimirIndicesColumnas()
    pygame.display.update ()
    imagen((880),(370),flechaAbajoD)
    imagen((880),(270),flechaArribaD)
    imagen((880),(470),flechaArribaC)
    imagen((929),(519),flechaDerechaC)
    imagen((929),(320),flechaDerechaD)
    imagen((830),(519),flechaIzquierdaD)
    imagen((830),(320),flechaIzquierdaC)
    imagen((880),(519),cuadroDecoracion)
    imagen((880),(320),cuadroDecoracion)
    imagen((810),(230),tituloDesplazamiento)
    imagen((810),(430),tituloCrecimiento)
    imagen((890),(100),guardarPartidaBoton)
    imagen((850),(580),menuB)
    while game_over ==False:
        if turno == 0:
            pygame.draw.rect(screen, NEGRO,[760,130,80,80])
            label = myfont4.render(("Turno de:"), 1, CYAN)
            screen.blit(label, (760,100))
            label2 = myfont4.render((nombreJ1), 1, CYAN)
            screen.blit(label2, (760,130))
            pygame.display.update ()
        else:
            pygame.draw.rect(screen, NEGRO,[760,130,80,80])
            label = myfont4.render(("Turno de:"), 1, VERDE)
            screen.blit(label, (760,100))
            label2 = myfont4.render((nombreJ2), 1, VERDE)
            screen.blit(label2, (760,130))
            pygame.display.update ()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, NEGRO, (0,0, width, SQUARESIZE))
                if event.pos[0]>=0 and event.pos[0]<=690:
                    if event.pos[1]>=0 and event.pos[1]<=100:
                        posx = event.pos[0]
                        if turno == 0:
                            pygame.draw.circle(screen, CYAN, (posx, int(SQUARESIZE/2)), radio)
                        else:
                            pygame.draw.circle(screen, VERDE, (posx, int(SQUARESIZE/2)), radio)
            pygame.display.update ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, NEGRO, (0,0, width, SQUARESIZE))
                if event.pos[0]>=850 and event.pos[0]<=950:
                    if event.pos[1]>=580 and event.pos[1]<=680:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            screen2 = pygame.display.set_mode ((600,600))
                            matriz=([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
                            turno = 0
                            game_over = False
                            nombreJ1 = ""
                            nombreJ2 = ""
                            indicesAImprimirFila=[1,2, 3, 4, 5, 6]
                            indicesAImprimirColumna=[1, 2, 3, 4, 5, 6, 7]
                            indiceEnPantallaCol=0
                            indiceEnPantallaFila=0
                            menuDeInicio()
                if event.pos[0]>=890 and event.pos[0]<=990:
                    if event.pos[1]>=100 and event.pos[1]<=200:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            guardarPartida(matriz)
                if event.pos[0]>=0 and event.pos[0]<=690:
                    if event.pos[1]>=0 and event.pos[1]<=100:
                        if turno == 0:
                            posx = event.pos[0]
                            col = int(math.floor(posx/100))+indiceEnPantallaCol
                            if columnaLlena (matriz,col):
                                creceHaciaArriba ()
                                pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                imprimirIndicesFilas()
                                imprimirIndicesColumnas()
                                pygame.display.update ()
                            fila=colocaEnFila (col)
                            colocaFicha(matriz,fila,col,1)
                            fichasEnTablero (matriz)
                            if ganeDeJugador (1):
                                label = myfont.render(("GANADOR: "), 1, CYAN)
                                screen.blit(label, (185,10))
                                label = myfont.render((nombreJ1), 1, CYAN)
                                screen.blit(label, (450,10))
                                listaConPuntuaciones (nombreJ1)
                                game_over = True
                        else:
                            posx = event.pos[0]
                            col = int(math.floor(posx/100))+indiceEnPantallaCol
                            if columnaLlena (matriz,col):
                                creceHaciaArriba ()
                                pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                imprimirIndicesFilas()
                                imprimirIndicesColumnas()
                                pygame.display.update ()
                            fila=colocaEnFila (col)
                            colocaFicha(matriz,fila,col,2)
                            fichasEnTablero (matriz)
                            if ganeDeJugador (2):
                                label = myfont.render("GANADOR: ", 1, VERDE)
                                screen.blit(label, (185,10))
                                label = myfont.render((nombreJ2), 1, VERDE)
                                screen.blit(label, (450,10))
                                listaConPuntuaciones (nombreJ2)
                                game_over = True
        
                        print(matriz)
                        pygame.display.update ()
                        turno += 1
                        turno = turno % 2
                else:
                    if event.pos[0]>=933 and event.pos[0]<=976:
                        if event.pos[1]>=519 and event.pos[1]<=570:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                crearMatrizNuevaDer ()
                                pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                imprimirIndicesColumnas()
                                imprimirIndicesFilas()
                                pygame.display.update ()
                        else:
                            if event.pos[1]>=321 and event.pos[1]<=379:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    moverDerecha ()
                                    pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                    imprimirIndicesColumnas ()
                                    imprimirIndicesFilas()
                                    pygame.display.update ()
                    else:
                        if event.pos[0]>=830 and event.pos[0]<=880:
                            if event.pos[1]>=320 and event.pos[1]<=370:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    moverIzquierda ()
                                    pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                    imprimirIndicesColumnas ()
                                    imprimirIndicesFilas()
                                    pygame.display.update ()
                            else:
                                if event.pos[1]>=520 and event.pos[1]<=570:
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        crearMatrizNuevaIzq ()
                                        pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                        imprimirIndicesColumnas ()
                                        imprimirIndicesFilas()
                                        pygame.display.update ()
                        else:
                            if event.pos[0]>=880 and event.pos[0]<=930:
                                if event.pos[1]>=270 and event.pos[1]<=320:
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        moverArriba ()
                                        pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                        imprimirIndicesFilas()
                                        imprimirIndicesColumnas()
                                        pygame.display.update ()
                                else:
                                    if event.pos[1]>=470 and event.pos[1]<=520:
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            creceHaciaArriba()
                                            pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                            imprimirIndicesFilas()
                                            imprimirIndicesColumnas()
                                            pygame.display.update ()
                                    else:
                                        if event.pos[1]>=370 and event.pos[1]<=420:
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                moverAbajo ()
                                                pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                                imprimirIndicesFilas()
                                                imprimirIndicesColumnas()
                                                pygame.display.update ()

        pygame.display.update ()       
    while game_over==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait (3000)
        screen2 = pygame.display.set_mode ((600,600))
        matriz=([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        turno = 0
        game_over = False
        nombreJ1 = ""
        nombreJ2 = ""
        indicesAImprimirFila=[1,2, 3, 4, 5, 6]
        indicesAImprimirColumna=[1, 2, 3, 4, 5, 6, 7]
        indiceEnPantallaCol=0
        indiceEnPantallaFila=0
        menuDeInicio ()

#-----------------------------------------------------------------------------------

#                                         IA

#-----------------------------------------------------------------------------------

#-----------------------------Movimiento IA-----------------------------

#VERTICAL AI

#E: matriz
#S: una lista
#D: toma la matriz y cuenta cuantas fichas seguidas hay de forma vertical en cada columna, esto lo hace con ayuda de una funcion
#   auxiliar

def cuantasFichasSeguidas(matriz):
    res = []
    columna = []
    for i in range(0, len(matriz[0])):
        for j in range(0, len(matriz)):
            columna = columna + [matriz[j][i]]
        res += [cuantasFichasSeguidas_aux(columna)]
        columna = []
    return res

#E: numero entero (columna)
#S: una lista
#D: toma una columna y busca cuantas fichas seguidas hay y que numero de ficha es el que hay seguido

def cuantasFichasSeguidas_aux(columna):
    valorAcumulado = 0
    i = 0
    while columna[i] == 0 and i < len(columna) - 1:
        i += 1
    ficha = columna[i]
    while columna[i] == ficha and i < len(columna) - 1:
        i += 1
        valorAcumulado += 1

    if columna[i] == ficha and columna[i] != 0:
        ficha = columna[i]
        valorAcumulado += 1

    return [valorAcumulado, ficha]

#E: matriz
#S: un numero entero si encuetra donde tirar, y si no un string
#D: toma la matriz y con la lista de las posibles posiciones a donde puede tirar evalua si es un lugar libre y esta permitido tirar,
#   elige de manera random una de esas posiciones. Si no hay ninguna posicion a donde tirar retornar un string:"no hay gane"

def elijaColumna_ponerVeritcal(matriz):
    lineasVerticales = cuantasFichasSeguidas(matriz)
    posiblesPosGane = []
    posiblesPosTape = []

    for i in range(0, len(matriz[0])):
        if lineasVerticales[i][0] > 2 and lineasVerticales[i][1] == 2:
            posiblesPosGane += [i]
        elif lineasVerticales[i][0] > 2 and lineasVerticales[i][1] == 1:
            posiblesPosTape += [i]

    if posiblesPosGane == []:
        if posiblesPosTape == []:
            return "no hay gane"
        else:
            return random.choice(posiblesPosTape)

    return random.choice(posiblesPosGane)



#HORIZONTAL AI

#E: matriz
#S: una lista
#D: toma la matriz y cuenta cuantas fichas seguidas hay de forma horizontal en cada fila, esto lo hace con ayuda de una funcion
#   auxiliar

def cuantasFichasSeguidasH(matriz):
    res = []
    fila = []
    for i in range(0, len(matriz)):
        fila = matriz[i]
        res = res + [cuantasFichasSeguidasH_aux(fila)]
        fila = []
    return res

#E: numero entero (fila)
#S: una lista
#D: toma una fila y busca cuantas fichas seguidas hay y que numero de ficha es el que hay seguido

def cuantasFichasSeguidasH_aux(fila):
    valorAcumulado = 0
    ficha = 0
    for i in range(0, len(fila) - 2):
        if fila[i] != 0:
            ficha = fila[i]
            if fila[i] == fila[i + 1] and fila[i + 1] == fila[i + 2]:
                ficha = fila[i]
                valorAcumulado += 3
            else:
                if fila[i] == fila[i + 1]:
                    ficha = fila[i]
                    valorAcumulado += 2
    return [valorAcumulado, ficha]

#E: matriz (la global)
#S: una lista (copia de la matriz global con las marcas)
#D: toma la matriz revisa en cada una de las columnas si hay posibilidades de gane de alguna u otra forma y las marca con un 8

def cuentaHorizontal(matrizOriginal):
    matriz = copy.deepcopy(matrizOriginal)
    poneFicha = 0
    x = 8
    for i in reversed(range(0, len(matriz))):
        for j in range(0, len(matriz[0]) - 2):
            if matriz[i][j] == 1 and matriz[i][j + 1] == 1 and matriz[i][j + 2] == 1:
                if j + 2 == len(matriz[0]) - 1:
                    if matriz[i][j - 1] == 0:
                        matriz[i][j - 1] = x
                        print("Esta es la matriz1")
                        print(matriz)
                        return (matriz)
                else:
                    if j == 0:
                        if matriz[i][j + 3] == 0:
                            matriz[i][j + 3] = x
                            print("Esta es la matriz2")
                            print(matriz)
                            return (matriz)
                    else:
                        if matriz[i][j - 1] == 0 and matriz[i][j + 3] == 0:
                            poneFicha = random.choice([1, 2])
                            if poneFicha == 1:
                                print("Esta es la matriz3")
                                print(matriz)
                                matriz[i][j - 1] = x
                                return (matriz)
                            else:
                                matriz[i][j + 3] = x
                                print("Esta es la matriz4")
                                print(matriz)
                                return (matriz)
                        else:
                            if matriz[i][j - 1] == 0:
                                matriz[i][j - 1] = x
                                print("Esta es la matriz5")
                                print(matriz)
                                return (matriz)
                            else:
                                if matriz[i][j + 3] == 0:
                                    matriz[i][j + 3] = x
                                    print("Esta es la matriz6")
                                    print(matriz)
                                    return (matriz)
    for i in reversed(range(0, len(matriz))):
        for j in range(0, len(matriz[0]) - 3):
            if matriz[i][j] == 1 and matriz[i][j + 1] == 1 and matriz[i][j + 2] == 0 and matriz[i][j + 3] == 1:
                matriz[i][j + 2] = x
                print("Esta es la matriz7")
                print(matriz)
                return (matriz)
            else:
                if matriz[i][j] == 1 and matriz[i][j + 1] == 0 and matriz[i][j + 2] == 1 and matriz[i][j + 3] == 1:
                    matriz[i][j + 1] = x
                    print("Esta es la matriz8")
                    print(matriz)
                    return (matriz)

    for i in reversed(range(0, len(matriz))):
        for j in range(0, len(matriz[0]) - 1):
            if matriz[i][j] == 1 and matriz[i][j + 1] == 1:
                if j + 1 == len(matriz[0]) - 1:
                    if matriz[i][j - 1] == 0:
                        matriz[i][j - 1] = x
                        print("Esta es la matriz9")
                        print(matriz)
                        return (matriz)
                else:
                    if j == 0:
                        if matriz[i][j + 2] == 0:
                            matriz[i][j + 2] = x
                            print("Esta es la matriz10")
                            print(matriz)
                            return (matriz)
                    else:
                        if matriz[i][j - 1] == 0 and matriz[i][j + 2] == 0:
                            poneFicha = random.choice([1, 2])
                            # print(poneFicha)
                            return (matriz)
                            if poneFicha == 1:
                                matriz[i][j - 1] = x
                                print("Esta es la matriz11")
                                print(matriz)
                                return (matriz)
                            else:
                                matriz[i][j + 2] = x
                                print("Esta es la matriz12")
                                print(matriz)
                                return (matriz)
                        else:
                            if matriz[i][j - 1] == 0:
                                matriz[i][j - 1] = x
                                print("Esta es la matriz13")
                                print(matriz)
                                return (matriz)
                            else:
                                if matriz[i][j + 2] == 0:
                                    matriz[i][j + 2] = x
                                    print("Esta es la matriz14")
                                    print(matriz)
                                    return (matriz)
    return matrizOriginal

#E: matriz
#S: una lista conformada por booleanos
#D: toma la matriz y revisa en cada una de las columnas si hay ceros abajo del todo

def tieneCeros_abajo(matriz):
    res = []
    columna = []
    for i in range(0, len(matriz[0])):
        for j in range(0, len(matriz)):
            columna = columna + [matriz[j][i]]
        res += [tieneCeros_abajo_aux(columna)]
        columna = []
    return res

#E: numero entero (columna)
#S: un bool, True or False
#D: la columna y revisa si hay 0 en la parte final o no

def tieneCeros_abajo_aux(col):
    tiene = False
    i = 0

    while tiene == False and i < len(col) - 1:
        if col[i] != 0 and col[i + 1] == 0:
            tiene = True
        i += 1
    return tiene

#E: matriz
#S: una lista conformada por booleanos
#D: toma la matriz y revisa en cada una de las columas si estan marcadas o no en la matriz temporal

def comlumna_marcada(matriz):
    res = []
    columna = []
    for i in range(0, len(matriz[0])):
        for j in range(0, len(matriz)):
            columna = columna + [matriz[j][i]]
        res += [comlumna_marcada_aux(columna)]
        columna = []
    return res

#E: matriz
#S: un bool, True or False
#D: funcion auxiliar que toma la matriz y revisa en cada una de las columas si estan marcadas o no en la matriz temporal

def comlumna_marcada_aux(col):
    marcada = False
    i = 0
    x = 8

    while marcada == False and i < len(col):
        if col[i] == x:
            marcada = True
        i += 1
    return marcada

#E: matriz
#S: un numero entero si encuetra donde tirar, y si no un string
#D: toma la matriz y con la lista de las posibles posiciones a donde puede tirar evalua si es un lugar libre y esta permitido tirar,
#   elige de manera random una de esas posiciones. Si no hay ninguna posicion a donde tirar retornar un string:"no hay gane"

def elijaColumna_ponerHorizontal(matriz):
    tempMatriz = cuentaHorizontal(matriz)
    columnaMarcada = comlumna_marcada(tempMatriz)
    columnaCeros_abajo = tieneCeros_abajo(tempMatriz)
    posiblesPos = []

    for i in range(0, len(matriz[0])):
        if columnaMarcada[i] and not(columnaCeros_abajo[i]):
            posiblesPos += [i]

    if posiblesPos != []:
        return random.choice(posiblesPos)
    else:
        return "no hay gane"


#-------------------------------------------------------------------

#                       DIAGONAL ANTI_DIAGONAL

#-------------------------------------------------------------------

#E: matriz (la global)
#S: una lista (copia de la matriz global con las marcas)
#D: toma la matriz revisa en cada una de las columnas si hay posibilidades de gane de alguna u otra forma y las marca con un 8

def cuentaAnti_Diagonal(matrizOriginal):
    matriz = copy.deepcopy(matrizOriginal)
    poneFicha=0
    x=8
    for i in range (0, len(matriz)-3):
        for j in range(3, len(matriz[0])):
            if matriz[i+1][j-1] == 1 and matriz[i+2][j-2] == 1 and matriz[i+3][j-3] == 1:
                if matriz[i][j] == 0:
                    matriz[i][j] = x
                    return (matriz)
            else:
                if matriz[i][j] == 1 and matriz[i+1][j-1] == 1 and matriz[i+2][j-2] == 1 and matriz[i+3][j-3]==0:
                    matriz[i+3][j-3] = x
                    return (matriz)
                else:
                    if matriz[i][j] == 1 and matriz[i+1][j-1] == 0 and matriz[i+2][j-2] == 1 and matriz[i+3][j-3]==1:
                        matriz[i+1][j-1] =x
                        return (matriz)
                    else:
                        if matriz[i][j] == 1 and matriz[i+1][j-1] == 1 and matriz[i+2][j-2] == 0 and matriz[i+3][j-3]==1:
                            matriz[i+2][j-2] =x
                            return (matriz)

    return matrizOriginal

#E: matriz
#S: un numero entero si encuetra donde tirar, y si no un string
#D: toma la matriz y con la lista de las posibles posiciones a donde puede tirar evalua si es un lugar libre y esta permitido tirar,
#   elige de manera random una de esas posiciones. Si no hay ninguna posicion a donde tirar retornar un string:"no hay gane"

def elijaColumna_ponerAntiDiagonal(matriz):
    tempMatriz = cuentaAnti_Diagonal(matriz)
    columnaMarcada = comlumna_marcada(tempMatriz)
    columnaCeros_abajo = tieneCeros_abajo(tempMatriz)
    posiblesPos = []

    for i in range(0,len(matriz[0])):
        if columnaMarcada[i] and not(columnaCeros_abajo[i]):
            posiblesPos += [i]

    if posiblesPos != []:
        return random.choice(posiblesPos)
    else:
        return "no hay gane"




#-------------------------------------------------------------------

#                       DIAGONAL DIAGONAL

#-------------------------------------------------------------------

#E: matriz (la global)
#S: una lista (copia de la matriz global con las marcas)
#D: toma la matriz revisa en cada una de las columnas si hay posibilidades de gane de alguna u otra forma y las marca con un 8

def cuentaDiagonal(matrizOriginal):
    matriz = copy.deepcopy(matrizOriginal)
    poneFicha=0
    x=8
    for i in range (1, len(matriz)-3):
        for j in reversed (range(1, len(matriz[0])-3)):
            if matriz[i][j] == 1 and matriz[i+1][j+1] == 1 and matriz[i+2][j+2] == 1:
                if matriz [i-1][j-1]==0 and matriz [i+3][j+3]==0:
                   matriz[i+3][j+3] = x
                   return matriz
    for i in range (0, len(matriz)-3):
        for j in reversed( range(0, len(matriz[0])-3)):
            if matriz[i+1][j+1] == 1 and matriz[i+2][j+2] == 1 and matriz[i+3][j+3] == 1:
                if matriz[i][j] == 0:
                    matriz[i][j] = x
                    return matriz
            else:
                if matriz[i][j] == 1 and matriz[i+1][j+1] == 1 and matriz[i+2][j+2] == 1:
                    if matriz[i+3][j+3]==0:
                        matriz[i+3][j+3]=x
                        return matriz
                else:
                    if matriz[i][j] == 1 and matriz[i+1][j+1] == 0 and matriz[i+2][j+2] == 1 and matriz[i+3][j+3]==1:
                        matriz[i+1][j+1] =x
                        return matriz
                    else:
                        if matriz[i][j] == 1 and matriz[i+1][j+1] == 1 and matriz[i+2][j+2] == 0 and matriz[i+3][j+3]==1:
                            matriz[i+2][j+2] =x
                            return matriz
    return matrizOriginal

#E: matriz
#S: un numero entero si encuetra donde tirar, y si no un string
#D: toma la matriz y con la lista de las posibles posiciones a donde puede tirar evalua si es un lugar libre y esta permitido tirar,
#   elige de manera random una de esas posiciones. Si no hay ninguna posicion a donde tirar retornar un string:"no hay gane"

def elijaColumna_ponerDiagonal(matriz):
    tempMatriz = cuentaDiagonal(matriz)
    columnaMarcada = comlumna_marcada(tempMatriz)
    columnaCeros_abajo = tieneCeros_abajo(tempMatriz)
    posiblesPos = []

    for i in range(0,len(matriz[0])):
        #print(i)
        if columnaMarcada[i] and not(columnaCeros_abajo[i]):
            print(i)
            posiblesPos += [i]

    if posiblesPos != []:
        return random.choice(posiblesPos)
    else:
        return "no hay gane"

#E: una matriz
#S: una matriz
#D: retorna la matriz girada (filas al contrario)

def invertirMatriz (matriz, res=[]):
    for fila in matriz:
        res=[fila]+res
    return res

#-----------------------------Juego principal IA - PYGAME-----------------------------

#E: ninguna
#S: cada uno de los turnos del juego
#D: función pricipal y base del juego donde todo comienza
#   En esta funcion se toman los turnos, se controla el posicionamiento de fichas y la actualizacion de la matriz
def turnos2 ():
    pygame.mixer.music.load("juegoIA.mp3")
    pygame.mixer.music.play (-1)
    global matriz, game_over2,turno2,screen, VERDE,CYAN,indiceEnPantallaCol,indiceEnPantallaFila,indicesAImprimirFila, indicesAImprimirColumna
    screen2 = pygame.display.set_mode (size)
    cuadroDeJuego (matriz)
    imprimirIndicesFilas()
    imprimirIndicesColumnas()
    pygame.display.update ()
    imagen((880),(370),flechaAbajoD)
    imagen((880),(270),flechaArribaD)
    imagen((880),(470),flechaArribaC)
    imagen((929),(519),flechaDerechaC)
    imagen((929),(320),flechaDerechaD)
    imagen((830),(519),flechaIzquierdaD)
    imagen((830),(320),flechaIzquierdaC)
    imagen((880),(519),cuadroDecoracion)
    imagen((880),(320),cuadroDecoracion)
    imagen((810),(230),tituloDesplazamiento)
    imagen((810),(430),tituloCrecimiento)
    imagen((850),(580),menuB)

    while game_over2 ==False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, NEGRO, (0,0, width, SQUARESIZE))
                if event.pos[0]>=0 and event.pos[0]<=690:
                    if event.pos[1]>=0 and event.pos[1]<=100:
                        posx = event.pos[0]
                        if turno2 == 0:
                            pygame.draw.circle(screen, CYAN, (posx, int(SQUARESIZE/2)), radio)
            pygame.display.update ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, NEGRO, (0,0, width, SQUARESIZE))
                if event.pos[0]>=850 and event.pos[0]<=950:
                    if event.pos[1]>=580 and event.pos[1]<=680:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            screen2 = pygame.display.set_mode ((600,600))                 
                            matriz=([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
                            turno2 = 0
                            game_over2 = False
                            indicesAImprimirFila=[1,2, 3, 4, 5, 6]
                            indicesAImprimirColumna=[1, 2, 3, 4, 5, 6, 7]
                            indiceEnPantallaCol=0
                            indiceEnPantallaFila=0
                            menuDeInicio()
                if event.pos[0]>=0 and event.pos[0]<=690:
                    if event.pos[1]>=0 and event.pos[1]<=100:
                        if turno2 == 0:
                            posx = event.pos[0]
                            col = int(math.floor(posx/100))+indiceEnPantallaCol
                            if columnaLlena (matriz,col):
                                creceHaciaArriba ()
                                pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                imprimirIndicesFilas()
                                imprimirIndicesColumnas()
                                pygame.display.update ()
                            fila=colocaEnFila (col)
                            colocaFicha(matriz,fila,col,1)
                            fichasEnTablero (matriz)
                            if ganeDeJugador (1):
                                label = myfont.render("GANADOR: Jugador#1.", 1, CYAN)
                                screen.blit(label,(185,10))
                                pygame.display.update ()
                                game_over2 = True
                            turno2 += 1
                            turno2 = turno2 % 2
                else:
                    if event.pos[0]>=933 and event.pos[0]<=976:
                        if event.pos[1]>=519 and event.pos[1]<=570:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                crearMatrizNuevaDer ()
                                pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                imprimirIndicesFilas()
                                imprimirIndicesColumnas()
                                pygame.display.update ()
                        else:
                            if event.pos[1]>=321 and event.pos[1]<=379:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    moverDerecha ()
                                    pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                    imprimirIndicesFilas()
                                    imprimirIndicesColumnas()
                                    pygame.display.update ()        
                    else:
                        if event.pos[0]>=830 and event.pos[0]<=880:
                            if event.pos[1]>=320 and event.pos[1]<=370:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    moverIzquierda ()
                                    pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                    imprimirIndicesFilas()
                                    imprimirIndicesColumnas()
                                    pygame.display.update ()
                            else:
                                if event.pos[1]>=520 and event.pos[1]<=570:
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        crearMatrizNuevaIzq ()
                                        pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                        imprimirIndicesFilas()
                                        imprimirIndicesColumnas()
                                        pygame.display.update ()
                        else:
                            if event.pos[0]>=880 and event.pos[0]<=930:
                                if event.pos[1]>=270 and event.pos[1]<=320:
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        moverArriba ()
                                        pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                        imprimirIndicesFilas()
                                        imprimirIndicesColumnas()
                                        pygame.display.update ()
                                else:
                                    if event.pos[1]>=470 and event.pos[1]<=520:
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            creceHaciaArriba()
                                            pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                            imprimirIndicesFilas()
                                            imprimirIndicesColumnas()
                                            pygame.display.update ()
                                    else:
                                        if event.pos[1]>=370 and event.pos[1]<=420:
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                moverAbajo ()
                                                pygame.draw.rect(screen, NEGRO,[700,100,100,800])
                                                imprimirIndicesFilas()
                                                imprimirIndicesColumnas()
                                                pygame.display.update ()

        if turno2==1 and game_over2 ==False:
            if elijaColumna_ponerHorizontal(matriz) == "no hay gane" and elijaColumna_ponerVeritcal(matriz) == "no hay gane" and elijaColumna_ponerDiagonal(matriz) == "no hay gane" and elijaColumna_ponerAntiDiagonal(matriz) == "no hay gane":
                col = random.randint(0, len(matriz[0]) - 1)
                if columnaLlena (matriz,col):
                    creceHaciaArriba ()
            else:
                if elijaColumna_ponerDiagonal(matriz) != "no hay gane":
                    col = elijaColumna_ponerDiagonal(matriz)
                else:
                    if elijaColumna_ponerAntiDiagonal(matriz) != "no hay gane":
                        col = elijaColumna_ponerAntiDiagonal(matriz)
                    else:
                        if elijaColumna_ponerVeritcal(matriz) != "no hay gane":
                            col = elijaColumna_ponerVeritcal(matriz)
                        else:
                            if elijaColumna_ponerHorizontal(matriz) != "no hay gane":
                                col = elijaColumna_ponerHorizontal(matriz)
            fila=colocaEnFila (col)
            colocaFicha(matriz,fila,col,2)
            fichasEnTablero (matriz)
            if ganeDeJugador (2):
                label2 = myfont.render("GANADOR: Computadora.", 1, VERDE)
                screen.blit(label2, (185,10))
                game_over2 = True
            pygame.display.update ()
            turno2 += 1
            turno2 = turno2 % 2
            pygame.display.update ()       

    while game_over2==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.time.wait (3000)
        screen2 = pygame.display.set_mode ((600,600))
        matriz=([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
        turno2 = 0
        game_over2 = False
        indicesAImprimirFila=[1,2, 3, 4, 5, 6]
        indicesAImprimirColumna=[1, 2, 3, 4, 5, 6, 7]
        indiceEnPantallaCol=0
        indiceEnPantallaFila=0
        menuDeInicio ()

#-----------------------------------------------------------------------------------
#                           CARGA DE IMAGENES PARA VENTANAS
#-----------------------------------------------------------------------------------

#E: punto x, punto y (números enteros) y una imagen
#S: ninguna, solo coloca la imagen
#D: dados los parámetros (coordenadas), coloca la imagen dada según estos

def imagen (x,y,imagen):
    screen2.blit(imagen,(x,y))

#-----------------------------------------------------------------------------------
#                                 NOMBRES DE JUGADORES - PYGAME
#-----------------------------------------------------------------------------------

menuB=pygame.image.load ("menu.png")
fondo2J=pygame.image.load ("2jugadoresF.png")
iniciarPartidaI=pygame.image.load ("nuevoJuego.png")
partidaNoInicia=True
text = ''
text2 = ''

#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (INICIA EL JUEGO)

def iniciarPartida (x,y,ancho,altura):
    global nombreJ1,nombreJ2
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if nombreJ1!="" and nombreJ2!="":
            if click[0]==1:
                turnos ()
                partidaNoInicia=False

#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (VUELVE AL MENÚ)
                
def volverAlMenu (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            menuDeInicio ()
            partidaNoInicia=False

#E: ninguna
#S: pasarle los nombres (strings) a las variables globales para que sean utilizadas
#D: mediante 2 inputs se toman 2 strings (nombres de los jugadores) y estos se le pasan a dos variables globales y son utilizados por otras funciones

def nombreJugadores ():
    pygame.mixer.music.load("ponerNombresWaiting.mp3")
    pygame.mixer.music.play (-1)
    global text,text2,nombreJ1,nombreJ2
    pygame.font.init ()
    font = pygame.font.Font(None, 32)
    font2 = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(310, 155, 140, 32)
    input_box2 = pygame.Rect(310, 280, 140, 32)
    color_inactive = pygame.Color('red')
    color_inactive2 = pygame.Color('red')
    color_active2 = pygame.Color('green')
    color_active = pygame.Color('green')
    color = color_inactive
    color2 = color_inactive2
    active = False
    active2 = False
    done = False
    done2 = False
    while partidaNoInicia:
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                pygame.display.update ()
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        nombreJ1=text
                        print(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                pygame.display.update ()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box2.collidepoint(event.pos):
                    active2 = not active2
                else:
                    active2 = False
                color2 = color_active2 if active2 else color_inactive2
                pygame.display.update ()
            if event.type == pygame.KEYDOWN:
                if active2:
                    if event.key == pygame.K_RETURN:
                        nombreJ2=text2
                        print(text2)
                        text2 = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode
                pygame.display.update ()

        screen.blit(fondo2J,(0,0))
        iniciarPartida (130,460,128,128)
        volverAlMenu(10,470,100,100)
        imagen((10),(470),menuB)
        imagen((130),(460),iniciarPartidaI)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface2 = font2.render(text2, True, color2)
        width2 = max(200, txt_surface2.get_width()+10)
        input_box2.w = width2
        screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
        pygame.draw.rect(screen, color2, input_box2, 2)
        pygame.display.flip() #este es el que daba problema, se pone solo uno al final de todo
        pygame.display.update()
    while partidaNoInicia==False:
        quit ()

#-----------------------------------------------------------------------------------
#                                      PUNTAJES - PYGAME
#-----------------------------------------------------------------------------------

trofeo=pygame.image.load ("trofeo.png")
puntajesVistos=True
fondoP=pygame.image.load ("fondoPuntajes.png")

#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (VUELVE AL MENÚ)

def volverAlMenu (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            menuDeInicio ()
            puntajesVistos=False

#E: ninguno
#S: impresion de los labels en pantalla con el ranking correspondiente
#D: tomando la lista de puntuaciones ordenada la imprime en labels en pantalla, esto en orden descendente
            
def historialPuntajes (): 
    pygame.mixer.music.load("puntajesWaiting.mp3")
    pygame.mixer.music.play (-1)
    while puntajesVistos:
        screen2.blit(fondoP,(0,0))
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        imagen((420),(420),trofeo)
        imagen((10),(470),menuB)
        volverAlMenu(10,470,100,100)
        imprimirRanking()
        pygame.display.update ()
    while puntajesVistos==False:
        quit ()
        
#-----------------------------------------------------------------------------------
#                                   NUEVA PARTIDA - PYGAME
#-----------------------------------------------------------------------------------

partidaNueva=True

fondoNP=pygame.image.load ("fondoNP.png")
unJugadorI=pygame.image.load ("1jugador.png")
dosJugadoresI=pygame.image.load ("2jugadores.png")

#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (VUELVE AL MENÚ)

def volverAlMenu (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            menuDeInicio ()
            partidaNueva=False
            
#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (INICIA JUEGO CONTRA MÁQUINA)

def unJugador (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            turnos2()
            partidaNueva=False

#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (VA A INGRESAR NOMBRES)
            
def dosJugadores (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            nombreJugadores()
            partidaNueva=False

#E: ninguna
#S: pasar de una ventana a otra 
#D: con sus funciones y sus botones logra que se actualicen las ventanas (CAMBIO DE VENTANA DESDE LA NUEVA PARTIDA)
            
def nuevaPartidaOpciones ():
    pygame.mixer.music.load("nuevaPartida.mp3")
    pygame.mixer.music.play (-1)
    while partidaNueva:
        screen2.blit(fondoNP,(0,0))
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        unJugador (410,150,128,128)
        dosJugadores (410,400,128,128)
        imagen((410),(150),unJugadorI)
        imagen((410),(400),dosJugadoresI)
        imagen((10),(490),menuB)
        volverAlMenu(10,470,100,100)
        pygame.display.update ()
    while partidaNueva==False:
        quit ()



#-----------------------------------------------------------------------------------
#                                        MENU - PYGAME
#-----------------------------------------------------------------------------------
width2 = 600
height2 = 600
size2 = (width2, height2)
screen2 = pygame.display.set_mode (size2)

introJuego=True
fondoM=pygame.image.load ("fondo.png")
cargarPartidaI=pygame.image.load ("cargarPartida.png")
nuevoJuegoI=pygame.image.load ("nuevoJuego.png")
puntajesI=pygame.image.load ("puntajes.png")

#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (CARGAR PARTIDA DEL TXT Y JUEGAR CON NORMALIDAD)

def cargarPartida (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            if cargarPartidaTXT ()==True:
                turnos()
            else:
                menuDeInicio()
            introJuego=False
            
#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (VA AL MENÚ DE OPCIONES DE PARTIDAD)
            
def nuevoJuego (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            nuevaPartidaOpciones ()
            introJuego=False

#E: punto x, punto y, ancho y alto de una imagen (todos NÚMEROS ENTEROS)
#S: pasar de una ventana a otra 
#D: dado parámetros de click retorna un cambio de ventana al tocar entre estos (VA HACIA LOS PUNTAJES)
            
def puntajes (x,y,ancho,altura):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+ancho>mouse[0]>x and y+altura>mouse[1]>y:
        if click[0]==1:
            historialPuntajes ()
            introJuego=False

#E: ninguna
#S: contiene los botones para pasar de una ventana a otra
#D: ventana principal en la cual se controla toda accion posible dentro del juego
            
def menuDeInicio():
    pygame.mixer.music.load("partidaMenu.mp3")
    pygame.mixer.music.play (-1)
    while introJuego:
        screen2.blit(fondoM,(0,0))
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        cargarPartida (410,150,128,128)
        nuevoJuego (410,300,128,128)
        puntajes (410,450,128,128)
        imagen((410),(150),cargarPartidaI)
        imagen((410),(300),nuevoJuegoI)
        imagen((410),(450),puntajesI)
        pygame.display.update ()
    while introJuego==False:
        quit ()

menuDeInicio()

















