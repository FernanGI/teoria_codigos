import numpy as np
import cv2
import time as t
from math import floor
from sys import getsizeof
from PIL import Image
import PIL.Image as im


def imagen_to_array(img):
    # Img será un objeto de tipo scipy.misc con la imagen
    array_imagen = []
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            # Recorro cada banda, R, G , B
            for b in range(0, 3):
                palabra = img[i][j][b]
                # Lo pasamos a binario
                palabra = (bin(palabra)[2:]).zfill(8)
                # Lo pasamos a una lista de 0,1
                lista = [int(k) for k in str(palabra)]
                array_imagen += lista
    return array_imagen

def comprimir_palabra(v, H, k):
    sindrome = np.dot(H, v)
    sindrome = [i % 2 for i in sindrome]
    dev = v
    # Búsqueda de la comlumna correspondiente al sindrome y se codifica:

    for col in range(len(H[0, :])):
        # Para que se cumpla en todas las posiciones
        if (H[:, col] == sindrome).all():
            dev[col] = (dev[col] + 1) % 2
            break
    return dev[:k]

def comprimir_imagen(ruta, H, n, k):
    #La imagen comprimida
    imagen_comprimida= []
    # Lector imagen
    lector_imagen = cv2.imread(ruta)
    print(lector_imagen)
    print("________________________")
    #Paso la imagen a array
    array_imagen = imagen_to_array(lector_imagen)
    #Saco el numero de palabras completas
    num_palabras_completas = floor(len(array_imagen) / n)
    # Parte de compresón
    for i in range(num_palabras_completas - 1):
        palabra = array_imagen[i * n: i * n + n]
        palabra_comprimida = comprimir_palabra(palabra, H, k)
        imagen_comprimida.extend(palabra_comprimida)
    # Para los bits completos
    if ((len(array_imagen) / n) % 1 != 0):
        inicio =(num_palabras_completas-1)*n+1
        imagen_comprimida.extend(array_imagen[(num_palabras_completas-1)*n:])
    estructura_imagen_comprimida = {"array": imagen_comprimida,
                                    "shape": lector_imagen.shape,
                                    "u_size": getsizeof(array_imagen),
                                    "c_size": getsizeof(imagen_comprimida)}
    return estructura_imagen_comprimida


def descomprimir_imagen(imagen_comprimida, G, j):
    imagen = []
    retorno = []
    num_palabras_completas = floor(len(imagen_comprimida["array"]) / j)
    # Decodificación de palabra
    for i in range(num_palabras_completas - 1):
        palabra = imagen_comprimida["array"][i * j : i * j + j]

        original = np.dot(palabra, G)
        original = [i % 2 for i in original]
        imagen.extend(original)
    # Agregamos el final de la imagen
    if ((len(imagen_comprimida["array"])/float(j)) % 1 != 0.):
        inicio = (num_palabras_completas - 1) * j + j
        imagen.extend(imagen_comprimida["array"][inicio:])
    for i in range(int(len(imagen)/8)):
        numero = imagen[ i * 8 : i * 8 + 8]

        retorno.append(255 - int("".join(map(str,numero)),2))
    # Agregamos los bits que nos falten debido a los errores de redondeo
    while(len(retorno) != (imagen_comprimida["shape"][0] * imagen_comprimida["shape"][1] * imagen_comprimida["shape"][2])):
        retorno.append(0)
    imagen_descomprimida = np.array(retorno).reshape(imagen_comprimida["shape"])
    return imagen_descomprimida




#Codigo de Hamming(7,4)
#Gt = [[1,1,0,1],[1,0,1,1],[1,0,0,0],[0,1,1,1],[0,1,0,0],[0,0,1,0], [0,0,0,1]]
#H= [[1,0,1,0,1,0,1],[0,1,1,0,0,1,1],[0,0,0,1,1,1,1]]

#H= [[1,0,0,1],[0,1,0,1],[0,0,1,1]]
#G= [1,1,1,1]
#3,1
H=[[0,1,1],[1,0,1]]
G=[[1,1,1]]
#7,4,3
#H=[[0,0,0,1,1,1,1],[0,1,1,0,0,1,1],[1,0,1,0,1,0,1]]
H=np.array(H)
G=np.array(G)


n, k = 3,1
comprimida = comprimir_imagen("lena512color.tiff", H, n, k)
#comprimida = comprimir_imagen("lena.png", H, n, k)

img4 = descomprimir_imagen(comprimida, G, k)





print("Comprimir: ", t2 - t1, " Descomprimir: ", t3 - t2)
print("Tamaño comprimida: ", comprimida["c_size"], "Tamaño descomprimida: ", comprimida["u_size"], "Ratio: ",float(comprimida["c_size"])/float(comprimida["u_size"]))
