class _Nodo:
    def __init__(self,dato = None ,prox = None):
        self.prox = prox
        self.dato = dato

#class Pila:
#    def __init__(self):
#        self.ult = None
#    def apilar(self,dato):
#        if self.ult == None:
#            self.ult = _Nodo(dato)
#        else:
#            self.ult = _Nodo(dato,self.ult)
#    def desapilar(self):
#        dato = self.ult.dato
#        self.ult = self.ult.prox
#        return dato
#    def esta_vacia(self):
#        return self.ult == None
#    def ver_tope(self):
#        return self.ult.dato
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

class Cola:
    def __init__(self):
        self.ult = None
        self.prim = None
    def encolar(self,dato):
        if self.prim == None:
            self.prim = _Nodo(dato)
            self.ult = self.prim
        else:
            self.ult.prox = _Nodo(dato)
            self.ult = self.ult.prox
    def desencolar(self):
        dato = self.prim.dato
        self.prim = self.prim.prox
        return dato
    def esta_vacia(self):
        return self.prim == None
    def ver_primero (self):
        return self.prim.dato

class ListaEnlazadaOrdenada:
    def __init__(self):
        self.prim = None
    def insertar_ordenado(self,dato):
        if self.prim == None:
            self.prim = _Nodo(dato)
        else:

            if dato < self.prim.dato:
                self.prim = _Nodo(dato,self.prim)
                return
            anterior = self.prim
            actual = anterior.prox
            while actual != None:
                if dato < actual.dato:
                    anterior.prox = _Nodo(dato,actual)
                    return
                anterior = actual
                actual = anterior.prox
            anterior.prox = _Nodo(dato)
    def invertir(self):
        pila_aux = Pila()
        if self.prim == None:
            return
        elif self.prim.prox == None:
            return
        
        while self.prim:
            pila_aux.apilar(self.prim.dato)
            self.prim = self.prim.prox
        actual = self.prim
        while not pila_aux.esta_vacia():
            if self.prim == None:
                self.prim = _Nodo(pila_aux.desapilar())
                actual = self.prim
            else:
                actual.prox = _Nodo(pila_aux.desapilar())
                actual = actual.prox
    def __str__(self):
        cadena = '|'
        act = self.prim
        while act:
            cadena += f'{act.dato},'
            act = act.prox
        cadena += '|'
        return cadena
    

def es_piramidal(pila):
    pila_aux = Pila()
    respuesta = True
    actual =pila.desapilar()
    while not pila.esta_vacia():
        if actual < pila.ver_tope():
            respuesta = False
            pila.apilar(actual)
            while not pila_aux.esta_vacia():
                pila.apilar(pila_aux.desapilar())
            
            return respuesta
        pila_aux.apilar(actual)
        actual = pila.desapilar()
    pila.apilar(actual)
    while not pila_aux.esta_vacia():
        pila.apilar(pila_aux.desapilar())

    return respuesta

def filtrar_cola(colauria,f):
    cola_final= Cola()
    cola_aux = Cola()
    while not colauria.esta_vacia():
        dato = colauria.desencolar()
        if f(dato):
            cola_final.encolar(dato)
        cola_aux.encolar(dato)
    while not cola_aux.esta_vacia():
        colauria.encolar(cola_aux.desencolar())
    return cola_final

def reemplazar_pila(p,v_v,v_n):
    p_aux = Pila()
    while not p.esta_vacia():
        dato = p.desapilar()
        if dato == v_v:
            p_aux.apilar(v_n)
        else:
            p_aux.apilar(dato)
    while not p_aux.esta_vacia():
        p.apilar(p_aux.desapilar())

def eliminar_repetidos(pila):
    lista = []
    while not pila.esta_vacia():
        dato = pila.desapilar()
        if not dato in lista:
            lista.append(dato)
    for i in range(len(lista)):
        pila.apilar(lista[len(lista) -1 -i])
def es_palindromo(cola,largo):
    pila_aux = Pila()
    pila_2 = Pila()
    cadena_1 = ''
    cadena_2 = ''
    while not cola.esta_vacia():
        dato = cola.desencolar()
        cadena_1 += dato
        pila_aux.apilar(dato)
    while not pila_aux.esta_vacia():
        dato = pila_aux.desapilar()
        cadena_2 += dato
        pila_2.apilar(dato)
    if cadena_1 == cadena_2:
        respuesta = True
    else:
        respuesta = False
    while not pila_2.esta_vacia():
        cola.encolar(pila_2.desapilar())
    return respuesta
class TorreDeControl:
    def __init__(self):
        self.arribo = Cola()
        self.partida = Cola()
    def nuevo_arribo(self,dato):
        self.arribo.encolar(dato)
    def nueva_partida(self,dato):
        self.partida.encolar(dato)
    def ver_estado(self):
        cola_a = Cola()
        cola_p = Cola()
        cadena_a = 'Vuelos esperando para aterrizar: '
        cadena_p = 'Vuelos esperando para despegar: '
        while not self.arribo.esta_vacia():
            dato = self.arribo.desencolar()
            cadena_a += f'{dato} ,'
            cola_a.encolar(dato)
        while not self.partida.esta_vacia():
            dato = self.partida.desencolar()
            cadena_p += f'{dato},'
            cola_p.encolar(dato)
        while not cola_a.esta_vacia():
            self.arribo.encolar(cola_a.desencolar())
        while not cola_p.esta_vacia():
            self.partida.encolar(cola_p.desencolar())
        return f'''{cadena_a}.
{cadena_p}.'''
    def asignar_pista(self):
        if not self.arribo.esta_vacia():
            return f'el vuelo {self.arribo.desencolar()} aterrizo'
        elif not self.partida.esta_vacia():
            return f'el vuelo {self.partida.desencolar()} despego'
        else:
            return 'No hay aviones cerca xd'

def es_exprecion_matematica(cadena):
    'recibe una cadena como una expresion matematica y devuelve true en caso de que este bien formulados los corchetes,parentecis, etc. o False en caso contrario'
    abrir = '{[('
    cerrar = ']})'
    combinaciones = {']':'[','}':'{',')':'('}
    pila = Pila()
    for e in cadena:
        if e in abrir:
            pila.apilar(e)
        elif e in cerrar and not pila.esta_vacia() and combinaciones[e] == pila.ver_tope():
            pila.desapilar()
        elif e in cerrar and (pila.esta_vacia() or combinaciones[e] != pila.ver_tope()):
            return False
    if pila.esta_vacia():
        return True
    return False
