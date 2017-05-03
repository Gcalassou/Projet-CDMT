# -*- coding: utf-8 -*-
"""
Created on Wed May  3 13:48:04 2017

@author: dpts
"""

from astropy.time import Time
import numpy as np 

class Laser:
    
    def __init__(self):
        self.path='ilrsa.pos+eop.160105.v135.snx'
        
    
    def Epoch(self):
        """
        Fonction permettant de lire le bloc EPOCHS d'un fichier SLR
        parametre: fichier SLR
        sortie: matrice: code station,date de début d'acquisition, date de fin d'acquisition et mean epoch
        """
        fichier=open(self.path,'r')
        lignes=fichier.readlines()
        i=0
        mat_resultat = np.array([[]])
        #T=np.zeros((nb_s,3))
        #print(T)
        for ligne in lignes:
            ligne=ligne.split()
            if ligne[0]=='+SOLUTION/EPOCHS':
            #            print(ligne[0])
                j=i+2
                
                while ((lignes[j]).split())[0]!='-SOLUTION/EPOCHS':
                    ligne_test=lignes[j].split()  
                    code=ligne_test[0]
                    dat_deb=Laser.convert(ligne_test[4])
                    date_debut=Time(dat_deb)
                    date_debut.format='mjd'
                    dat_fin=Laser.convert(ligne_test[5])
                    date_fin=Time(dat_fin)
                    date_fin.format='mjd'
                    dat_mean = Laser.convert(ligne_test[6])
                    date_mean =Time(dat_mean)
                    date_mean.format = 'mjd'
                    liste_temp = np.array([[code,date_debut.value,date_fin.value, date_mean.value]])
                    if mat_resultat.shape == (1,0):
                        mat_resultat = liste_temp
                    else:
                        mat_resultat = np.concatenate((mat_resultat, liste_temp))
    #                liste+=[[code,date_debut.value,date_fin.value, date_mean.value]]
                    j += 1
            i+=1
        fichier.close()
        return(mat_resultat)
                
    
    def Domes(self):
        """
        Fonction pour lire le bloc ID d'un fichier SLR
        parametre: fichier SLR
        sortie: matrice : code station et DOMES correspondant
        """
        fichier=open(self.path,'r')
        lignes=fichier.readlines()
        i=0
        mat_resultat = np.array([[]])
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
                    liste_temp=np.array([[code,DOMES]])
                    if mat_resultat.shape == (1,0):
                        mat_resultat = liste_temp
                    else:
                        mat_resultat = np.concatenate((mat_resultat, liste_temp))
                    
                    j+=1
            i+=1
        fichier.close()
        return(mat_resultat)
        
    def Estimate_solution(self):
        """
        Fonction permettant de lire le bloc Solution Estimate
        parametre: fichier SLR
        sortie: matrice: code station, STAX,STAY,STAZ
        """
        fichier=open(self.path,'r')
        lignes=fichier.readlines()
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

    
        
    def Matrice_cov(self):
        """
        Fonction permettant de lire le bloc Matrix Estimate qui correspond a la matrice de covariance
        parametre: fichier SLR
        sortie: matrice de covariance
        """
        fichier=open(self.path,'r')
        lignes=fichier.readlines()
        dim=Laser.Estimate_solution(self)[1]
        mat=np.zeros((dim,dim))
        i=0
        for ligne in lignes :
            ligne=ligne.split()
            if ligne[0]=='+SOLUTION/MATRIX_ESTIMATE':
                j=i+2
                
                while ((lignes[j]).split())[0]!='-SOLUTION/MATRIX_ESTIMATE':
                    temp=[]
                    ligne_test=lignes[j].split()
                    PAR1=int(ligne_test[0])
                    #print(PAR1)
                    PAR2=int(ligne_test[1])
                    #print(PAR2)
                    temp=ligne_test[2:]
                    for i in range(len(temp)):
                        mat[PAR1-1][PAR2+i-1]=temp[i]
                    
                        
                    
                    j+=1
            i+=1
        return mat
    
        
    
    def convert(date) :
        """
        Fonction permettant de convertir une date au format  en 
        parametre: date format 'YY:DD:SS'
        sortie: date format 'YY:DD:HH:M' compatible avec le module astropy
                pour apres la convertir en jour julien modifie
        """
        
        form=date.split(':')
       
        if form[0]<='50' and form[0]>='0':
            year='20'+form[0]
        else:
            year='19'+form[0]
        day=form[1]
        h=int(float(form[2])/3600)
        m=int((float(form[2])/3600-h)*60)
        if m<10:
            m='0'+str(m)
        else:
            m=str(m)
        date_f=year+':'+day+':'+str(h)+':'+m
        return(date_f)
    
if __name__ == '__main__':
    l=Laser()
    result=l.Estimate_solution()
    print(result)
    