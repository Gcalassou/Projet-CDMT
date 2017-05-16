# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 14:46:21 2017

@author: dpts
"""


"""
ce script fonctionne
"""

import ftplib as ftp
import os


class Ftp :
    
    def __init__(self,address,listDir,user,password):
        """
        address : adresse du ftp, chaine de carac, forme 'cddis.nasa.gov'
        listDir : liste contenant les répertoires successifs dans le bon ordre
        user : chaine de caractères, nom d'utilisateur du ftp, si ftp sans user alors user=''
        password : chaine de caractères, mot de passe du ftp, si ftp sans mdp password = ''
        """
        self.address = address
        self.listDir = listDir
        self.user = user
        self.password = password
        

    def connexion(self):
        """
        permet de se connecter au ftp 
        """        
        
        connex = ftp.FTP(self.address)
        if len(self.user)==0 and len(self.password)==0 :
            connex.login()
        else : 
            connex.login(self.user,self.password)
        connex.dir()
            
    
        
        
    def connexion_changeDir_download(self,ftpfile,destination):
        """
        ftpfile : chaine de caractère, nom du fichier à télécharger
        destination : chaine de caractère, chemin du répertoire où on va enregristrer le fichier
        connexion au ftp, changement de répertoire puis téléchargement du fichier ftpfile
        """
        #connexion au ftp
        connex = ftp.FTP(self.address)
        if len(self.user)==0 and len(self.password)==0 :
            connex.login()
        else :
            connex.login(self.user,self.password)
        #changement de répertoire
        n = len(self.listDir)
        
        for i in range(0,n):
            connex.cwd(self.listDir[i])
        
        #si l'utilisateur ne renseigne pas la destination,
        #on enregistre dans le répertoire courant
        if len(destination)==0 :  
            connex.retrbinary('RETR '+ftpfile, open(ftpfile,'wb').write)  #transfert de fichiers en binaire
            #connex.retrlines('RETR '+ftpfile, open(ftpfile,'wb').write) #transfert de fichiers en ascii mode
        else:
            
            connex.retrbinary('RETR '+ftpfile, open(os.path.join(destination,ftpfile),'wb').write)
            
     
     
    def connexion_changeDir_upload(self,diskfile,path):
        """
        connexion au ftp
        changement de répertoire
        poste le fichier diskfile sur le ftp
        diskfile (chaine de caractères) est le nom du fichier à uploader
        path (chaine de caractères) : répertoire du fichier
        """
        #connexion au ftp
        connex = ftp.FTP(self.address)
        if len(self.user)==0 and len(self.password)==0 :
            connex.login()
        else :
            connex.login(self.user,self.password)
        #changement de répertoire
        n = len(self.listDir)
        fichier = path+'/'+diskfile
        file = open(fichier,'rb')
        
        for i in range(0,n):
            connex.cwd(self.listDir[i])
        connex.storbinary('STOR ' + diskfile,file)
        
        file.close()
         
      
      
      
      
      
    
        
#essai pour récupérer un fichier -> cela fonctionne
#test = Ftp('itrf.ign.fr',['incoming'],'','')
#
#test.connexion_changeDir_download('codomes_gps.snx')



#essai pour poster un fichier -> cela fonctionne
#test1 = Ftp('ftp2.ign.fr',[],'ing2-geocentre','Eiguceuqu0Yiu8wa')
#test1.connexion_changeDir_upload('nomTresTresSerieux','/home/dpts/Bureau/ProjetDev')

connec = Ftp('cddis.gsfc.nasa.gov',['reports','slrlog'],'','')


fichier = open('log_names.txt','r')

#construction d'une liste de noms de fichiers pour en télécharger plusieurs à la fois
#liste = fichier.readlines()
#
#
#
##formatage des données
#for i in range(len(liste)) :
#    liste[i] = liste[i].rstrip('\n')  #suppression des \n
#    liste[i] = liste[i].rstrip('\t')  #suppression des \t

#connec.connexion_changeDir_download('godl_20161207.log','/home/dpts/Bureau/ProjetDev/Logs')
#
#for i in range(0,len(liste)):
#    print(i)
#    ftpfile = (liste[i])
#    connec.connexion_changeDir_download(ftpfile,'/home/dpts/Bureau/ProjetDev/Logs')
    
#ftpfile = liste[1]
#print(ftpfile)
#connec.connexion_changeDir_download(ftpfile)



#gestion de l'erreur 550
#
#except ftplib.error_perm, resp:
#    if str(resp) == "550 No files found":
#        print "No files in this directory"
#    else:
#        raise
