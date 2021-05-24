#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:52:45 2019

@author: adrian
"""

import pyfreeling
import sys
import os


"""This function is in charge of processing the sentences of a given text. 
It requires the argument "ls", which is the transformed text
by means of a series of options supplied by Freeling itself."""

def ProcessSentences(ls):
    if(os.path.isfile('ResultadosAnalizador.csv')):
        os.remove('ResultadosAnalizador.csv')
    # for each sentence in list
    for s in ls :
        # for each word in sentence
        for w in s :
            # print word form
            print("Palabra '"+w.get_form()+"'","Selected Analysis: ("+w.get_lemma()+","+w.get_tag()+")", file=open("ResultadosAnalizador.csv", "a"))
            # print possible analysis in word, output lemma and tag
            #print("  Possible analysis: {",end="", file=open("ResultadosP.csv", "a"))
            #for a in w :
                #print(" ("+a.get_lemma()+","+a.get_tag()+")",end="", file=open("ResultadosP.csv", "a"))
            #print(" }", file=open("ResultadosP.csv", "a"))
            #  print analysis selected by the tagger 
            #print("Selected Analysis: ("+w.get_lemma()+","+w.get_tag()+")", file=open("ResultadosAnalizador.csv", "a"))
        # sentence separator
        print("", file=open("ResultadosAnalizador.csv", "a"))
        
"""This function is part of the internal configuration of the Freeling library, it does not need to be touched."""
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
## ----------------------------------------------
## -------------    MAIN PROGRAM  ---------------
## ----------------------------------------------


"""These options are ready to configure the routes of the Freeling configuration."""
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
                            
                              
    # creamos el tagger
    tagger = pyfreeling.hmm_tagger(lpath+"tagger.dat",True,2)
                              
    # procesamos el texto de este input
    mainfile = "3-amor_original.pdf.txt"
    filess = open(mainfile, 'rt', encoding="utf-8")
    text = filess.read()
    
    #tokeniza cada sentencia input a una lista de palabras
    lw = tk.tokenize(text)
    #Definir todos los parrafos
    filess.close()
    # dividimos las palabras en sentencias, retornamos la lista de sentencias
    ls = sp.split(lw)
    
    # realizamos un analisis morfosintactico y de desambiguacion
    ls = morfo.analyze(ls)
    ls = tagger.analyze(ls)
        
    # Realiza en analisis de cada palabra   
    ProcessSentences(ls)
    filess.close()
    """if(os.path.isfile('ResultadosAnalizador.csv')):
    
        os.system("python Pruebas.py")"""
    