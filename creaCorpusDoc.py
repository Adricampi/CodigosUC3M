#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:48:34 2021

@author: adrian
"""

import re
import pyfreeling
import sys
import os


documentos = os.listdir("CorpusLFFaciles")

#esta funcion agrupa un objeto iterable en el numero n de iteraciones que quieras.
def grouper(iterable, n):
    
    args = [iter(iterable)]* n
    return zip(*args)


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
    
    #Con este bucle recorremos la lista de documentos, agrupamos por oraciones e imprimimos
    #esos grupos
    for texto in documentos:
        
    
        
        file = open('CorpusLFFaciles/'+texto, 'rt', encoding="utf-8")
        text = file.read()
        lw = tk.tokenize(text)
        
        #Definir todos los parrafos
        # split list of words in sentences, return list of sentences
        ls = sp.split(lw)
        # perform morphosyntactic analysis and disambiguation
        ls = morfo.analyze(ls)
        ls = tagger.analyze(ls)
        # for each sentence in list
        i = 1
        ii = 0
        
        for grupo in grouper(ls, 20):
            print("grupo ", i)
            if(ii<4):
                for s in grupo:
                    frase = ""
                    for w in s:
                        frase = (frase +" " + w.get_form())
                    print(frase, file=open("CorpusLFRedm/"+texto+str(i)+"Red", "a" ))
                i = i +1
                ii = ii+1
                
            
        file.close()