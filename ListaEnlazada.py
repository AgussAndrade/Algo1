class _Nodo:
    def __init__(self,dato = None,prox = None):
        self.dato = dato
        self.prox = None
class ListaEnlazada:
    def __init__(self):
        self.prim = None
    def append(self,dato):
        if self.prim == None:
            self.prim = _Nodo(dato)
        else:
            actual = self.prim
            while actual.prox:
                actual = actual.prox
            actual.prox = _Nodo(dato)
    def pop(self):
        anterior = None
        actual = self.prim
        while actual.prox:
            anterior = actual
            actual = actual.prox
        dato = actual.dato
        if anterior:
            anterior.prox= None
        else:
            self.prim = None
        return dato
    def __repr__(self):
        cadena = '|'
        actual = self.prim
        while actual:
            cadena += f'{actual.dato} ,'
            actual = actual.prox
        cadena += '|'
        return cadena
    def extend(self,le):
        actual = le.prim
        while actual:
            self.append(actual.dato)
            actual = actual.prox
    def remover_todo(self,elemento):
        anterior = None
        actual = self.prim
        while actual:
            prox = actual.prox
            if not anterior and actual.dato == elemento:
                self.prim = prox
                actual = prox
                continue
            elif anterior and actual.dato == elemento:
                anterior.prox = prox
                actual = prox
                continue
            anterior = actual
            actual = anterior.prox
    def duplicar_elemento(self,elemento):
        actual = self.prim
        while actual:
            if actual.dato == elemento:
                self.append(elemento)
            actual = actual.prox.prox
    def invertir(self):
        anterior = None
        act = self.prim
        prox = act.prox
        while prox:
            if not anterior:
                act.prox = None
                anterior = act
                act = prox
                prox = act.prox
            else:
                act.prox = anterior
                anterior = act
                act = prox
                prox = act.prox
        act.prox = anterior
        self.prim = act
    