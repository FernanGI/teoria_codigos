#!/usr/bin/env python
# coding: utf-8


import numpy as np



import cv2





import time as t




from math import floor, ceil
from sys import getsizeof
from PIL import Image
import PIL.Image as im
import matplotlib.pyplot as plt


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


def comprimir_imagen(ruta, H, n, k):
    #La imagen comprimida
    imagen_comprimida= []

    # Lector imagen
    lector_imagen = cv2.imread(ruta)

    #Paso la imagen a array
    array_imagen = imagen_to_array(lector_imagen)

    #Saco el numero de palabras completas
    num_palabras_completas = floor(len(array_imagen) / n)


    resto = []
    if ((len(array_imagen) / n) % 1 != 0):
        resto = array_imagen[num_palabras_completas*n:]

    array_dividido = np.array(array_imagen[:num_palabras_completas*n]).reshape([num_palabras_completas,n])

    esta =[]
    for palabra in array_dividido:
        palabra = list(palabra)
        #Calculamos el síndrome
        sindrome = np.dot(palabra, H.transpose())
        sindrome = [i % 2 for i in sindrome]

        #Si pertenece al código
        if 1 not in sindrome :
            #Saco los bits de datos
            palabra_comprimida =["C"] + palabra[:k]
            esta.extend(palabra[:k])

        #Sino pertenece al código lo escribo
        else:
            palabra_comprimida =["N"]+palabra
            esta.extend(palabra)

        imagen_comprimida.extend(palabra_comprimida)
     #Si hay una parte lo añado
    if (int(len(array_imagen) / n) != (len(array_imagen) / n) ):
        imagen_comprimida.extend(["X"]+resto)
        esta.extend(resto)


    estructura_imagen_comprimida = {"array": imagen_comprimida,
                                    "shape": lector_imagen.shape,
                                    "u_size": getsizeof(array_imagen),
                                    "c_size": getsizeof(esta),
                                       "resto":len(resto)}
    return estructura_imagen_comprimida


def descomprimir_imagen(imagen_comprimida, G, k,n):
    imagen = []
    retorno = []

    #Vector con la imagen comprimida
    vector_imagenes = imagen_comprimida["array"]

    #Leo la imagen
    indice = 0
    while indice < len(vector_imagenes):
            esta_comprimido = vector_imagenes[indice]
            indice +=1

            if esta_comprimido== "X":

                palabra_descomprimida=vector_imagenes[indice:]
                indice += len(vector_imagenes[indice:])
            else:
                if esta_comprimido=="C":
                    palabra = vector_imagenes[indice:indice +k]
                    palabra_descomprimida = np.dot( palabra,G)

                    indice += k

                else:
                    palabra_descomprimida = vector_imagenes[indice:indice +n]
                    indice += n

            imagen.extend(palabra_descomprimida)

            

    #Creo la imagen
    #Lo agrupo de 8 en 8 bits

    imagen_8_bits = np.array(imagen).reshape(int(len(imagen)/8),8)
    retorno = np.array([int(sum([v[i]*2**(len(v)-i) for i in range(len(v))])/2)for v in imagen_8_bits])

    imagen_descomprimida = np.array(retorno).reshape(imagen_comprimida["shape"])
    return imagen_descomprimida



#Codigo de Hamming(7,4)
G = [[1,1,0,1,0,0,0],
     [0,1,1,0,1,0,0],
     [1,1,1,0,0,1,0],
     [1,0,1,0,0,0,1]]

H= [[1,0,0,1,0,1,1],
    [0,1,0,1,1,1,0],
    [0,0,1,0,1,1,1]]
n,k=7,4





#H= [[1,0,0,1],[0,1,0,1],[0,0,1,1]]
#G= [1,1,1,1]
#3,1





H=[[1,0,1],[0,1,1]]
G=[1,1,1]
n,k=3,1
uG = np.array(G).transpose()
print(G,uG)




#6,3
G=[[1,0,1,1,0,1],
   [1,1,0,0,1,0],
   [0,1,1,0,0,1]]
H=[[1,0,0,1,1,0],[0,1,0,0,1,1],[0,0,1,1,0,1]]
n,k=6,3




#H 15 ,11
H=[[1,0,0,0, 1,0,0,1,1,0,1,0,1,1,1],
   [0,1,0,0, 1,1,0,1,0,1,1,1,1,0,0],
   [0,0,1,0, 0,1,1,0,1,0,1,1,1,1,0],
   [0,0,0,1, 0,0,1,1,0,1,0,1,1,1,1]]

G=[[1,1,0,0, 1,0,0,0,0,0,0,0,0,0,0],
   [0,1,1,0, 0,1,0,0,0,0,0,0,0,0,0],
   [0,0,1,1, 0,0,1,0,0,0,0,0,0,0,0],
   [1,1,0,1, 0,0,0,1,0,0,0,0,0,0,0],
   [1,0,1,0, 0,0,0,0,1,0,0,0,0,0,0],
   [0,1,0,1, 0,0,0,0,0,1,0,0,0,0,0],
   [1,1,1,0, 0,0,0,0,0,0,1,0,0,0,0],
   [0,1,1,1, 0,0,0,0,0,0,0,1,0,0,0],
   [1,1,1,1, 0,0,0,0,0,0,0,0,1,0,0],
   [1,0,1,1, 0,0,0,0,0,0,0,0,0,1,0],
   [1,0,0,1, 0,0,0,0,0,0,0,0,0,0,1]]
n, k = 15,11




H=np.array(H)
G=np.array(G)

comprimida = comprimir_imagen("lena512color.tiff", H, n, k)

print(comprimida["array"][-15:])

img4= descomprimir_imagen(comprimida, G, k,n)



print("Tamaño comprimida: ", comprimida["c_size"], "Tamaño descomprimida: ", comprimida["u_size"],"Tamaño original: ",getsizeof(a), "Ratio: ",float(comprimida["c_size"])/float(comprimida["u_size"]))
