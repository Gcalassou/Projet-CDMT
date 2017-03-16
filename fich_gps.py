# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 11:28:01 2017

@author: Gabriel
"""

import numpy as np
import math
import matplotlib.pyplot as plt
#import astropy.time.Time

#lbd=0
#phi=0
#a = 6378137.0      # IAG GRS80 constants
#e2 = 0.006694380022

class calc(object):
    def __init__(self,l,p,h):
        self.l=l  #longitude
        self.p=p  #latitude
        self.h=h  #hauteur        
        self.mat=np.genfromtxt("tutu.txt") #matrice contenant les différentes info du fichier GPS
        self.a = 6378137.0      # IAG GRS80 constants
        self.e2 = 0.006694380022
#        self.t=0
    @property           
    def matc(self):
        """
        Extrait les données utiles des fichiers GPS.
        Sortie :
            coord : matrice des déplacements dx,dy,dz de la station GPS
            t : matrice des temps de mesure des points par la station
        
        """
        ma = self.mat
        coord=np.zeros((ma.shape[0],3))
        t=np.zeros((ma.shape[0]))
        for i in range(ma.shape[0]):
                t[i]=ma[i][0]
                coord[i]=[ma[i][5],ma[i][6],ma[i][7]]
        return coord, t
    
    def d_sigma_nez(self):
        """
        Extrait les d_sigma en E, N, et H
        Sortie :
            sigma : matrice contenant les d_sigma en E, N, et H en cm
            
        """
        ma=self.mat
        sigma= np.zeros((ma.shape[0],3))
        for i in range(ma.shape[0]):
            sigma[i]=[ma[i][8],ma[i][9],ma[i][10]]
        return sigma
        
    @property
    def dms_to_dd(self):
        """
        Converti des angles en format degres/ minutes/ secondes en degres décimaux
        """
        phi= self.p
        lbd= self.l
#        alt=self.h
        ld=float(lbd[0])+float(lbd[1])/60+float(lbd[2])/3600
        pd=float(phi[0])+float(phi[1])/60+float(phi[2])/3600
        return ld, pd
        
    def cart_to_geo(self,X,Y,Z):
        """
        Conversion de coordonées cartésiennes à géographiques
        
        Arguments : 
            - X, Y, Z : coordonnées cartésiennes
        """
        
        f = 1 - math.sqrt(1-self.e2)
        
        rxy = math.sqrt(X**2 + Y**2)
        r = math.sqrt(X**2 + Y**2 + Z**2)
        mu = math.atan((Z/rxy)*((1-f) + self.a*self.e2/r))
        
        num = Z*(1-f) + self.e2*self.a *(math.sin(mu))**3
        denum = (1-f) * (rxy-self.a * self.e2 * (math.cos(mu))**3)
        lat = math.atan(num/denum)
        
        lon = 2 * math.atan(Y/(X+rxy))
        
        w = math.sqrt(1 - self.e2*math.sin(lat)**2)
        h = rxy*math.cos(lat) + Z*math.sin(lat) - self.a*w
        
        return lon,lat,h
    
    def R(self):
        """
        Creer la matrice de rotation R
        Arguments:
            lbd : longitude du GPS étudié
            phi : latitude du GPS étudié
        """
        lbd= self.dms_to_dd[0]  #longitude en degres decimaux
        phi= self.dms_to_dd[1]  #latitude en degres decimaux
        
        r=np.array([[-np.sin(lbd), np.cos(lbd),0],
                 [np.sin(phi)*np.cos(lbd), -np.sin(lbd)*np.sin(phi),np.cos(phi)],
                  [np.cos(phi)*np.cos(lbd), np.cos(phi)*np.sin(lbd),np.sin(phi)]])
        return r
    
    @property
    def mat_xyz(self):
        """
        Creer la matrice la matrice des déplacements en coordonnées cartesiennes
        de la station GPS étudiées sous le format:
        [[dx_1,dy_1,dz_1]
         [dx_2,dy_2,dz_2]
         ...,
         [dx_n,dy_n,dz_n]]
        """
        mat1=self.matc[0]
        R=self.R()
#        print(mat1)
        ma=np.zeros((mat1.shape[0],mat1.shape[1]))
        for i in range(mat1.shape[0]):
            ma[i]=np.dot(R,mat1[i])
        return ma
        
    def covariance_xyz(self):
        ma = self.mat_xyz
        R= self.R()
        cov = [[],[],[],[],[]]
        dec_cov=[]
        for i in range(ma.shape[0]):
            sigma = np.diag(self.d_sigma_nez()[i])
#            print("sigma : "+str(sigma))
            cov1= np.dot(R, np.dot(sigma.T, R.T))
#            print("cov "+str(cov1))
            for k in range(-2,3):     
                dec_cov= np.diag(cov1,k)

#                print()
#                for i in range()
                for elt in dec_cov:
                        cov[2+k]+=[elt]
                if i < ma.shape[0]-1:
                    cov[2+k]+=abs(k)*[0]
#        print("decomposition : "+str(cov))
        return cov
    
    def mat_cov(self):
        cov= self.covariance_xyz()
#        print("cov : "+str(cov))
        result= np.zeros((len(cov[2])))
        for k in range(-2,3):
            test= np.diag(cov[k+2],k)
#            print(test.shape)
#            print(str(k+2)+" :" +str(test))
            result=result+test
#            temp=
        return result
        
    def moy_pond(self):
        sig=self.d_sigma_nez()
        mat=self.matc[0]
        n= len(mat[:,0])
        list_moy=[]
        sum_a=sum(sig[:,0])
        sum_b=0
        sum_c=0
        for i in range(n):
            sum_b+=mat[i][0]/sig[i][0]
        moy=(1/sum_a)*sum_b
        for j in range(n):
            sum_c += (mat[i][0]-moy)**2/sig[i][0]
        moy_pond= np.sqrt((1/sum_a)*(1/n)*sum_c)
        return moy_pond
        
#    def moy_pond_bis(self):
#        
    def modele_estimation(self):
        
    
    def affichage(self):
        """
        Permet l'affichage des déplacements d'une station GPS selon
        N, E, et Z
        """
        ma_n=(self.matc[0])[:,0]
        ma_e=(self.matc[0])[:,1]
        ma_z=(self.matc[0])[:,2]
        p_n = plt.plot(self.matc[1],ma_n)
        p_e = plt.plot(self.matc[1],ma_e)
        p_z = plt.plot(self.matc[1],ma_z)
        plt.title("Deplacement d'une station GPS au cours du temps")
#        plt.legend([p_n,p_e,p_z],[" N", " E", "Z"])
        plt.show()
#        plt.plot(self.matc[1],ma_y)
#        plt.show()
#        plt.plot(self.matc[1],ma_z)
#        plt.show()
#  
#
#    def sigma(self):
#        for i in range(3):
#            ma= self.mat_xyz[:,i]
#            moy=0
#            for j in range(ma.shape[1]):
#                moy+=


if __name__ == '__main__':
    lbd=[298, 28, 20.8]
    phi=[16,15, 44.2]
    alt=-25.6
#    lbd=[47, 13, 45.1]
#    phi=[-19, 1,05.9]
#    alt=1553.0
    a= calc(lbd,phi,alt)
    mat=a.mat
    temps=a.matc[1]
    colonne_interet=a.matc
    liste_cov=a.covariance_xyz()
    mat_covariance= a.mat_cov()
    mp=a.moy_pond()
#    print(a.matc[0])
#    print(a.matc[1])
    print(a.d_sigma_nez())
#    print(a.dms_to_dd)
#    print(a.mat_xyz)
#    print(mat_covariance)
#    print(a.affichage())
#    print(mat)