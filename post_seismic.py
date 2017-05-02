# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 14:28:06 2017

@author: Gabriel
"""
#import FtpBis as ftp
import numpy as np
import conversion as conv
from astropy.time import Time
import matplotlib.pyplot as plt
import options as opt

class seismic:
    def __init__(self):
#        self.path= 'ITRF2014-psd-slr.snx'
#        self.path = opt.fichier_ref_slr
        self.path='post_seismic_data.txt'
        
#    def data(self):
#        mon_ftp=ftp.Ftp('itrf.ign.fr',['incoming'])
#        mon_ftp.connexion_changeDir_download(self.path)
    
    
    def lecture_ID(self):
        fichier=open(self.path,'r')
        lignes=fichier.readlines()
        c=0
        i=0
        liste=[]
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
        
    def lecture_solution(self):
        """Fonction permettant de lire le bloc "SOLUTION/ESTIMATE"
        
        parametres
        fichier = fichier contenant les déformations seismique
        
        sortie
        -- liste : liste des données contenus dans le bloc
        -- j-(i+2) : renvoi le nombre d'éléments de la liste
        """
        fichier=open(self.path,'r')
        lignes=fichier.readlines()
        i=0
        liste=[]
        for ligne in lignes:
            ligne_test=ligne.split()
            
            if ligne_test[0] =='+SOLUTION/ESTIMATE':
                j=i+2
                while ((lignes[j]).split())[0]!='-SOLUTION/ESTIMATE':
                                        
                    type_data = (lignes[j])[7:13]
                    
                    code = (lignes[j])[14:18]
#                    print('test'+str(code))
                    epoch = (lignes[j])[27:39]
                    estimate_sol = float((lignes[j])[47:69])
                    liste+=[[type_data, code, epoch,estimate_sol]]
                    j+=1
                break
            i+=1
        return liste, j-(i+2)
        
    def lecture_matrice_cov(self):
        """Fonction permettant de lire le bloc "SOLUTION/MATRIX_ESTIMATE"
        
        sortie 
        -- mat : matrice contenant l'ensemble des données du bloc en question
        """
        fichier=open(self.path,'r')
        lignes=fichier.readlines()
        dim=self.lecture_solution()[1]
#        print(dim)
        mat=np.zeros((dim,dim))
#        print(mat.shape)
        i=0
        for ligne in lignes :
            ligne=ligne.split()
            if ligne[0]=='+SOLUTION/MATRIX_ESTIMATE':
                j=i+2
                
                while ((lignes[j]).split())[0]!='-SOLUTION/MATRIX_ESTIMATE':
                    temp=[]
                    ligne_test=lignes[j].split()
                    PAR1=int(ligne_test[0])
#                    print(PAR1)
                    PAR2=int(ligne_test[1])
                    #print(PAR2)
                    temp=ligne_test[2:]
                    for i in range(len(temp)):
                        mat[PAR1-1][PAR2+i-1]=temp[i]
                    
                        
                    
                    j+=1
            i+=1
        return mat
    
    def L(self,t):
        """Allow to calculate the total sum of the PSD correction express in a local frame 
        at the echo t (for the moment, this script calculate this just for one componente for 
        a GPS station)
        
        parameters
        t -- epoch t (format MJD)
        
        return : L
        
        """
        liste = self.lecture_solution()[0]
#        print(liste)
        a_exp, a_log=[],[]
        ti_exp, ti_log = [],[]
        t_exp, t_log = [],[]
        for i in range(len(liste)):
            if liste[i][1]=='7403':
                if liste[i][0]=='AEXP_E':
                    a_exp+=[[[liste[i][3]],[conv.convert_utc_mjd(liste[i][2])]]]
#                    ti_exp+=[liste[i][2]]
                if liste[i][0]=='ALOG_E':
                    a_log+=[[[liste[i][3]],[conv.convert_utc_mjd(liste[i][2])]]]
#                    ti_log+=[liste[i][2]]
                if liste[i][0]=='TEXP_E':
                    t_exp+=[liste[i][3]]
                if liste[i][0]=='TLOG_E':
                    t_log+=[liste[i][3]]
        
        print(a_exp)
        print(t_exp)
        sum_exp,sum_log=0,0
        for i in range(len(a_exp)):
            sum_exp+=a_exp[i][0]*(1-np.exp(-((t-a_exp[i][1])/365.25)/t_exp[i]))
        for j in range(len(a_log)):
            sum_log+=a_log[j][0]*np.log(1+((t-a_log[j][1])/365.25)/t_log[i])
        l=sum_exp+sum_log
        return l
        
    def tracer_deformation(self):
        nt  = Time.now()
        nt.format = 'mjd'
        t=np.arange(0, nt.value, 1)
        plt.plot(t, self.L(t))
        plt.show()
        
        
                


    
if __name__ == '__main__':
    s = seismic()
    identification = s.lecture_ID()
    solution = s.lecture_solution()
    matrice = s.lecture_matrice_cov()
##    l=s.L()
    s.tracer_deformation()
#    print (ID)
#    print(solution)
#    print(matrice)
#    print(l)
    