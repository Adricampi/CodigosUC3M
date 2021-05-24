#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 09:53:12 2019

@author: adrian
"""
import re
import pyfreeling
import sys
sys.path.append('/home/adrian/legibilidad')
import os
import textstat
import legibilidad.legibilidad
import json
import CreaDict
import contadores
from nltk.corpus import wordnet as wn
from wordnet import Wordnet


## -----------------------------------------------
## Do whatever is needed with analyzed sentences
## -----------------------------------------------

## Muchas de las funciones a continuación no se usan, pero en su día las construí por si pudieran ser útiles en el futuro.

## -----------------------------------------------
## Sentencias en el texto
## -----------------------------------------------


mu = legibilidad.legibilidad.mu
Flesch = legibilidad.legibilidad.fernandez_huerta

    
def sentencias(ls):
    cont = 0
    
    #Escribimos el bucle para contar las sentencias
    for s in ls :
        cont = cont + 1
    print("Numero de sentencias en el texto: " , cont)

"""def sentPal(ls):
    # for each sentence in list
    mu = legibilidad.legibilidad.mu
    Flesch = legibilidad.legibilidad.fernandez_huerta
    cont = 0
    for s in ls :
        frase = ""
        # for each word in sentence
        for w in s :
            frase = frase + w.get_form()+" "
        print("Frase" , (cont+1), frase, file=open("ResultadosP.csv", "a"))    
        cont = cont + 1
        #print("SALTO DE FRASE:", cont)
        print("Indice mu para la sentencia",cont,":", mu(frase),file=open("ResultadosP.csv", "a"))
        print("Indice flesch para la sentencia",cont,":", Flesch(frase),file=open("ResultadosP.csv", "a"))

        print("\n", file=open("ResultadosP.csv", "a" ))"""
        

## -----------------------------------------------
## Palabras en el texto
## -----------------------------------------------
def Palabras(ls):
    # for each sentence in list
    for s in ls :
        # for each word in sentence
        cont = 0
        for w in s :
            # print word form  
            palabra = w.get_form()
            print(palabra +"\n")
            cont = cont + 1
        print("Numero de palabras: " , cont)
            



## -----------------------------------------------
## Set desired options for morphological analyzer
## -----------------------------------------------
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

def ProcessPalabra(lw):
    
    if(os.path.isfile("ResultadosPalabras.csv")):
        os.remove("ResultadosPalabras.csv")
    
    for w in lw:
        AnalisisPalabra = CreaDict.GestPalabras(CreaDict.datos, w.get_form().lower())
        print("La palabra",'"', w.get_form(),'"', AnalisisPalabra, file=open("ResultadosPalabras.csv", "a" ))  

def ImprimirPalabraJSON(lw):
    
    for w in lw:
        AnalisisPalabra = CreaDict.GestPalabras(CreaDict.datos, w.get_form().lower())
        
        Recomendacion = puntoComa(w.get_form()) or parentesis(w.get_form())
        palabras = {"Word": w.get_form(), "Results":AnalisisPalabra, "Recomendación": Recomendacion}
        ImprePal = json.dumps(palabras, ensure_ascii=False)
        print(ImprePal, file=open("ResultadosJSON.csv", "w" ))

def ImprimirSentsJSON(ls):
    
    cont = 0
    
    listaF = []
    for s in ls:
        contpal = 0
        cont = cont + 1
        frase = ""
        # for each word in sentence
        lista = []
        for w in s:
            contpal = contpal + 1
            AnalisisPalabra = CreaDict.GestPalabras(CreaDict.datos, w.get_form().lower())
            if(AnalisisPalabra == "es poco frecuente"):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Synonyms": "Sinónimo adecuado",}
            elif(w.get_form() == "(" or w.get_form() == ")"):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Recomendación": "Aconsejamos evitar el uso de paréntesis",}
            elif(w.get_form() == "[" or w.get_form() == "]"):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Recomendación": "Aconsejamos evitar el uso de corchetes",}
            elif(w.get_form() == "%" or w.get_form() == "&"):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Recomendación": "Aconsejamos evitar el uso de símbolos poco habituales",}
            elif(w.get_form() == "..."):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Recomendación": "Aconsejamos evitar el uso de puntos suspensivos",}
            elif(legibilidad.legibilidad.count_syllables(w.get_form()) >= 5 ):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Recomendación": "Aconsejamos evitar el uso de palabras de más de 5 sílabas",}
            elif("mente" in w.get_form()):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Recomendación": "Aconsejamos evitar el uso de adverbios terminados en mente",}
            elif("ísimo" in w.get_form()):
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra, "Recomendación": "Aconsejamos evitar el uso de superlativos",}
            
            else:
                palabras = {"Word": w.get_form(), "Frequency_value": CreaDict.Fvalue(w.get_form().lower()) , "Results":AnalisisPalabra}
            lista.append(palabras)
            if(w.get_form() == "." or w.get_form() == "," or w.get_form() ==";" or w.get_form() == ":" or w.get_form() == "/" or w.get_form() == "?" or w.get_form() == "¿"):
                frase = (frase + w.get_form())
            else:
                frase = (frase +" " + w.get_form())
            
            
        if (contpal > 20):
            fras = {"Sentence_number": cont, "Sentence": frase.strip(), "mu_Index": mu(frase), "Flesch-kincaid_index":Flesch(frase), "Words": lista, "Numero_Palabras": contpal,"Recomendación": "La frase es demasiado larga, recomendamos acortarla a menos de 20 palabras",
            }
        else:
            
            fras = {"Sentence_number": cont, "Sentence": frase.strip(), "mu_Index": mu(frase), "Flesch-kincaid_index":Flesch(frase), "Words": lista, "Numero_Palabras": contpal,
            
            }
        listaF.append(fras)
        
    return listaF
        #ImpreSent = json.dumps(fras, ensure_ascii=False)
        
        #print(ImpreSent, file=open("ResultadosJSON.csv", "a" ))
        #ImprimirPalabraJSON(s)
        
def JSONAnalysis(frases, palabras):
    lista = []
    Datos = {
            "Sentences_number": frases,
            "Words_number": palabras,
                "Verbs_Number_set":[
                    {"Infinitive_Verbs_number": len(contadores.buscaVerboER("I", fileName, lista)),
                     "Gerund_Verbs_number": len(contadores.buscaVerboER("G", fileName, lista)),
                     "Participle_Verbs_number": len(contadores.buscaVerboER("P", fileName, lista)),}],
                "Articles_number": len(contadores.buscaPalabra("DA", file)),
                "Preposition_number": len(contadores.buscaPalabra("SP", file)),
                "Dates_number": len(contadores.buscaPalabra("W", file)),
                "Proper_noun_number": len(contadores.buscaPalabra("NP", file))}
    
    return (Datos)
    #with open("Verbos.json", "w") as file:
            #json.dump(Datos, file, indent=3, ensure_ascii = False)
def jsonWordnet(lw):
    lista = []
    for w in lw:
        palabras = {"palabra":w.get_form(), "synsets":wn.synsets(w.get_form(),lang="spa"),}
        lista.append(palabras)
    
    return lista

#Funcion principal del programa, encargada de construir e imprimir en un fichero recien creado el JSON completo.
def ImprimirJSON(titulo, url, formato, tema, usuario, caracter, ls, frases, palabras):
    
    file = open(titulo, 'rt', encoding="utf-8")
    readtext = file.read()
    
    Datos = {
            "Title":titulo,
            "URL":url,
            "Format":formato,
            "Topic":tema,
            "Aimed_to":usuario,
            "Character":caracter,
                "Readability_Set":
                        {"Flesch-kincaid_Index": Flesch(readtext),"mu_Index": mu(readtext) }, 
                            "Sentences_Set": ImprimirSentsJSON(ls),
                            "Readability_Analysis_Set": JSONAnalysis(frases, palabras),
            }
    file.close()
    
        
    with open(fichero + "Resultados.json", "w") as file:
            json.dump(Datos, file, indent=3, ensure_ascii = False)
    
    """DatosFichero = json.dump(Datos, ensure_ascii=False)
    print(DatosFichero, file=open("ResultadosJSON.json", "a" ))"""


def sinsets(lw):
    lista = []
    for w in lw:
        palabra = ("palabra:" + w.get_form())
        Datos = wn.synsets(w.get_form(),lang="spa")
        lista.append(palabra)
        lista.append(Datos)
   
    return lista

        
def puntoComa(palabra):
    
    if (palabra == ";"):
        return "Recomendamos evitar el uso de punto y coma"
    else:
        return ""
    
def parentesis(palabra):
    if(palabra == "(" or ")"):
        return "Recomendamos evitar el uso de parentesis"
    else:
        return ""
    
    
        
"""def pruebaJSON(ls):
    
    frases = {"Frases": ImprimirSentsJSON(ls)}
    Datos = json.dumps(frases, ensure_ascii=False)
    print(Datos)"""
## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------
    
if __name__ == "__main__":
    
    

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
                              
    # process input text
    fichero = "3-amor_original.pdf.txt"
    url = "null"
    formato = "txt"
    tema = "trámites"
    usuario = "Adultos"
    caracter="Público"
    
    file = open(fichero, 'rt', encoding="utf-8")
    leido = file.read()
    
    fileName = "ResultadosAnalizador.csv"
    
    # tokenize input line into a list of words
    lw = tk.tokenize(leido)
    #Definir todos los parrafos
    
    # split list of words in sentences, return list of sentences
    ls = sp.split(lw)
    
    #sentPal(ls)
    # perform morphosyntactic analysis and disambiguation
    ls = morfo.analyze(ls)
    ls = tagger.analyze(ls)
    
    # Realiza en analisis de cada palabra   
    
    #Devuelve el total de palabras
    totalPalabras = len(lw)
    #Devuelve el total de sentencias
    totalSentencias = len(ls)
    
    
    #Devuelve el total de palabras del documento
    print("Numero de palabras en el texto: " , totalPalabras)
    
    #Devuelve el numero de sentencias del documento
    sentencias(ls)
    
    #Devuelve el idioma del documento
    print ("EL idioma del texto es: "+la.identify_language(leido)+"\n")
    
    LetrasMedia = textstat.textstat.avg_letter_per_word(leido)
    #Devuelve la media de letras por palabra de todo el documento
    print("Numero medio de letras por palabra: " , LetrasMedia)
    MediaSilabasPalabra = textstat.textstat.avg_syllables_per_word(leido)
    #Devuelve el Numero medio de sílabas por palabra de todo el documento
    print("Numero medio de sílabas por palabra: " , MediaSilabasPalabra)
    
    #Devuelve el indice Flesch.Kincaid (Fernandez Huertas en español) de todo el documento
    #Devuelve la interpretacion de dificultad en funcion del indice Fernandez Huertas obternido anteriormente
    
    print("indice flesch-kincaid del documento", Flesch(leido))
    print("indice mu del documento", mu(leido))
    #Devuelve la interpretacion de la comprensibilidad del texto en funcion del indice Gutierrez obtenido anteriormente
    #Devuelve la cantidad de sentencias del texto
    #print("Numero de sentencias en el texto:" , count_sentences(text))
    #Devuelve la cantidad de párrafos del texto
    #print("Numero de párrafos del texto:",count_paragraphs(text))
    #sentPal(ls)
    #mediaFrases(text)
    #mediaParrafos(text)
    #print("Numero de parrafos:", legibilidad.legibilidad.count_paragraphs(text))
    ProcessPalabra(lw)
    #ImprimirSentsJSON(ls)
    ImprimirJSON(fichero,url, formato, tema, usuario, caracter, ls, totalSentencias, totalPalabras)
    file.close()
    #pruebaJSON(ls)
    #JSONAnalysis(totalSentencias, totalPalabras)
    
    #print(sinsets(lw), file=open("Sinsets.csv","w"))
    







