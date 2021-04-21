  def crear_arbol(freq):
        T = [[(freq[simbolo], simbolo)] for simbolo in freq]

        while len(T) > 3:

            arboles = []
            for i in range(sys.argv[3]):
                #Por si no hay suficientes para unir
                if len(T)<=2 :
                    break
                arboles.append( min(T))
                T.remove(arboles[i])

            nuevo_arbol = [(sum([arboles[i][0][0]for  i in range(len(arboles))]),)]+ arboles
            T.append(nuevo_arbol)


        arbol_izquierdo = min(T)
        T.remove(arbol_izquierdo)
        arbol_derecho = min(T)
        T.remove(arbol_derecho)
        nuevo_arbol = [(arbol_izquierdo[0][0]+arbol_derecho[0][0],), arbol_izquierdo, arbol_derecho]
        T.append(nuevo_arbol)


        T = [(1,),T[0], T[1]]
        return T

    #Constructor de la tabla de traducción del código Huffman.
    #Se recibe el arbol creado y se devuelve un diccionario con la clave la secuencias de bits y como definición la secuencia de 0 y 1 que hay que seguir
def construir_codigo( arbol_total):
        #Funcion que va recorriendo el arbol y añadiendo al diccionario
        def recorrer_arbol(arbol, codigo):
            #Para hojas solas
            if len(arbol) == 1:
                diccionario_codigo[arbol[0][1]]= codigo
            else:
                for i in range(len(arbol)):
                    if i != 0:#Para no ver la primera porque es una variable que dice el porcentaje que contiene
                        #Pongo el código relativo a esa rama
                        codigo_relativo = codigo + str(i-1)
                        #Si justo el que veo tiene longitud 2 es que es una hoja
                        if len(arbol[i])==2:
                            diccionario_codigo[arbol[i][1]]= codigo_relativo

                        else:
                            #Si tiene longitud 3 es que  hay hijo izquierdo e hijo derecho
                            recorrer_arbol(arbol[i], codigo_relativo)


        codigo = ""
        diccionario_codigo = {}
        recorrer_arbol(arbol_total, codigo)
        return diccionario_codigo

def crear_diccionario_huffman(fichero):
    #Función que recibe un texto y devuelve la tabla de correspondencias

    #Diccionario que almacena el número de apariciones de cada byte
    diccionario_simbolos = {}

    #Total almacena el número de bytes que ha leido
    total = 0

    #Mientras haya bytes por leer será True
    for linea in fichero:
        palabra= ""
        for letra in linea:
            if letra not in  (" " ,"\t","\n", ",", ";",".", "!","?","¿","¡",")","("," ", "\b"):
                palabra = palabra + letra
            else:

                if palabra in diccionario_simbolos.keys():
                    diccionario_simbolos[palabra]+= 1
                else:
                    diccionario_simbolos[palabra]= 1
                total += 1

                if letra in   diccionario_simbolos.keys():
                    diccionario_simbolos[letra]+=1
                else:
                    diccionario_simbolos[letra]=1
                total += 1
                palabra = ""

    #Diccionario con las frecuencias de cada símbolo

    diccionario_frecuencias = {}
    #Recorro todos los símbolos
    total = sum([ diccionario_simbolos[i] for i in diccionario_simbolos.keys()])

    for i in diccionario_simbolos.keys():
        diccionario_frecuencias[i] = diccionario_simbolos[i]/total

    #Construyo el arbol de huffman
    arbol =crear_arbol(diccionario_frecuencias)
    #A partir del arbol de huffman construyo la tabla de correspondencias que
    #lo vamos a llamar diccionario_codigo
    diccionario_codigo=construir_codigo(arbol)

    return diccionario_codigo


def escribir_codificacion(nombre_fichero, diccionario_codigo):
    #Esta función escribe el archivo codificado.
    #Recibe el nombre del fichero (sys.argv[1]) y el diccionario de la tabla de correspondencias
    #Y  crea dos archivos:
    # codificado.bin que contendrá el fichero codificado con el código huffman
    #   diccionario.txt que contendrá la tabla de correspondencias


    #Se abre en binario para poder leer byte a byte
    fichero_lector = open(nombre_fichero,"r")
    #Fichero que va a contener el fichero con la codificación de Huffman
    fichero_escrito = open("codificado.bin", "w")
    #Fichero que va a almacenar la tabla de correspondencias para su posterior
    #decodificación

    fichero_diccionario= open("diccionario.txt","w")


    #Escribo la extensión original del fichero
    extension = nombre_fichero.split(".")[-1]

    fichero_diccionario.write(extension+"\n")

    #Escribo la tabla de correspondencias
    for letra in diccionario_codigo.keys():
        letra_cambiada = letra
        escribir = diccionario_codigo[letra]+ "\t" +letra_cambiada+ "\n"
        fichero_diccionario.write(escribir)
    fichero_diccionario.close()



    #Leo el archivo a codificar mediante el código Huffman
    for linea in fichero_lector:
        palabra= ""
        for letra in linea:
            #print(letra, ord(letra), letra not in  (" " ,"\t","\n", ",", ";",".", "!","?","¿","¡",")","("," ") )
            if letra not in (" " ,"\t","\n", ",", ";",".", "!","?","¿","¡",")","("," ", "\b"):
                palabra += letra
            else:
                escribir = diccionario_codigo[palabra]
                fichero_escrito.write(escribir)

                fichero_escrito.write(diccionario_codigo[letra])
                palabra = ""
    fichero_escrito.close()
    fichero_lector.close()


def decodificar():
    #Esta función decodifica el archivo generando decodificado.extensión

    fichero_decodificar = open("codificado.bin","r")

    #Leo el archivo que contiene la tabla de correspondencias y creo la tabla de
    #correspondencias que se va a almacenar en diccionario_decodificar.
    fichero_diccionario= open("diccionario.txt","r")
    diccionario_decodificar = {}
    extension = fichero_diccionario.readline()
    for linea in fichero_diccionario:
        linea = linea.split("\t")
        #Quito el salto de linea
        linea[1]=linea[1][:-1]
        diccionario_decodificar[linea[0]]=linea[1]

    fichero_diccionario.close()
    #Creo el fichero decodificado que va a contener la decodificación del archivo
    #original mediante el uso del diccionario almacenado en diccionario.txt
    fichero_decodificado = open("decodificado."+extension[:-1], "w")


    for linea in fichero_decodificar:
            codigo = ""
            for i in linea:
                codigo += i
                if codigo in diccionario_decodificar.keys():
                    fichero_decodificado.write(diccionario_decodificar[codigo])
                    codigo = ""

    fichero_decodificado.close()
    fichero_decodificar.close()



def main():
  
    if int(sys.argv[3]) > 9:
        print("No es posible que haya un codigo {}-ario".format(sys.argv[3]))
        return
    if sys.argv[2][1]== "c":
        print("Codifico")
        fichero = open(sys.argv[1], "r")
        diccionario_huffman = crear_diccionario_huffman(fichero)

        escribir_codificacion(sys.argv[1], diccionario_huffman)
        fichero.close()
   
    if (len(sys.argv[2])==3 and sys.argv[2][2] == "d") or (len(sys.argv[2])==2 and sys.argv[2][1]== "d") or (len(sys.argv)== 2 and sys.argv[1][1]=="d"):
        print("Decodifico")
        decodificar()


if __name__ == "__main__":
    main()
