# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:50:18 2017

@author: dpts
"""

def lecture_fichier_ref(file):
    fichier=open(file,'r')
    lignes=fichier.readlines()
    i=0
    liste=[]
    for ligne in lignes:
        ligne=ligne.split()
        print(ligne[0])
        if i>700 :
            break
        if ligne[0] =='+SITE/ID':
            
            j=i+2
            
            while ((lignes[j]).split())[0]!='-SITE/ID':
                ligne_test=lignes[j].split()
                k=0
                while k<len(ligne_test):
                    
                    try:
                        float((ligne_test[k]))
                        
                    except ValueError:
                        del ligne_test[k]
                        k-=1
                    k+=1
                print(ligne_test)
                code=ligne_test[0]
                lon=ligne_test[2:5]
                lat=ligne_test[5:8]
                alti=ligne_test[8]
                liste+=[[code,lon,lat,alti]]
                j+=1
            break
      
        i+=1
    return liste
    
var=lecture_fichier_ref('fichier_ref')