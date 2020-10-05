def mergesort(lista):
    """Pre:recibe una lista de objetos comparables
    Post:la lista esta ordenada de menor a mayor"""
    if len(lista) <2 :
        return lista
    divisor = len(lista)//3
    izquierda = mergesort(lista[:divisor])
    medio = mergesort(lista[divisor:divisor*2])
    derecha = mergesort(lista[divisor*2:])
    return merge(izquierda,medio,derecha)

def merge(iz,m,d):
    i = 0
    j = 0
    k = 0
    lista = []
    while i < len(iz) and j < len(m):
        if iz[i] < m[j]:
            lista.append(iz[i])
            i +=1
            continue
        lista.append(m[j])
        j+=1
    lista += iz[i:]
    lista += m[j:]
    i = 0
    lista_2 = []
    while i < len(lista) and k < len(d):
        if lista[i] < d[k]:
            lista_2.append(lista[i])
            i +=1
            continue
        lista_2.append(d[k])
        k+=1
    lista_2 += lista[i:]
    lista_2 += d[k:]
    return lista_2
print(mergesort([1,5,3,7,6,3,9,2,5,9,2]))