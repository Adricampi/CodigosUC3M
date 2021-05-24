# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:03:08 2019

@author: adric
"""
import re
import os
filename = "ResultadosAnalizador.csv"
file = open(filename, 'rt', encoding="utf8")
print("Numero de lineas totales:", len(file.readlines()))
print("\n")
documento = file.read()
print(documento)
file.close()


def textos():
    return os.listdir("/home/adrian/FreeLing/APIs/python3/HomologosDificiles")

def DocumentAnalysis(listaArchivos):
    for archivo in listaArchivos:
        
        filename = archivo
        file = open(filename, 'rt', encoding="utf8")
        print("Numero de lineas totales:", len(file.readlines()))
        print("\n")
        documento = file.read()
        print(documento)
        Puntuacion = buscaPalabra("Fp" and "Fz", file)
        file.close()
    
#Creamos una funcion que nos permita buscar linea a linea en funcion de una cadena de caracteres determinada

def buscaDet(str, file):       
    listaDet = [];
    for line in file:        
        for part in line.split():            
            if str == part:                
                listaDet.append(line);
    return listaDet
    file.close()
#Esta funcion busca y retorna una lista de palabras que contengan el atributo
def buscaPalabra(str, file):       
    file = open(filename, 'rt', encoding="utf8")
    lista = [];
    for line in file:        
        for part in line.split():            
            if str in part:                
                lista.append(line);
    file.close()
    return lista


def buscaExpReg(er, fileName, lista):  
  file = open(fileName, 'rt', encoding="utf8")
  txt = str(file.read().replace('\n','\t'))
   
  patron = re.compile(er) #creamos un patrón de expresión regular a buscar
  lista = patron.findall(txt)
  file.close()
  return lista      

#Funcion que busca y lista los verbos correspondientes a cierta etiqueta
def buscaVerboER(tipoVerbo, file, lista):
    patronVerbo = "V."+tipoVerbo+"...."
    return buscaExpReg(patronVerbo, file, lista);


    
    
    

"""def mediaVerbos(lista):
    if lista == buscaVerboER("I", filename, lista):"""
        
    
"""def quitarLineasER(er, ifileName, ofileName):  
  ofile = open(ofileName, 'w', encoding="utf8") # todo menos lineas borradas
  logfile = open("logFileLineasBorradas.txt", 'w', encoding="utf8") # lineas borradas
  ifile = open(ifileName, 'rt', encoding="utf8")
   
  patron = re.compile(er)
  
  for line in file:        
     if patron.search(line)==None:
         ofile.write(line)
     else:
         logfile.write(line)
    
  ofile.close()
  logfile.close()
  ifile.close()
  return lista      


quitarLineasER("DA....| SP ", filename, "outSinVacias.txt")
"""


file = open(filename, 'rt', encoding="utf8")
Puntuacion = buscaPalabra("Fp" and "Fz", file)
file.close()
#print("Signos de puntuación: ", Puntuacion )
print("Numero de Signos de puntuación ", len(Puntuacion))

print("\n")

file = open(filename, 'rt', encoding="utf8")
TotPal = (len(file.readlines()) - len(Puntuacion))
print("Palabras totales:", TotPal)
print("\n")
#Busca expresiones Regulares (verbos)   

lista=[]
lista = buscaVerboER("I", filename, lista)
#print(lista)

InfVerb = len(lista)
print("Estos son los verbos en infinitivo: " , InfVerb)
print("\n")

print("Incidencia de verbos en infinitivo:", ((InfVerb/TotPal)*100),"%")
print("\n")
lista.clear()

lista = buscaVerboER("P", filename, lista)
#print(lista)
ParVerb = len(lista)
print("Estos son los verbos en participio: " , ParVerb)
print("\n")
    
print("Incidencia de verbos en participio:", ((ParVerb/TotPal)*100),"%")
print("\n")
    
lista.clear()
    

lista = buscaVerboER("G", filename, lista)
#print(lista)
GerVerb = len(lista)
print("Estos son los verbos en gerundio: " , GerVerb)
print("\n")

print("Incidencia de verbos en gerundio:", ((GerVerb/TotPal)*100),"%")
print("\n")
lista.clear()
#seleccionamos las lineas que nos interesan
file = open(filename, 'rt', encoding="utf8")
determinantes = buscaPalabra("DA", file)
#file.close()
#print("estos son los determinantes", determinantes)
print("numero de determinantes ", len(determinantes))
lista.clear()
print("\n")

file = open(filename, 'rt', encoding="utf8")
preposiciones = buscaPalabra("SP", file)
file.close()
#print("estas son las preposiciones", preposiciones)
print("numero de preposiciones", len(preposiciones))

file.close()
print("\n") 
file = open(filename, 'rt', encoding="utf8")
nombresComunes = buscaPalabra("NC", file)
file.close()
#print("estos son los nombres comunes", nombresComunes )
print("numero de nombres comunes ", len(nombresComunes))
lista.clear()
print("\n")

file = open(filename, 'rt', encoding="utf8")
Fechas = buscaPalabra("W", file)
file.close()
#print("Fechas del documento: ", Fechas )
print("Numero de fechas ", len(Fechas))
lista.clear()
print("\n")

file = open(filename, 'rt', encoding="utf8")
NombresPropios = buscaPalabra("NP", file)
file.close()
#print("Nombres propios: ", NombresPropios )
print("Numero de Nombres Propios ", len(NombresPropios))
lista.clear()
print("\n")

file = open(filename, 'rt', encoding="utf8")

