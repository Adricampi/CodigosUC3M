#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:15:18 2020

@author: adrian
"""
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import natsort
from os import listdir
from os.path import isfile
import re
from io import StringIO



texto = ""

def textos():
    
    path = "/home/adrian/FreeLing/APIs/python3/testHospital"
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


def lectura(listaArchivos):
    textosLeidos = []
    for texto in listaArchivos:
        textosLeidos.append(convert_pdf_to_txt(texto))
    
    
    return textosLeidos
        


def convertpdftexto(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    fp.close()
    device.close()
    text = retstr.getvalue()
    retstr.close()
    return text

def convert_pdf_to_txt(listaArchivos):
    
    for texto in listaArchivos:
    
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(texto, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        maxpages = 0
        caching = True
        pagenos = set()
    
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                      
                                      caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
    
        fp.close()
        device.close()
        text = retstr.getvalue()
        retstr.close()
        
        print(text, file=open("/home/adrian/FreeLing/APIs/python3/ExpLF/CorpusLFParejas/PDFtextFaciles/"+texto+".txt", "a"))






def convert(listaArchivos, pages=None):
        
    
    for texto in listaArchivos:
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)
    
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
    
        infile = open(texto, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        print(text, file=open("/home/adrian/FreeLing/APIs/python3/testHospital/"+texto+".txt", "w"))
        print("Hemos transcrito el " + texto)
        

convert(textos())
##print(convertpdftexto("guia_internet_redes_sociales.pdf"))
##lectura(textos())



"""
from PyPDF2 import PdfFileReader

def extract_information(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
        

    txt = f
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    texto : {texto}
    

    print(txt)
    return information

if __name__ == '__main__':
    path = '1._bases_ayudas_emprendimiento_2018_lf.pdf'
    extract_information(path)
"""
