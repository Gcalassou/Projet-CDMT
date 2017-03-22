# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:26:08 2017

@author: dpts
"""
import solution_estimate as sp
import numpy as np

def lecture_matrice_cov(file):
    fichier=open(file,'r')
    lignes=fichier.readlines()
    dim=sp.lecture_solution(file)[1]
    mat=np.zeros((dim,dim))
    print(mat.shape)
    i=0
    for ligne in lignes :
        ligne=ligne.split()
        if ligne[0]=='+SOLUTION/MATRIX_ESTIMATE':
            j=i+2
            
            while ((lignes[j]).split())[0]!='-SOLUTION/MATRIX_ESTIMATE':
                temp=[]
                ligne_test=lignes[j].split()
                PAR1=int(ligne_test[0])
                print(PAR1)
                PAR2=int(ligne_test[1])
                #print(PAR2)
                temp=ligne_test[2:]
                for i in range(len(temp)):
                    mat[PAR1-1][PAR2+i-1]=temp[i]
                
                    
                
                j+=1
        i+=1
    return mat
    
toto=lecture_matrice_cov('ilrsa.pos+eop.160105.v135.snx')
