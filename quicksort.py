def quicksort(lista):
	if len(lista) < 2:
		return lista
	izquierda,medio,derecha = partir(lista,len(lista) -1)
	return quicksort(izquierda) + [medio] + quicksort(derecha)
def partir(lista, fin):
	pivote = lista[0]
	izquierda = []
	derecha = []
	i = 1
	while i <= fin:
		if lista[i] < pivote:
			izquierda.append(lista[i])
			i += 1
		else:
			derecha.append(lista[i])
			i += 1
	return izquierda,pivote,derecha

print(quicksort([5,6,43,8,2,865,2,7,0,15,4]))