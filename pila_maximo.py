class _Nodo():
    def __init__(self,dato,prox = None):
        self.dato =dato
        self.prox = prox
class _Pila():
    def __init__(self):
        self.ult = None
    def apilar (self,dato):
        if self.ult == None:
            self.ult = _Nodo(dato)
        else:
            dato_a_agregar = _Nodo(dato,self.ult)
            self.ult = dato_a_agregar
    def desapilar(self):
        dato = self.ult.dato
        self.ult = self.ult.prox
        return dato
    def esta_vacia(self):
        if self.ult == None:
            return True
        return False
    def ver_tope(self):
        return self.ult.dato
class PilaConMaximo:
    def __init__(self):
        self.pila = _Pila()
        self.pila_m = _Pila()
    def apilar(self,dato):
        if self.pila.esta_vacia():
            self.pila_m.apilar(dato)
        elif self.pila.ver_tope() <= dato:
            self.pila_m.apilar(dato)
        self.pila.apilar(dato)
    
    def desapilar(self):
        dato = self.pila.desapilar()
        if dato == self.pila_m.ver_tope():
            self.pila_m.desapilar()
        return dato
    def obtener_maximo(self):
        if not self.pila_m.esta_vacia():
            return self.pila_m.ver_tope()
        return 'esta vacia'
    
l = PilaConMaximo()
l.apilar(1)
l.apilar(4)
l.apilar(3)
l.apilar(7)
l.apilar(1)
l.desapilar()
print(l.obtener_maximo())
l.desapilar()
print(l.obtener_maximo())
l.desapilar()
print(l.desapilar())
l.desapilar()

print(l.obtener_maximo())