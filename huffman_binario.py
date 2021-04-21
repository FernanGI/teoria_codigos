from collections.abc import Container, Iterable, Sized
from abc import abstractmethod
import sys
#Código creado por el propio IDE
class IMap(Container, Iterable, Sized):  # [imap
    @abstractmethod
    def __getitem__(self, key: "K") -> "T": pass
    @abstractmethod
    def __setitem__(self, key: "K", value: "T"): pass
    @abstractmethod
    def __delitem__(self, key: "K"): pass
    @abstractmethod
    def get(self, key: "K", default: "T"): pass
    @abstractmethod
    def setdefault(self, key: "K", default: "T") -> "T": pass
    @abstractmethod
    def keys(self) -> "Iterable<K> and Sized": pass
    @abstractmethod
    def values(self) -> "Iterable<T> and Sized": pass
    @abstractmethod
    def items(self) -> "Iterable<(K, T)> and Sized": pass  # ]imap


IMap.register(dict)  # []dict
#Codigo de la clase del arbol Huffman
class HuffmanConstructorCodigo:
    def __init__(self, crearArbol: "-> IMap<simbolo, str>"=dict):
        self.crearArbol = crearArbol
    def crear_arbol(self, freq: "IMap<simbolo, Real>") -> "arbol of simbolo":
        T = [[(freq[simbolo], simbolo)] for simbolo in freq]
        while len(T) > 1:
            arbol_izquierdo = min(T)
            T.remove(arbol_izquierdo)
            arbol_derecho = min(T)
            T.remove(arbol_derecho)
            nuevo_arbol = [(arbol_izquierdo[0][0]+arbol_derecho[0][0],), arbol_izquierdo, arbol_derecho]
            T.append(nuevo_arbol)
        return T[0]

    #Constructor de la tabla de traducción del código Huffman.
    #Se recibe el arbol creado y se devuelve un diccionario con la clave la secuencias de bits y como definición la secuencia de 0 y 1 que hay que seguir
    def construir_codigo(self, arbol_total):
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
    #Leo un byte
    byte = fichero.read(32)
    #Mientras haya bytes por leer será True
    while byte:
        total += 1
        #Si  está en el diccionario aumento las apariciones en 1
        if byte in diccionario_simbolos.keys():
            diccionario_simbolos[byte]+= 1
        #Si no está lo añado
        else:
            diccionario_simbolos[byte]= 1
        byte = fichero.read(32)
    #Vector con todos los símbolos del fichero
    letras = list(diccionario_simbolos.keys())
    #Diccionario con las frecuencias de cada símbolo
    diccionario_frecuencias = {}
    #Recorro todos los símbolos
    for i in letras:
        diccionario_frecuencias[i] = diccionario_simbolos[i]/total*100
    #Construyo el arbol de huffman
    arbol = HuffmanConstructorCodigo().crear_arbol(diccionario_frecuencias)
    #A partir del arbol de huffman construyo la tabla de correspondencias que
    #lo vamos a llamar diccionario_codigo
    diccionario_codigo= HuffmanConstructorCodigo().construir_codigo(arbol)

    return diccionario_codigo


def escribir_codificacion(nombre_fichero, diccionario_codigo):
    #Esta función escribe el archivo codificado.
    #Recibe el nombre del fichero (sys.argv[1]) y el diccionario de la tabla de correspondencias
    #Y  crea dos archivos:
    # codificado.bin que contendrá el fichero codificado con el código huffman
    #   diccionario.txt que contendrá la tabla de correspondencias


    #Se abre en binario para poder leer byte a byte
    fichero_lector = open(nombre_fichero,"rb")
    #Fichero que va a contener el fichero con la codificación de Huffman
    fichero_escrito = open("codificado.bin", "wb")
    #Fichero que va a almacenar la tabla de correspondencias para su posterior
    #decodificación

    fichero_diccionario= open("diccionario.txt","w")


    #Escribo la extensión original del fichero
    extension = nombre_fichero.split(".")[-1]

    fichero_diccionario.write(extension+"\n")

    #Escribo la tabla de correspondencias
    for letra in diccionario_codigo.keys():
        letra_cambiada = letra
        escribir = diccionario_codigo[letra]+ "\t" +letra_cambiada.hex()+ "\n"
        fichero_diccionario.write(escribir)
    fichero_diccionario.close()

    byte = fichero_lector.read(32)

    #Leo el archivo a codificar mediante el código Huffman
    while byte:
        #Traduzco el simbolo a la secuencias de 1 y  0
        escribir = diccionario_codigo[byte]
        #Escribo la secuencia de  1 y 0
        for letra in escribir:
            if letra == '1':
                letra = b'1'
            else:
                letra = b'0'

            fichero_escrito.write(letra)

        byte = fichero_lector.read(32)

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
        diccionario_decodificar[linea[0]]=bytearray.fromhex(linea[1])

    fichero_diccionario.close()
    #Creo el fichero decodificado que va a contener la decodificación del archivo
    #original mediante el uso del diccionario almacenado en diccionario.txt
    fichero_decodificado = open("decodificado."+extension[:-1], "wb")


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
    #Si se le pasa como argumento nombre_fichero -c o -cd
    if sys.argv[2][1]== "c":
        print("Codifico")
        fichero = open(sys.argv[1], "rb")
        diccionario_huffman = crear_diccionario_huffman(fichero)
        escribir_codificacion(sys.argv[1], diccionario_huffman)
        fichero.close()
    #Si se le pasa como argumento -d o -cd
    if (len(sys.argv[2])==3 and sys.argv[2][2] == "d") or (len(sys.argv[2])==2 and sys.argv[2][1]== "d") or (len(sys.argv)== 2 and sys.argv[1][1]=="d"):
        print("Decodifico")
        decodificar()


if __name__ == "__main__":
    main()
