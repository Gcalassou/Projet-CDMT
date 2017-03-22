# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 09:52:44 2017

@author: dpts
"""

def lecture_ID(file):
    fichier=open(file,'r')
    lignes=fichier.readlines()
    c=0
    i=0
    liste=[]
    #T=np.zeros((nb_s,3))
    #print(T)
    for ligne in lignes:
        ligne=ligne.split()
        if ligne[0]=='+SITE/ID':
            j=i+2
            while ((lignes[j]).split())[0]!='-SITE/ID':
                ligne_test=lignes[j].split()
                code=ligne_test[0]
                DOMES=ligne_test[2]
                liste+=[[code,DOMES]]
                j+=1
        i+=1
    
    return(liste)
    

    
print(lecture_ID('ilrsa.pos+eop.160105.v135.snx'))