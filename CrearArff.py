#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:54:02 2020

@author: adrian
"""
from sklearn.feature_extraction.text import TfidfVectorizer
cv = TfidfVectorizer()
import pandas as pd
import re
import pyfreeling
import sys
sys.path.append('/home/adrian/legibilidad')
import legibilidad.legibilidad
import os
from os import listdir
from os.path import isfile
import natsort
import COWDict
sys.path.append('/home/adrian/Documentos')
import refranes
import ordinales



"""Recorre un texto, lo separa palabra a palabra, etiqueta
cada palabra e imprime estos resultados en un fichero con el mismo
nombre que su predecesor, pero con las palabras etiquetadas (Freeling)"""
def ProcessSentences(ls, texto):
    
        
    # for each sentence in list
    for s in ls :
        # for each word in sentence
        for w in s :
            # print word form  
            print("Palabra '"+w.get_form()+"'","Selected Analysis: ("+w.get_lemma()+","+w.get_tag()+")", file=open("Etiquetas"+texto+".csv", "a"))
            # print possible analysis in word, output lemma and tag
            #print("  Possible analysis: {",end="", file=open("ResultadosP.csv", "a"))
            #for a in w :
                #print(" ("+a.get_lemma()+","+a.get_tag()+")",end="", file=open("ResultadosP.csv", "a"))
            #print(" }", file=open("ResultadosP.csv", "a"))
            #  print analysis selected by the tagger 
            #print("Selected Analysis: ("+w.get_lemma()+","+w.get_tag()+")", file=open("ResultadosAnalizador.csv", "a"))
        # sentence separator
        print("", file=open("Etiquetas"+texto+".csv", "a"))
    

"""Inspecciona un directorio y devuelve una lista con todos los 
ficheros que encuentra"""
def todosTextos():
    lst = os.listdir("/home/adrian/FreeLing/APIs/python3/creaCorpus/CorpusLFRedm")
    lst = natsort.natsorted(lst)
    return lst

def textos():
    
    path = "/home/adrian/FreeLing/APIs/python3/creaCorpus/CorpusLFRedm"
    comienzo = re.compile('Etiquetas')
    final = re.compile('py')
    orden = re.compile('Orden')
    readability = re.compile('Readability_')
    conjunto = re.compile('untoTemporal')
    lst = [obj for obj in listdir(path) if isfile(obj)]
    
    for obj in listdir(path):
        
        if (comienzo.findall(obj)):
            lst.remove(obj)
    
    for obj in lst:
        if(readability.findall(obj)):
            lst.remove(obj)
            
    for obj in lst:
        if(final.findall(obj)):
            lst.remove(obj)
            
    for obj in lst:
        if(orden.findall(obj)):
            lst.remove(obj)
            
    for obj in lst:
        if(conjunto.findall(obj)):
            lst.remove(obj)
    
    lst = natsort.natsorted(lst)
    
    return lst

    

"""Devuelve un fichero con la lista de los documentos en "listaArchivos"
y sus indices clasicos de legibilidad"""

def DocumentAnalysis(listaArchivos):
    mu = legibilidad.legibilidad.mu
    
    for archivo in listaArchivos:
        
        filename = archivo
        comienzo = re.compile('Etiquetas.')
        if not(comienzo.findall(filename)):
            print("Indice mu para documento", filename, mu(archivo), file=open("IndicesTextos.csv", "a"))

def lectura(listaArchivos):
    textosLeidos = []
    for texto in listaArchivos:
        file = open(texto, 'rt', encoding = 'utf-8-sig')
        leido = file.read()
        textosLeidos.append(leido.lower())
        file.close()
    return textosLeidos


"""Devuelve una lista de los determinantes de un fichero
Requiere la version etiquetada de dicho fichero"""
def buscaDet(str, file):
    listaDet = [];
    for line in file:        
        for part in line.split():            
            if str == part:                
                listaDet.append(line);
    return listaDet
    file.close()

"""Devuelve una lista de determinada palabra de un fichero
Requiere la version etiquetada de dicho fichero"""
def buscaPalabra(str, file, filename):       
    file = open(filename, 'rt', encoding="utf8")
    lista = [];
    for line in file:        
        for part in line.split():            
            if str in part:                
                lista.append(line);
    file.close()
    return lista

"""Establece una expresion regular en funcion de determianda cadena
de caracteres requerida"""
def buscaExpReg(er, fileName, lista):  
  file = open(fileName, 'rt', encoding="utf8")
  txt = str(file.read().replace('\n','\t'))
   
  patron = re.compile(er) #creamos un patrón de expresión regular a buscar
  lista = patron.findall(txt)
  file.close()
  return lista      

"""Funcion que busca y lista los verbos correspondientes
a cierta etiqueta"""
def buscaVerboER(tipoVerbo, file, lista):
    
    lista = []
    patronVerbo = "V."+tipoVerbo+"...."
    
    return buscaExpReg(patronVerbo, file, lista);
    
def sumastfidf(array, textos):
    sumas = []
    for documentos in array:
        suma = 0;
        for datos in documentos:
            suma = suma + datos 
        sumas.append(suma)
    return sumas

    
    

def my_maco_options(lang,lpath) :

    # create options holder 
    opt = pyfreeling.maco_options(lang);

    # Provide files for morphological submodules. Note that it is not 
    # necessary to set file for modules that will not be used.
    opt.UserMapFile = "";
    opt.LocutionsFile = lpath + "locucions.dat"; 
    opt.AffixFile = lpath + "afixos.dat";
    opt.ProbabilityFile = lpath + "probabilitats.dat"; 
    opt.DictionaryFile = lpath + "dicc.src";
    opt.NPdataFile = lpath + "np.dat"; 
    opt.PunctuationFile = lpath + "../common/punct.dat"; 
    return opt;

"""Realiza el procesado y etiquetado por Freeling de todo el 
conjunto de textos en listaTextos"""    
def formatoFreeling(listaTextos):
    
    
    for texto in listaTextos:
        final = re.compile('.py')
        orden = re.compile('Orden.')
        fles = re.compile('Flesch.')
        if not(final.findall(texto) or (orden.findall(texto)) or fles.findall(texto)):
            
            file = open(texto, 'rt', encoding="utf-8")
            text = file.read()
            lw = tk.tokenize(text)
        
            #Definir todos los parrafos
            # split list of words in sentences, return list of sentences
            ls = sp.split(lw)
            # perform morphosyntactic analysis and disambiguation
            ls = morfo.analyze(ls)
            ls = tagger.analyze(ls)
        
            ProcessSentences(ls,texto)
            file.close()
            
"""Crea un documento de texto en formato arff con todos los datos 
extraidos del conjunto de textos"""
def WordsAnalysis(listaArchivos, sumas):
    mu = legibilidad.legibilidad.mu
    flesch = legibilidad.legibilidad.fernandez_huerta
    i = 0
    print('@RELATION Readability_Corpus', file=open("Readability_Corpus.txt", "a"))
    print('\n', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE title STRING', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE WordsSentence NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE mu_index NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE FK_index NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_infinitive NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_participle NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_longWords NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_gerund NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_nouns NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_Main_Nouns NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_determinants NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_prepositions NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_signosPunt NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_adverbiosMente NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_superlativos NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Ratio_Comas/sentencia NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Ratio_Verbos/sentencia NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Frecuent_Words_Pg NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Medium_Frecuent_Words_Pg NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Not_Frecuent_Words_Pg NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE TFIDF_Sumatory NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_ordinales NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_numbers NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_puntos_suspensivos NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Pg_Refranes NUMERIC', file=open("Readability_Corpus.txt", "a"))
    print('@ATTRIBUTE Difficulty {EASY, DIFFICULT}', file=open("Readability_Corpus.txt", "a"))
    print('\n', file=open("Readability_Corpus.txt", "a"))
    print('@Data', file=open("Readability_Corpus.txt", "a"))
    print('\n', file=open("Readability_Corpus.txt", "a"))
    
    
    for archivo in listaArchivos:   
        trespuntos = "..."
        mayor = 0
        medio = 0
        menor = 0
        totalPal = 0  
        palabrasLargas = 0
        advMente = 0
        superlativos = 0
        refCont = 0
        puntosSuspensivos = 0
        titulo = archivo
        numeros = 0
        ordinal = 0
        comienzo = re.compile('Etiquetas')
        orden = re.compile('Orden.')
        if not((comienzo.findall(archivo)) or (orden.findall(archivo))):
            
            file = open(archivo, 'rt', encoding="utf-8-sig")
            text = file.read()
            for refran in refranes.lista_refranes:
                if refran.lower() in text:
                    refCont = refCont + 1
            for refran in refranes.lista_refranes:
                if refran in text:
                    refCont = refCont + 1
            for ordin in ordinales.lista_ordinales:
                if ordin.lower() in text:
                    ordinal = ordinal + 1
            for ordin in ordinales.lista_ordinales:
                if ordin in text:
                    ordinal = ordinal + 1   
            
                    
            if trespuntos in text:
                puntosSuspensivos = puntosSuspensivos + 1
                
            lw = tk.tokenize(text)
            #Definir todos los parrafos
            # split list of words in sentences, return list of sentences
            ls = sp.split(lw)
            # perform morphosyntactic analysis and disambiguation
            ls = morfo.analyze(ls)
            ls = tagger.analyze(ls)
            
            sentence_number = len(ls)
            mu_index = mu(text)
            FK_index = flesch(text)
            for s in ls:
                
                for w in s:
                    numeroSilabas = legibilidad.legibilidad.count_syllables(w.get_form())
                    if(numeroSilabas > 5 ):
                        palabrasLargas = palabrasLargas + 1
                    if("mente" in w.get_form()):
                        advMente = advMente +1
                    if("ísimo" in w.get_form()):
                        superlativos = superlativos + 1
                    totalPal = totalPal + 1
                    frequency_value = COWDict.FrecVal(w.get_form().lower())
                    if (frequency_value > 10):
                        mayor = mayor + 1
                    elif (frequency_value < 10 and frequency_value > 0.02):
                        medio = medio + 1
                    elif (frequency_value < 0.02):
                        menor = menor + 1
                    
                    if(w.get_form().isdigit()):
                        numeros = numeros + 1
                        
                        
            file.close()
            
            for e in listaArchivos:
                if archivo in e and ".csv" in e:
                    
                    filename = e
                    file = open(filename, 'rt', encoding="utf8")
                    Comas = buscaPalabra("Fc", file, filename)
                    
                    lista = []
                    listaI = buscaVerboER("I", filename, lista)
                    lista.clear()
                    listaP = buscaVerboER("P", filename, lista)
                    lista.clear()
                    listaG = buscaVerboER("G", filename, lista)
                    lista.clear()
                    NombresPropios = buscaPalabra("NP", file, filename)
                    nombresComunes = buscaPalabra("NC", file, filename)
                    determinantes = buscaPalabra("DA", file, filename)
                    preposiciones = buscaPalabra("SP", file, filename)
                    Puntuacion = buscaPalabra("Fp" and "Fz", file, filename)
                    
                    Pg_infinitive = ((len(listaI)/totalPal)*100)
                    Pg_participle = ((len(listaP)/totalPal)*100)
                    Pg_gerund = ((len(listaG)/totalPal)*100)
                    Pg_nouns = ((len(nombresComunes)/totalPal)*100)
                    Pg_Main_Nouns = ((len(NombresPropios)/totalPal)*100)
                    Pg_determinants = ((len(determinantes)/totalPal)*100)
                    Pg_prepositions = ((len(preposiciones)/totalPal)*100)
                    Ratio_CS = (len(Comas)/sentence_number)
                    Ratio_VS = ((len(listaI)+len(listaP)+len(listaG))/sentence_number)
                    signos = ((len(Puntuacion)/totalPal)*100)
                    Pg_palabrasLargas = (((palabrasLargas)/totalPal)*100)
                    Pg_adMente = (((advMente)/totalPal)*100)
                    Pg_superlativos = (((superlativos)/totalPal)*100)
                    Pg_mayor = (mayor/totalPal)*100
                    Pg_medio = (medio/totalPal)*100
                    Pg_menor = (menor/totalPal)*100
                    num_ordinales = (ordinal/totalPal)*100
                    numbers = (numeros/totalPal)*100
                    suspensivos = (puntosSuspensivos/totalPal)*100
                    refranero = (refCont/totalPal)*100
                    wordspsentence = (totalPal/sentence_number)
                    
                    Difficulty = 'EASY' 
                    print(titulo,',',wordspsentence,',',mu_index,',',FK_index,',',Pg_infinitive,',',Pg_participle,',',Pg_palabrasLargas,',',
                          Pg_gerund,',',Pg_nouns,',',Pg_Main_Nouns,',',Pg_determinants,',',Pg_prepositions,',',signos,',',Pg_adMente,',',Pg_superlativos,',',
                          Ratio_CS,',',Ratio_VS,',',Pg_mayor,',',Pg_medio,',',Pg_menor,',',sumas[i],',',num_ordinales,',',numbers,',',suspensivos,
                          ',', refranero,',',
                          Difficulty,',', file=open("Readability_Corpus.txt", "a"))
                    print('\n', file=open("Readability_Corpus.txt", "a"))
                    print("Preparado el documento: ", i , titulo)
                    file.close()
                    i = i+1
                    

def indicesFlesch(listaArchivos):
    flesch = legibilidad.legibilidad.fernandez_huerta
    for archivo in listaArchivos: 
        file = open(archivo, 'rt', encoding="utf-8-sig")
        text = file.read()
        FK_index = flesch(text)
        print(archivo," ", FK_index,'\n', file=open("listadoFlesch.txt", "a"))


## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------

# set locale to an UTF8 compatible locale 
pyfreeling.util_init_locale("default");

# get requested language from arg1, or English if not provided      
lang = "es"
if len(sys.argv)>1 : lang=sys.argv[1]

# get installation path to use from arg2, or use /usr/local if not provided
ipath = "/usr/local";
if len(sys.argv)>2 : ipath=sys.argv[2]

# path to language data   
lpath = ipath + "/share/freeling/" + lang + "/"
leng = ipath + "/share/freeling/" 
# create language detector. Used just to show it. Results are printed
# but ignored (after, it is assumed language is LANG)
la=pyfreeling.lang_ident(leng+"common/lang_ident/ident-few.dat");

# create analyzers
tk=pyfreeling.tokenizer(lpath+"tokenizer.dat");
sp=pyfreeling.splitter(lpath+"splitter.dat");

# create the analyzer with the required set of maco_options  
morfo=pyfreeling.maco(my_maco_options(lang,lpath));
#  then, (de)activate required modules   
morfo.set_active_options (False,  # UserMap 
                          True,  # NumbersDetection,  
                          True,  # PunctuationDetection,   
                          True,  # DatesDetection,    
                          True,  # DictionarySearch,  
                          True,  # AffixAnalysis,  
                          False, # CompoundAnalysis, 
                          True,  # RetokContractions,
                          True,  # MultiwordsDetection,  
                          True,  # NERecognition,     
                          False, # QuantitiesDetection,  
                          True); # ProbabilityAssignment                 

# create tagger
tagger = pyfreeling.hmm_tagger(lpath+"tagger.dat",True,2)


            
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

formatoFreeling(textos())
corpus = lectura(textos())
#print(textos())
Y = cv.fit(corpus)
Y = cv.transform(corpus)
array = Y.toarray()
tf_idf = pd.DataFrame(Y.toarray(), columns = cv.get_feature_names())
sumas = sumastfidf(array, textos())
 
WordsAnalysis(todosTextos(), sumas)
#EtiquetasAnalysis(textos())
#DocumentAnalysis(textos())
print(textos())

