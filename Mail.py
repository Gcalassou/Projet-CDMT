# -*- coding: utf-8 -*-
"""
Created on Wed May  3 09:30:27 2017

@author: dpts
"""

import Ftp as ftp
import Xml as xml
import re

"""
permet de récupérer les mails qui ont pour sujet un problème technique. 
Nous utilisons le fichier slrmail.index qui récapitule tous les mails échangés depuis 1995
"""


class Mail :
    
    def __init__(self, file,path,savename,savepath):
        
        """
        tous les paramètres sont des chaines de caractères
        file : nom du fichier en entrée (ici slrmail.index)
        path : chemin absolu de file
        savename : nom du fichier en sortie
        savepath : chemin absolu de savename
        """
        self.file = file
        self.path = path
        self.savename = savename
        self.savepath = savepath


    def recup(self):
        
        """
        cette fonction permet de récupérer les mails intéressants
        """

        #ouverture du fichier
        chemin = self.path+self.file
        fichier = open(chemin,'r')

        #stockage des données dans une liste
        liste = fichier.readlines()

        #nettoyage des données
        for i in range(len(liste)) :
            liste[i] = liste[i].rstrip('\n')  #suppression des \n
            liste[i] = liste[i].rstrip('\t')  #suppression des \t

        #Préparation des listes qui vont contenir les données

        #liste qui contient les numéros de toutes les slr
        code_slr = [1824,1831,1863,1864,1868,1870,1873,1874,1879,1884,1886,1887,1888,1889,1890,1891,1893,7040,7041,7045,7080,7090,7105,7110,7119,7124,7125,7130,7210,7231,7237,7249,7308,7328,7335,7337,7339,7343,7355,7356,7357,7358,7359,7370,7394,7403,7405,7406,7407,7501,7548,7594,7604,7806,7810,7811,7819,7820,7821,7822,7823,7824,7825,7826,7827,7828,7829,7830,7831,7832,7835,7836,7837,7838,7839,7840,7841,7843,7845,7846,7848,7849,7865,7939,7941,8834]
        #mise en correspondance des codes stations avec leur nom
        nom_slr = ['glsl','lvil','maid','mail','koml','mdvl','siml','mdvs','altl','rigl','arkl','bail','svel','zell','badl','irkl','ktzl','octl','llcd','apol','mdol','yarl','godl','monl','ha4t','thtl','go1l','go4t','hall','wuhl','chal','beil','kogc','kogl','kasl','miul','tatl','beit','urul','lhal','beia','gmsl','daek','burf','sejl','arel','conl','sjul','bral','harl','cgll','wett','bref','metl','ziml','borl','kun2','kunl','sha2','thtf','sfef','sfel','stl3','strk','sosw','parf','graf','chaf','hlwl','riyl','grsl','potl','shal','sisl','grzl','herl','pot3','orrl','grsm','grsf','ajaf','strl','stal','matl','matm','wetl']


        #initialisation des listes contenant les infos des mails intéressants
        #liste qui contient le numéro des mails
        mail_number = []
        #liste qui contient la date des mails
        date = []
        #liste pour stocker le code de la station
        code_station = []
        #liste pour stocker l'objet des mails
        subject = []


        #recherche des mots clé et remplissage des listes ci dessus


    
        #**********attention***************
        #les listes mail_number, date et subject se remplissent correctement
        #la liste code_station n'est pas correcte en sortie

        for i in range(len(liste)):
            #on cible les mots clé
            if 'down' in liste[i] or 'failure' in liste[i] or 'problem' in liste[i]:
                #on utilise le séparateur | pour récupérer les différentes infos
                temp = liste[i].split('|') 
                #on remplit nos listes 
                mail_number.append(temp[0])
                date.append(temp[1])
                subject.append(temp[3])
                #on ajoute une donnée supplémentaire : code de la station
                #on cherche dans temp[3] = sujet du mail une suite de 4 chiffres
                
                code = re.findall('([0-9]{4})',temp[3])
                #pour l'instant on ne traite que les cas où une seule suite est trouvée
                #on controle visuellement si on récupère bien les numéros de stations
                #dans notre cas, des mauvais numéros sont récupérés : on les repère et on fait en sorte de les enlever via le test if
                #c'est assez expérimental, à améliorer
                if len(code) == 1 and code[0] != '2008' and code[0] != '2396' and code[0] != '0414' :
                    code_station.append(code[0])
                else : code_station.append('****') #s'il n'y a pas de numéro reconnu, on met un caractère arbitraire : '*'
        
        
        return(mail_number,date,subject,code_station)

      
      
      
    def result_file(self):
        
        """
        écriture d'un fichier de résultats
        """

        mail_number,date,subject,code_station = self.recup()
        
        chemin = self.savepath + self.savename

        result = open(chemin,'w')
        result.close()

        result = open(chemin,'a')
        result.write('date#####mail_number#####code_station#####subject')


        for i in range(len(mail_number)):
            result.write('\n'+date[i]+'#####'+mail_number[i]+'##### '+code_station[i]+' #####'+subject[i])

        result.close()



"""
essais
"""

#téléchargement du slrmail.index sur le ftp
#ces lignes sont commentées, en effet on le télécharge une seule fois

#création de l'objet Ftp
#connec = ftp.Ftp('cddis.gsfc.nasa.gov',['reports','slrmail'],'','')
#connexion et téléchargement du fichier slrmail.index
#connec.connexion_changeDir_download('slrmail.index','/home/dpts/Bureau/ProjetDev/')

#création de l'objet Mail
#mail = Mail('slrmail.index','/home/dpts/Bureau/ProjetDev/','result_mail.txt','/home/dpts/Bureau/ProjetDev/')
#
#mail.result_file()










