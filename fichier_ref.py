# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:50:18 2017

@author: dpts
"""
import math

def convert_lat(deg,minu,sec):
    DD= float(sec)/3600 + float(minu)/60 + float(deg)
    return DD 
    
def convert_lon(coord):
    form=coord.split()
    DD= float(form[2])/3600 + float(form[1])/60 + float(form[0])
    return DD
    
def geo_to_cart(lon,lat,h):
        """
        Conversion de coordonées géographiques à cartésiennes
        Arguments :
            - lon : longitude (rad)
            - lat : latitude (rad)
            - h : hauteur (m)
        """
        a = 6378137.0      
        e2 = 0.006694380022
        N = a / math.sqrt(1.0 - e2*(math.sin(lat))**2)        # angles in rad
        X = (N+h) * (math.cos(lon)) * (math.cos(lat))
        Y = (N+h) * (math.sin(lon)) * (math.cos(lat))
        Z = (N*(1-e2) + h) * (math.sin(lat))
	
        return X,Y,Z

def lecture_fichier_ref(file):
    fichier=open(file,'r')
    lignes=fichier.readlines()
    i=0
    liste=[]
    for ligne in lignes:
        ligne=ligne.split()
        if ligne[0] =='+SITE/ID':
            
            j=i+2
            while ((lignes[j]).split())[0]!='-SITE/ID':
                
                code=lignes[j][9:18]            #code de la station 
                lon=lignes[j][44:55]            #longitute en deg min sec
                lon_r=convert_lon(lon)          #conversion des longitudes en degres decimaux
                lat_deg=lignes[j][56:59]        
                lat_min=lignes[j][59:62]
                lat_sec=lignes[j][62:67]
                lat=convert_lat(lat_deg,lat_min,lat_sec)    #conversion des latitudes en degres decimaux
                alti=lignes[j][69:75] 
                X=geo_to_cart(float(lon_r),float(lat),float(alti))[0]
                Y=geo_to_cart(float(lon_r),float(lat),float(alti))[1]
                Z=geo_to_cart(float(lon_r),float(lat),float(alti))[2]
                liste+=[[code,X,Y,Z]]
                j+=1
            break
      
        i+=1
    return liste
    
var=lecture_fichier_ref('fichier_ref')




