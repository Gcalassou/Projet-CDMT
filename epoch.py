# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 10:51:20 2017

@author: dpts
"""

from astropy.time import Time
import numpy as np 


def lecture_EPOCH(file):
    fichier=open(file,'r')
    lignes=fichier.readlines()
    c=0
    i=0
    liste=[]
    #T=np.zeros((nb_s,3))
    #print(T)
    for ligne in lignes:
        ligne=ligne.split()
        if ligne[0]=='+SOLUTION/EPOCHS':
            print(ligne[0])
            j=i+2
            
            while ((lignes[j]).split())[0]!='-SOLUTION/EPOCHS':
                ligne_test=lignes[j].split()  
                code=ligne_test[0]
                dat_deb=convert(ligne_test[4])
                date_debut=Time(dat_deb)
                date_debut.format='mjd'
                dat_fin=convert(ligne_test[5])
                date_fin=Time(dat_fin)
                date_fin.format='mjd'
                liste+=[[code,date_debut.value,date_fin.value]]
                j+=1
        i+=1
    return(liste)
                
    
    fichier.close()
    

def convert(date) :
    #format date ='YY:DD:SS'
    form=date.split(':')
    #year=form[0]
    #print(year)
    #print(type(year))
   
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
    
    
    
    

    


#print(convert('16:004:047371'))
    
print(lecture_EPOCH('ilrsa.pos+eop.160105.v135.snx'))


