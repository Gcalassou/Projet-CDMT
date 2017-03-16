# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:21:16 2017

@author: Gabriel
"""
#test = Ftp('itrf.ign.fr',['incoming'])

#test.connexion_changeDir_download('codomes_gps.snx')
import FtpBis as ftp
import numpy as np
#from FtpBis import Ftp('itrf.ign.fr',['incoming']) as test
class DOMES:
    def __init__(self,type_data,number):
        self.type_data=type_data
        self.number=number
        self.path= 'codomes_gps.snx'
        
    def lecture_data(self):
        mon_ftp=ftp.Ftp('itrf.ign.fr',['incoming'])
        mon_ftp.connexion_changeDir_download(self.path)
#        mat = np.genfromtxt(self.path)
        fichier = open(self.path, 'r')
        lignes = fichier.readlines()
        code, domes=[],[]
        for ligne in lignes:
            ligne= ligne.split()
            code += [ligne[0]]
            domes+= [ligne[2]]
        return code, domes
        
    def conversion(self):
        mat=self.lecture_data()
        if self.type_data=="GPS":
            i=0
            for value in mat[0]:
                i+=1
                if value == self.number:
                    return mat[1][i]
                    break
        if self.type_data=="Laser":
            i=0
            for value in mat[1]:
                i+=1
                if value == self.number:
                    return mat[0][i]
                    break

if __name__ == '__main__':
    test = DOMES("GPS", "NDS1")
    test2= DOMES("Laser", "12373S001")
    mat_Domes= test.lecture_data()
#    print(mat_Domes[:,0])
#    print(test.conversion())
    print(test2.conversion())
                