# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:32:02 2017

@author: dpts
"""


        
        
        
def lecture_solution(file):
    fichier=open(file,'r')
    lignes=fichier.readlines()
    c=0
    i=0
    liste=[]
    for ligne in lignes:
        ligne=ligne.split()
        
        if ligne[0] =='+SOLUTION/ESTIMATE':
            j=i+2
            while ((lignes[j]).split())[0]!='-SOLUTION/ESTIMATE':
                if ((lignes[j]).split())[1]=='XPO' or ((lignes[j]).split())[1]=='YPO' or ((lignes[j]).split())[1]=='LOD':
                    j=j+1
                else:
                    
                    ligne_test=lignes[j].split()  
                    code=ligne_test[2]
                    STAX=float(ligne_test[8])
                    STAY=float((lignes[j+1].split())[8])
                    STAZ=float((lignes[j+2].split())[8])
                    liste+=[[code,STAX,STAY,STAZ]]
                    j+=3
            
            break
        i+=1
    return liste,j-(i+2)
            
            
            
            
print(lecture_solution('ilrsa.pos+eop.160105.v135.snx'))