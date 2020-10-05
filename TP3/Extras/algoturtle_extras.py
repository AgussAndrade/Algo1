from math import *

class _Nodo:

    def __init__(self, dato=None, prox=None):
        self.dato = dato
        self.prox = prox

class Cola:

    def __init__(self):
        self.prim = None
        self.ultimo = None

    def __len__(self):
        'Devuelve la longitud de la cola'
        actual = self.prim
        contador = 0
        while actual:
            contador += 1
            actual = actual.prox
        return contador

    def ver_primero(self):
        'Devuelve el dato del primer elemento de la cola'
        return self.prim.dato

    def encolar(self, dato):
        'Agrega un elemento a la cola'
        nuevo_nodo = _Nodo(dato)
        if self.ultimo is not None:
            self.ultimo.prox = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.prim = nuevo_nodo
            self.ultimo = nuevo_nodo

    def desencolar(self):
        'Saca el primer elemento de la cola'
        if self.esta_vacia():
            raise IndexError
        dato = self.prim.dato
        self.prim = self.prim.prox
        if not self.prim:
            self.ultimo = None
        return dato

    def esta_vacia(self):
        'Devuelve True si la cola esta vacia si no False'
        return self.ultimo == None

class Pila:

    def __init__(self):
        self.ult = None

    def apilar (self,dato):
        'Agrega un elemento a la pila'
        if self.ult == None:
            self.ult = _Nodo(dato)
        else:
            dato_a_agregar = _Nodo(dato,self.ult)
            self.ult = dato_a_agregar

    def desapilar(self):
        'Saca un elemento de la pila'
        dato = self.ult.dato
        self.ult = self.ult.prox
        return dato

    def esta_vacia(self):
        'Devuelve True si el atributo ultimo es igual a none si no False'
        return self.ult == None

    def ver_tope(self):
        'Devuelve el dato del ultimo nodo'
        return self.ult.dato


class Tortuga:
    '''Clase tortuga representa un punto en el origen de cordenadas, que mediante los distintos metodos va realizando acciones'''

    def __init__(self, orientacion = radians(90), posicion = [0,0], pluma = True, posicion_inicial = [0,0], grosor = 1, color = 'black'):
        '''Constructor de la clase tortuga, la cual tiene como atributos posicion (lista de dos numeros),
        orientacion (numero), pluma(True si esta abajo y False en caso contrario),
        posicion_inicial (lista de dos numeros), color (cadena que contiene el color en ingles) y ancho (numero)
        '''
        self.pluma = pluma
        self.posicion = posicion
        self.posicion_inicial = posicion_inicial
        self.orientacion = orientacion
        self.grosor = grosor
        self.color = color

    def __repr__(self):
        '''Representacion de la tortuga, muesta el estado de la pluma, su posicion y su orientacion'''
        return f'[{self.pluma},{self.posicion},{self.orientacion}]'

    def voltear(self):
        '''Da vuelta a la tortuga sumando el equivalente a 180 grados al atributo orientacion'''
        self.orientacion += radians(180)
        if self.orientacion > radians(360):
            self.orientacion -= radians(360)

    def girar_izquierda(self, cantidad):
        '''Recibe un numero y le resta el equivalente en radianes al atributo orientacion'''
        self.orientacion -= radians(cantidad)
        if self.orientacion > radians(360):
            self.orientacion -= radians(360)

    def girar_derecha(self, cantidad):
        '''recibe un numero y le suma su equivalente en radianes al atributo orientacion'''
        self.orientacion += radians(cantidad)
        if self.orientacion > radians(360):
            self.orientacion -= radians(360)

    def avanzar(self,cantidad):
        '''Avanza la cantidad de unidades pasadas por parametro (entero) en cada componente'''
        self.posicion[0] -= cantidad * cos(self.orientacion)
        self.posicion[1] -= cantidad * sin(self.orientacion)

    def avanzar_sin_dibujar(self, cantidad):
        '''Levanta la pluma, avanza la cantidad de unidades pasadas por parametro, y baja la pluma'''
        self.pluma_arriba()
        self.avanzar(cantidad)
        self.pluma_abajo()

    def pluma_arriba(self):
        '''Sube la pluma haciendo que no escriba, cambiando el atributo pluma a False'''
        self.pluma = False

    def pluma_abajo(self):
        '''Baja la pluma haciendo que escriba, cambia el atributo pluma a True'''
        self.pluma = True

    def obtener_parametros_svg(self):
        '''Devuelve una tupla con los parametros para luego escribir el archivo svg'''
        x1, y1 = self.posicion_inicial
        x2, y2 = self.posicion
        grosor = self.grosor
        color = self.color
        return (x1, y1, x2, y2, grosor, color)

    def obtener_posicion_inicial(self):
        '''Devuelve la posicion_inicial de la tortuga'''
        return self.posicion_inicial[:]

    def obtener_posicion(self):
        '''Devuelve la posicion de la tortuga'''
        return self.posicion[:]

    def actualizar_posicion_inicial(self, posicion_nueva):
        '''Modifica in-place la posicion_inicial de la tortuga'''
        self.posicion_inicial = posicion_nueva

    def copiar_tortuga(self, tortuga_nueva):
        '''Copia los atributos de la tortuga a una tortuga nueva
        pero con la diferencia de que posicion inicial es igual a posicion
        '''
        tortuga_nueva.pluma = [self.pluma][:][0]
        tortuga_nueva.posicion_inicial = self.posicion[:]
        tortuga_nueva.posicion = self.posicion[:]
        tortuga_nueva.orientacion = [self.orientacion][:][0]
        tortuga_nueva.grosor = self.grosor
        tortuga_nueva.color = self.color


    def cambiar_color(self, color_nuevo):
        self.color = color_nuevo

    def cambiar_grosor(self, grosor_nuevo):
        self.grosor = grosor_nuevo
