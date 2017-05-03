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
    
    def L(self, t):
        """Allow to calculate the total sum of the PSD correction express in a local frame 
        at the echo t (for the moment, this script calculate this just for one componente for 
        a GPS station)
        
        parameters
        t -- epoch t (format MJD)
        
        return : L
        
        """
        liste = self.lecture_solution()[0]
#        print(liste)
        a_exp_e, ti_exp_e, time_exp_e, a_log_e, ti_log_e, time_log_e = [], [], [], [], [], []
        a_exp_n, ti_exp_n, time_exp_n, a_log_n, ti_log_n, time_log_n = [], [], [], [], [], []
        a_exp_h, ti_exp_h, time_exp_h, a_log_h, ti_log_h, time_log_h = [], [], [], [], [], []

        station_temp = ''
        mat_station = np.zeros((3,5))
        liste_station_matrice = []
        k=0
        resultat =[]
        while k != len(liste)-1:
            if station_temp == '':
                station_temp = liste[k][1]
            if liste[k][1]==station_temp:
#                print(liste[i][1]+' ' +liste[i][0]+' ' + str(conv.convert_utc_mjd(liste[i][2])))
                if liste[k][0]=='AEXP_E':
#                    mat_station[0][0] = liste[i][3]
#                    mat_station[0][4] = conv.convert_utc_mjd(liste[i][2])
                    a_exp_e +=[liste[k][3]]
                    time_exp_e +=[conv.convert_utc_mjd(liste[k][2])]
                elif liste[k][0]=='ALOG_E':
#                    mat_station[0][2] = liste[i][3]
                    a_log_e +=[liste[k][3]]
                    time_log_e +=[conv.convert_utc_mjd(liste[k][2])]
                elif liste[k][0]=='TEXP_E':
#                    mat_station[0][1] = liste[i][3]
                    ti_exp_e += [liste[k][3]]
                elif liste[k][0]=='TLOG_E':
#                    mat_station[0][3] = liste[i][3]
                    ti_log_e += [liste[k][3]]
                elif liste[k][0]=='AEXP_N':
#                    mat_station[1,0] = liste[i][3]
#                    mat_station[1,4] = conv.convert_utc_mjd(liste[i][2])
                    a_exp_n +=[liste[k][3]]
                    time_exp_n +=[conv.convert_utc_mjd(liste[k][2])]
                elif liste[k][0]=='ALOG_N':
#                    mat_station[1,2] = liste[i][3]
                    a_log_n +=[liste[k][3]]
                    time_log_n +=[conv.convert_utc_mjd(liste[k][2])]
                elif liste[k][0]=='TEXP_N':
#                    mat_station[1,1] = liste[i][3]
                    ti_exp_n += [liste[k][3]]
                elif liste[k][0]=='TLOG_N':
#                    mat_station[1,3] = liste[i][3]
                    ti_log_n += [liste[k][3]]
                elif liste[k][0]=='AEXP_H':
#                    mat_station[2,0] = liste[i][3]
#                    mat_station[2,4] = conv.convert_utc_mjd(liste[i][2])
                    a_exp_h +=[liste[k][3]]
                    time_exp_h +=[conv.convert_utc_mjd(liste[k][2])]
                elif liste[k][0]=='ALOG_H':
#                    mat_station[2,2] = liste[i][3]
                    a_log_h +=[liste[k][3]]
                    time_log_h +=[conv.convert_utc_mjd(liste[k][2])]
                elif liste[k][0]=='TEXP_H':
#                    mat_station[2,1] = liste[i][3]
                    ti_exp_h += [liste[k][3]]
                elif liste[k][0]=='TLOG_H':
#                    mat_station[2,3] = liste[i][3]
                    ti_log_h += [liste[k][3]]
            else:
                liste_station_matrice +=[[liste[k-1][1], mat_station]]
#                mat_station = np.zeros((3,5))
                sum_exp,sum_log=0,0
                if len(a_exp_e) != 0:
                    for i in range(len(a_exp_e)):
                        sum_exp+=a_exp_e[i]*(1-np.exp(-((t-ti_exp_e[i])/365.25)/time_exp_e[i]))
                if len(a_log_e) != 0:                    
                    for j in range(len(a_log_e)):
                        sum_log+=a_log_e[j]*np.log(1+((t-ti_log_e[j])/365.25)/time_log_e[j])
                l_e=sum_exp+sum_log
                
                sum_exp,sum_log=0,0
                if len(a_exp_n) != 0:  
                    for i in range(len(a_exp_n)):
                        sum_exp+=a_exp_n[i]*(1-np.exp(-((t-ti_exp_n[i])/365.25)/time_exp_n[i]))
                if len(a_log_n) != 0:  
                    print(len(a_log_n), len(ti_log_n), len(time_log_n))
                    for j in range(len(a_log_n)):
                        sum_log+=a_log_n[j]*np.log(1+((t-ti_log_n[j])/365.25)/time_log_n[j])
                l_n=sum_exp+sum_log
                
                sum_exp,sum_log=0,0
                if len(a_exp_h) != 0:
                    for i in range(len(a_exp_h)):
                        sum_exp+=a_exp_h[i]*(1-np.exp(-((t-ti_exp_h[i])/365.25)/time_exp_h[i]))
                if len(a_log_h) != 0:
                    for j in range(len(a_log_h)):
                        sum_log+=a_log_h[j]*np.log(1+((t-ti_log_h[j])/365.25)/time_log_h[j])
                l_h=sum_exp+sum_log
                resultat+= [[liste[k-1][1], l_e, l_n, l_h ]]
                a_exp_e, ti_exp_e, time_exp_e, a_log_e, ti_log_e, time_log_e = [], [], [], [], [], []
                a_exp_n, ti_exp_n, time_exp_n, a_log_n, ti_log_n, time_log_n = [], [], [], [], [], []
                a_exp_h, ti_exp_h, time_exp_h, a_log_h, ti_log_h, time_log_h = [], [], [], [], [], []
                station_temp = liste[k][1]
                k -= 1

            k+=1
        return resultat
        
    def tracer_deformation(self):
        nt  = Time.now()
        nt.format = 'mjd'
        t=np.arange(0, nt.value, 1)
        plt.plot(t, self.L(t))
        plt.show()
        
        
                


    
if __name__ == '__main__':
    s = seismic()
#    identification = s.lecture_ID()
#    solution = s.lecture_solution()
#    matrice = s.lecture_matrice_cov()
    l=s.L(55720)
#    s.tracer_deformation()
#    print (ID)
#    print(solution)
#    print(matrice)
#    print(l)
    