from algoturtle_extras import *
import sys
import csv



#Constantes Globales
ENTRADA = ['hex', '4', 'dads']
AVANZAR_UNIDADES = 10 #Cantidad de unidades que avanza la tortuga
DELIMITADOR_ARCHIVO_SISTEMA_L = ' '
EXTENSION_SVG = ".svg"
EXTENSION_SL = ".sl"
MENSAJE_ERROR = '''Bienvenido, abriste el archivo sin ningun comando o con menos de los necesarios, sus comandos son:
1. nombre del archivo .sl (obligatorio)
2. numero de veces a iterar (obligatorio tiene que ser entero)
3. nombre del archivo svg a escribir (obligatorio)
'''
ERROR_ARCHIVO_SISTEMA_L = 'El archivo ingresado a leer no existe'
ERROR_ANGULO = 'El angulo del archivo no es un numero'
ERROR_ARCHIVO_LETRA = 'Hay una linea que falla en el archivo'
OPERACIONES = "FGfg+-|[]ab12"
AZUL = "blue"
ROJO = "red"




#Main
def algo_fractales():
    '''Se encarga de la logica general de generar fractales, en caso de que alguna funcion encuentre un error, agarra la excepcion
    terminando con su ejecucion
    pre: la Entrada tiene que ser valida
    post: llama a las funciones necesarias para poder escribir el archivo svg deseado
    '''
    if validar_entrada(ENTRADA):
        ruta_archivo_sistema_l, iteraciones, ruta_archivo_svg = leer_entrada(ENTRADA, EXTENSION_SVG, EXTENSION_SL)
        try:
            comandos, tabla_conversion = generar_comandos(ruta_archivo_sistema_l, DELIMITADOR_ARCHIVO_SISTEMA_L, iteraciones)
        except Exception:
            sys.exit()
        primera_linea, cola_comandos = interpretar_comandos(comandos, OPERACIONES, tabla_conversion["angulo"], AVANZAR_UNIDADES)
        escribir_archivo_svg(ruta_archivo_svg, primera_linea, cola_comandos)
    else:
        print(MENSAJE_ERROR)




def validar_entrada(entrada):
    '''Verifica si los argumentos ingresados por el usuario son validos o no
    Pre: Recibe una lista de 3 elementos los cuales debe tener al elemento [1] como una cadena de entero
    Post: Devuelve True en caso de que la entrada sea valida o False sino
    '''
    if len(entrada) < 3:
        return False
    return len(entrada) == 3 and entrada[1].isdigit()



def leer_entrada(entrada_valida, extension_svg, extension_sl):
    '''Le da formato a la entrada valida del usuario
    Pre: Recibe una entrada valida y las extensiones de los archivos correspondientes
    Post: Devuelve la primer componente, si la componente del archivo le falta el .ls se lo agrega,
    la segunda componente como entero y la tercera componente, si le falta el .svg se lo agrega
    '''
    if not entrada_valida[2][:-5:-1] == extension_svg[::-1]:
        entrada_valida[2] += extension_svg
    if not entrada_valida[0][:-4:-1] == extension_sl[::-1]:
        entrada_valida[0] += extension_sl
    return entrada_valida[0], int(entrada_valida[1]), entrada_valida[2]



def generar_comandos(ruta, delimitador, iteraciones):
    '''Genera una cadena con los comandos a ejecutar y un diccionario con los axiomas, la tabla de conversion y el angulo
    Pre : Recibe la ruta del archivo donde se encuentra el sistema l, su separador y la cantidad de iteraciones
    Post: Devuelve una cadena de letras que se corresponden con los movimientos que debe realizar la tortuga
    y un diccionario ya mencionado
    '''
    tabla_conversion = {}
    leer_archivo_sistema_l(ruta, delimitador, tabla_conversion)
    movimientos = formar_movimientos(tabla_conversion, iteraciones)
    return movimientos, tabla_conversion


def leer_archivo_sistema_l(ruta, delimitador, tabla_conversion):
    '''Lee el archvio una vez, y crea un diccionario con claves y valores especificados a continuacion
    Pre: Recibe un nombre de un archivo en formato cadena (si el archivo no existe imprime un mensaje y levanta una excepcion),
    una cadena que va a servir como delimitador, y un diccionario vacio.
    Post: si el archivo se encontro de la forma:
    -angulo
    -axiomas
    -reglas
    Entonces devuelve un diccionario que tiene como claves angulo, axioma, y las letras del archivo
    y como valor los que elementos que sucedieron en las determinadas lineas del archivo
    '''
    try:
        with open(ruta, 'r', encoding = 'utf8') as archivo:
            lector = csv.reader(archivo, delimiter=delimitador)
            numero_angulo = next(lector)[0].split('.')

            if numero_angulo[0].isdigit():
                if len(numero_angulo) == 1:
                    tabla_conversion["angulo"] = int(numero_angulo[0])
                elif len(numero_angulo) ==2:
                    tabla_conversion["angulo"] = int(numero_angulo[0]) + int(numero_angulo[1])/(10*len(numero_angulo[1]))
                else:
                    print(ERROR_ANGULO)
                    raise Exception

            else:
                print(ERROR_ANGULO)
                raise Exception
            tabla_conversion["axiomas"] = next(lector)[0]
            for linea in lector:
                if len(linea) == 2:
                    tabla_conversion[linea[0]] = linea[1]
                else:
                    print(ERROR_ARCHIVO_LETRA)
                    raise Exception
    except FileNotFoundError:
        print(ERROR_ARCHIVO_SISTEMA_L)
        raise Exception


def formar_movimientos(tabla_conversion, iteraciones):
    '''Genera una cadena de comandos, con los movimientos que debe realizar la tortuga
    Pre: Recibe un diccionario con un formato de conversion ya especificado y un entero
    Post: Devuelve una cadena de la conversion de manera iterativa hecha tantas veces como las recibidas
    '''
    movimientos = tabla_conversion["axiomas"]
    movimientos_nuevo = ""
    for i in range(iteraciones):
        for letra in movimientos:
            if letra in tabla_conversion.keys():
                movimientos_nuevo += tabla_conversion[letra]
            else:
                movimientos_nuevo += letra
        movimientos = movimientos_nuevo
        movimientos_nuevo = ""
    return movimientos



def interpretar_comandos(cadena_comandos, operaciones, angulo, unidades_a_avanzar):
    '''Se encarga segun los comandos manejar a las tortugas e ir actualizando el canvas, de manera tal
    de conectar el sistema l con el movimento de las tortugas y generar los datos suficientes para el
    archivo svg.
    Pre: Recibe una cadena de comandos a realizar, una cadena con las operaciones validas,
    un entero que representa un angulo y la cantidad de unidades que avanza la tortuga
    Post: Genera la primera linea del archivo svg y una cola de tuplas con parametros para dar formato al svg
    '''
    pila_tortugas, cola_comandos, cordenada_minima, cordenada_maxima = inicializar()
    for letra in cadena_comandos:
        if letra not in operaciones:
            continue
        posicion_anterior, posicion_nueva = manejar_tortugas(letra, pila_tortugas, angulo, cola_comandos, unidades_a_avanzar)
        cordenada_minima, ancho, alto = actualizar_canvas(posicion_anterior, posicion_nueva, cordenada_minima, cordenada_maxima)
    primera_linea = f'<svg viewBox="{cordenada_minima[0] - 10} {cordenada_minima[1] - 10} {ancho + 15} {alto + 15}" xmlns="http://www.w3.org/2000/svg">'
    return primera_linea, cola_comandos


def inicializar():
    '''Se encarga de inicializar variables para luego ser utilizadas
    Pre: ---
    Post: Devuelve una pila de tortugas con una tortuga dentro, una cola de comandos
    vacia, las cordenadas minima y maxima
    '''
    pila_tortugas = Pila()
    cola_comandos = Cola()
    pila_tortugas.apilar(Tortuga())
    cordenada_minima = pila_tortugas.ver_tope().obtener_posicion()
    cordenada_maxima = pila_tortugas.ver_tope().obtener_posicion()
    return pila_tortugas, cola_comandos, cordenada_minima, cordenada_maxima


def manejar_tortugas(letra, pila_tortugas, angulo, cola_comandos, unidades_a_avanzar):
    '''Se encarga del manejo de tortugas, ejectudando los comandos, actualizando las posiciones
    y encolando los datos para dar formato al svg en caso de que la tortuga haya avanzado
    Pre: Recibe la letra del comando a ejecutar, una pila de tortugas, una cola de comandos,
    angulo al que debe girar la tortuga y cuantas unidades debe avanzar
    Post: Encola los datos en caso de haber avanzado y devuelve las posiciones antes y despues
    de ejecutar el comando.
    '''
    tortuga = pila_tortugas.ver_tope()
    posicion_anterior = tortuga.obtener_posicion_inicial()
    ejecutar_comando(letra, angulo, tortuga, pila_tortugas, unidades_a_avanzar)
    posicion_nueva = tortuga.obtener_posicion()
    if letra in 'FG':
        comando_svg = tortuga.obtener_parametros_svg()
        cola_comandos.encolar(comando_svg)
    tortuga.actualizar_posicion_inicial(posicion_nueva)
    return posicion_anterior,  posicion_nueva


def ejecutar_comando(letra, angulo, tortuga, pila_tortugas, unidades_a_avanzar):
    '''Ejecuta el comando segun la letra
    Pre: Recibe una letra que va a significar la accion a la tortuga recibida, una pila de tortugas
    si se debe apilar o desapilar una tortuga, un angulo para girar y cuantas unidades avanza la tortuga
    Post: Ejecuta el comando'''
    if letra in 'FG':
        tortuga.avanzar(unidades_a_avanzar)
    elif letra in 'fg':
        tortuga.avanzar_sin_dibujar(unidades_a_avanzar)
    elif letra == '+':
        tortuga.girar_derecha(angulo)
    elif letra == '-':
        tortuga.girar_izquierda(angulo)
    elif letra == '|':
        tortuga.voltear()
    elif letra == 'a':
        tortuga.cambiar_color(AZUL)
    elif letra == 'b':
        tortuga.cambiar_color(ROJO)
    elif letra == '1':
        tortuga.cambiar_grosor(1)
    elif letra == '2':
        tortuga.cambiar_grosor(2)
    elif letra == 'L':
        tortuga.circulo_svg()
    elif letra == '[':
        tortuga_nueva = Tortuga()
        tortuga.copiar_tortuga(tortuga_nueva)
        pila_tortugas.apilar(tortuga_nueva)
    elif letra == ']':
        pila_tortugas.desapilar()


def actualizar_canvas(posicion_anterior, posicion_nueva, cordenada_minima, cordenada_maxima):
    '''Actualiza el ancho, alto del canvas, fijandose cual fue la cordenada minima tanto para X como para Y, y
    analogamente para la cordenada maxima
    Pre: Recibe 4 listas, dos con las posiciones de la tortuga, otras dos con las cordenadas minimas y maximas,
    por las que en algun momento paso la tortuga.
    Post: Actualiza el ancho, alto del canvas y devuelve la cordenada minima para actualizar el origen de coordenadas
    '''
    eje_x = [posicion_anterior[0], posicion_nueva[0]]
    eje_y = [posicion_anterior[1], posicion_nueva[1]]
    if max(eje_x) > cordenada_maxima[0]:
        cordenada_maxima[0] = max(eje_x)
    if max(eje_y) > cordenada_maxima[1]:
        cordenada_maxima[1] = max(eje_y)
    if min(eje_x) < cordenada_minima[0]:
        cordenada_minima[0] = min(eje_x)
    if min(eje_y) < cordenada_minima[1]:
        cordenada_minima[1] = min(eje_y)
    ancho = abs(cordenada_minima[0]) + abs(cordenada_maxima[0])
    alto = abs(cordenada_minima[1]) + abs(cordenada_maxima[1])
    return cordenada_minima, ancho, alto



def escribir_archivo_svg(ruta, primera_linea, sucesion_comandos):
    '''Escribe el archivo svg con el formato correspondiente
    Pre: Recibe el nombre de una ruta a escribir, la primera linea a escribir y una cola de tuplas las cuales
    serviran para darle formato a una cadena que se escribiran en el orden el cual se vayan desencolando
    Post: Escribio el archivo
    '''
    if sucesion_comandos == None:
        print(MENSAJE_ERROR)
        raise Exception
    with open(ruta, 'w', encoding = 'utf8') as archivo:
        archivo.write(f'{primera_linea}\n')
        while not sucesion_comandos.esta_vacia():
            parametros = sucesion_comandos.desencolar()
            archivo.write(f'<line x1="{parametros[0]}" y1="{parametros[1]}" x2="{parametros[2]}" y2="{parametros[3]}" stroke-width="{parametros[4]}" stroke="{parametros[5]}"  />\n')
        archivo.write('</svg>')


algo_fractales()
