import csv
import sys
import random
_a = sys.argv
_prueba = ['algotweets.py','generar','erescurioso','alex_riveiro']
PEDIDO = _a
AYUDA = '''Bienvenido, abriste el archivo sin ningun comando, sus comandos son:
1. generar / generar {usuario}
2. favoritos
3. trending'''
RECHAZO = 'no me estas pidiendo nada, o lo pediste mal'
GENERANDO_TW = f' generando tweet a partir de {",".join(PEDIDO[2::])} '
NO_ES_USER = f'{" y/o ".join(PEDIDO[2::])} no es un usuario'
ER_FV = 'no pusiste un numero de lineas de favoritos'
ER_TR = 'No pusiste un entero para poder escribir los favoritos'
ER_CARPETA ='La carpeta en la cual se encuentra no dispone del archivo necesario para continuar'
ARCH_TW ='tweets.csv'
ARCH_FV = 'favs.txt'

def main ():
    'agarra la global pedido usuario e imprime lo que devuelva la funcion entender_usuario'
    
    respuesta = entender_usuario()
    print(respuesta)
def prevenir():
    'mira si se puso 2 o mas veces el mismo usuario y acomoda el PEDIDO para que no rompa'
    for i in range(2):
        t = 0
        for comando in PEDIDO:
            c = 0
            t += 1
            for comandito in PEDIDO:
                c+=1
                if comandito == comando and c != t:
                    PEDIDO.pop(PEDIDO.index(comandito))  
def entender_usuario():
    'recibe un pedido en una lista y si la segunda componente esta dentro de los parametros generar, favoritos o trending les aplica sus respectivas funciones'
    if PEDIDO == ['algotweets.py']:
        return AYUDA
    if len(PEDIDO) >= 2:
        
        if PEDIDO[1] == 'generar':
            prevenir()   
            return(generar())
    if len(PEDIDO) == 2 or len(PEDIDO) == 3:
        
        if PEDIDO[1] == 'favoritos':
            return(favoritos())
    if len(PEDIDO) == 3:
        if PEDIDO[1] == 'trending':
            return(trending())
    
    return(RECHAZO)

def generar(): 
    'imprime el tweet generado a partir de la lista pedido y si el usuario acepta lo copia en el archivo favs a partir de sus respectivas funciones'

    dic_de_guardado = guardar_palabras()
    lista_primeras =[]
    tweet_generado = []
    
    if dic_de_guardado == ER_CARPETA:
        return ER_CARPETA
    
    if not dic_de_guardado :
        print(NO_ES_USER)
        return ''
    print(GENERANDO_TW)

    for k in dic_de_guardado.keys():
        lista_primeras += [k]

    palabra_elegida = random.choice(lista_primeras)

    tweet_generado = [palabra_elegida]
    #print(tweet_generado)
        
    while revisar_caracteres(tweet_generado):
        if tweet_generado[len(tweet_generado) -1] in dic_de_guardado.keys():
            palabras_por_usuario =  dic_de_guardado[tweet_generado[len(tweet_generado) -1]]
        else:
            break
        tweet_generado += elegir_random(palabras_por_usuario) 
    tweet_final = acomodar(tweet_generado)
    print(tweet_final) 
    
    if preguntar_favorito() == True:
        poner_favorito(tweet_final)
    
    return 'listo'

def elegir_random(diccionario):
    lista = []
    valor_viejo = 0
    for k,v in diccionario.items():
        lista += [(k,valor_viejo+v)]
        valor_viejo += v
    num_elegido = random.randint(0,valor_viejo)
    for tupla in lista:
        if num_elegido <= tupla[1]:
            return [tupla[0]]
        
def revisar_caracteres (lista):
    'revisa que la lista en formato "oracion" no supere los 280 carecteres'
    caracteres = ' '.join(lista)
    
    if len (caracteres) >= 280:
        return False
    
    return True
               
def guardar_palabras ():
    'recibe una posicion y devuelve un diccionario con las palabras y sus siguientes que se encuentran en dicha posicion'
    dic_de_palabras = {}
    lista_de_user = []
    
    try:
    
        with open(ARCH_TW, encoding = 'utf8') as archivo_tweets:
            r = csv.reader(archivo_tweets, delimiter = '\t')
            linea = next ( r, None)
        
            while linea :
                contador = 0
             
                for i in PEDIDO[1::]:
                    if i in linea[0] or PEDIDO == ['algotweets.py','generar']:
                        lista_generadora = linea[1].split()
                        
                        user = linea[0]
                        if not user in lista_de_user and PEDIDO != ['algotweets.py','generar']:
                            lista_de_user += [user]
                                          
                        for palabra in lista_generadora:
                            dic_num = {}
                            if contador != 0:
                                palabra_anterior = lista_generadora[contador -1]
                            elif contador == 0:
                                contador += 1
                                continue
                            else:
                                
                                continue
                            dic_num[palabra] = dic_num.get(palabra,0) +1
                            if palabra_anterior in dic_de_palabras:
                                dic_de_palabras[palabra_anterior][palabra] = dic_de_palabras[palabra_anterior].get(palabra,0) + 1
                            else:
                                dic_de_palabras[palabra_anterior] = dic_num
                            contador +=1
                
                linea = next (r, None)
            
            if chequear_pedido(lista_de_user):
                return dic_de_palabras
            
            else:
                return None
    except FileNotFoundError:
        return ER_CARPETA 
def chequear_pedido(lista):
    ''' mira si en el diccionario con usuarios estan todos los que se piden si lo estan devuelve True si no devuelve False'''

    cantidad_de_usuarios = len(PEDIDO) -2
    
    if cantidad_de_usuarios == 0:
        return True
    
    if cantidad_de_usuarios == len(lista):
        return True
     
    return False

def acomodar(lista):
    'recibe una lista en "crudo" y la transforma en una cadena de maximo 280 caracteres'

    cadena_generada = ' '.join(lista)
    
    while len(cadena_generada) > 280:
        lista.pop()
        cadena_generada = ' '.join(lista)
   
    return cadena_generada

def preguntar_favorito():
    'pregunta al usuario y si escribe la letra s devuelve true si escribe la letra n devuelve false'
    
    while True:
        pregunta = input('desea guardar su tw en favorito? (s/n)' )
    
        if pregunta == 's' or pregunta == 'S':
            return True
        
        if pregunta == 'n' or pregunta == 'N':
            return False

def poner_favorito(tweet_generado):
    'recibe una cadena y la escribe en el archivo favs.txt'
    
    with open(ARCH_FV,'a', encoding = 'utf8') as archivo:
        
        return archivo.write(f'{tweet_generado}\n')

def favoritos ():
    'imprime las lineas del archivo favs.txt'
    lineas_pasadas = 0
    lista_lineas = []
    if PEDIDO[2:] != []:
        if not PEDIDO[2].isdigit():
            print(ER_FV)
            return 'listo'
    try:
        with open(ARCH_FV,'r+', encoding = 'utf8') as archivo:
            for linea in archivo:
                lista_lineas += [linea.rstrip('\n')]
        if len(PEDIDO) == 3 and PEDIDO[2].isdigit():
            lineas_pasadas = int(PEDIDO[2])
        else:
            lineas_pasadas = len(lista_lineas)
            
        if lineas_pasadas > len(lista_lineas):
            lineas_pasadas = len(lista_lineas)
        
        for i in range(lineas_pasadas-1,-1,-1):
            print(lista_lineas[i])
    except FileNotFoundError:
        print (ER_CARPETA)
        
    return 'listo'

def trending():
    'imprime las tendencias en base a la cantidad de "#" que hay en el texto tweets poniendo los que salen mas veces arriba'
    tendencias = {}
    tend_invertida = {}
    lista_a_escribir = []
    contador = 0
    if not PEDIDO[2].isdigit():
        print(ER_TR)
        return ''
    try:
        with open(ARCH_TW, encoding = 'utf8') as archivo:
            r = csv.reader(archivo, delimiter = '\t')
            linea = next ( r, None)
            
            while linea:
                lista_oracion = linea[1].split()
                for palabra in lista_oracion:
                    if '#' in palabra[0]:
                        tendencias[palabra] = tendencias.get(palabra,0) + 1
                linea = next(r,None)
            
            for palabra,cantidad in tendencias.items():
                tend_invertida[cantidad] = tend_invertida.get(cantidad,[]) +[palabra]
            
            for cantidad in tend_invertida.keys():
                lista_a_escribir += [cantidad] * len(tend_invertida[cantidad])
            lista_a_escribir = sorted(lista_a_escribir, reverse = True)
            
            numero_a_iterar = int(PEDIDO[2])
            if numero_a_iterar > len(lista_a_escribir):
                numero_a_iterar = len(lista_a_escribir)
            
            for relevancia in lista_a_escribir:
                for j in range(len(tend_invertida[relevancia])):
                    if contador == numero_a_iterar:
                        return 'listo'
                    print(f'{contador+1}.\t{tend_invertida[relevancia][j]} \n')
                    contador += 1
            return ''
    except FileNotFoundError:
        return ER_CARPETA
main()
