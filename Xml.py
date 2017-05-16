# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 11:30:33 2017

@author: dpts
"""

import File as file
from lxml import etree
import os

class Xml :
    
    """
    permet de créer un fichier xml pour 
    """
    
    def __init__(self,nameStation,file,path):
        self.nameStation = nameStation  #un fichier xml par station
        self.file = file
        self.path = path
        """
        nameStation : chaine de caractère, 4 lettres
        file : chaine de caractère, nom du fichier log
        path : chemin absolu du fichier log
        """
        
        
        
    def parcours(self,Liste):
        """
        Liste : liste
        cette fonction permet pour une liste de séparer les éléments 'titre' et les éléments
        'contenu'
        """
        titre = []
        contenu = []

        #on parcourt les listes de L0

        for i in range(len(Liste)):
            sT = ''
            sC = ''
            if ':' not in Liste[i]: #si il n'y a pas ':' dans la L[i], L[i] est considéré comme un titre
                for k in range(len(Liste[i])):
                    sT += Liste[i][k] 
                titre.append(sT)
                contenu.append('')
                sT=''
                sC=''
            else : #sinon on doit séparer ce qu'il y a avant ':' et après
                k = 0
                j = 0 
                while j < len(Liste[i]):
                    if Liste[i][j]!=':':
                        sT+=Liste[i][k]
                        j+=1
                        k+=1
                    else :
                        break
                titre.append(sT)
                sT=''
                
                for j in range(k+1,len(Liste[i])):
                    sC+= Liste[i][j] 
                contenu.append(sC)
                sC = ''
        
        #suppression des espaces et des parenthèses des titres (sinon en xml ça ne marche pas)
        for i in range(len(titre)):
            titre[i] = titre[i].replace(" ","")
            titre[i] = titre[i].replace("(","")
            titre[i] = titre[i].replace(")","")
            titre[i] = titre[i].replace("[","")
            titre[i] = titre[i].replace("]","")
            titre[i] = titre[i].replace(".","")
            titre[i] = titre[i].replace('"',"")
            titre[i] = titre[i].replace("%","")
            titre[i] = titre[i].replace("/","")
        
        #bug quand dans le .log il n'y a pas d'espace entre titre et ':'
            if ':' in titre[i] :
                ind = titre[i].index(':')
                copie = titre[i]
                contenu[i] = ''
                for k in range(ind+1,len(titre[i])):
                    contenu[i] += titre[i][k]
                titre[i] = ''
                for j in range(0,ind):
                    titre[i] += copie[j]    
                
                 
                  
        return(titre,contenu)
            
        
        
        
    def extraction(self):
        test = file.File(self.file,self.path)
        
        #pour chaque bloc :
        #on récupère les données
        #on sépare les données de type titre et de type contenu
        L0 = test.form()
        titre0,contenu0 = self.parcours(L0)
        
        L1 = test.srp()
        titre1,contenu1 = self.parcours(L1)
        
        L3 = test.gsi()
        titre3,contenu3 = self.parcours(L3)
        
        L4 = test.telescope_info()
        titre4,contenu4 = self.parcours(L4)
        
        L5 = test.lsi()
        titre5,contenu5 = self.parcours(L5)
        
        L6 = test.receiver_syst()
        titre6,contenu6 = self.parcours(L6)
        
        L8 = test.calibration()
        titre8,contenu8 = self.parcours(L8)
        
        L9 = test.tfs()
        titre9,contenu9 = self.parcours(L9)
        
        L10 = test.pi()
        titre10,contenu10 = self.parcours(L10)

        L12 = test.meteo_instru()
        titre12,contenu12 = self.parcours(L12)

        return(titre0,contenu0,titre1,contenu1,titre3,contenu3,titre4,contenu4,titre5,contenu5,titre6,contenu6,titre8,contenu8,titre9,contenu9,titre10,contenu10,titre12,contenu12)
        
        
    def create_tree(self,path):
        """
        cette fonction va récupérer les listes produites par extraction, et va créer la structure xml
        path : chaine de caractères, chemin absolu du répertoire où enregistrer output
        """
        titre0,contenu0,titre1,contenu1,titre3,contenu3,titre4,contenu4,titre5,contenu5,titre6,contenu6,titre8,contenu8,titre9,contenu9,titre10,contenu10,titre12,contenu12 = self.extraction()
        
        #listes qui servent pour la méthode générale
        titre = [titre0,titre1,titre3,titre4,titre5,titre6,titre8,titre9,titre10,titre12]
        contenu = [contenu0,contenu1,contenu3,contenu4,contenu5,contenu6,contenu9,contenu10,contenu12]
        
        
        #création de la racine de l'arbre
        station = etree.Element(self.nameStation)
        doc = etree.ElementTree(station)
        
        #liste des entiers de 0 à 9 pour tester si des balises commencent par un chiffre
        liste = ['0','1','2','3','4','5','6','7','8','9']
        #quand un titre commence par un chiffre, on ajoute un a devant
        #une boucle for par bloc, pas optimal mais ne fonctionne pas autrement        
        title = etree.SubElement(station,'a'+titre0[0])
        for i in range(1,len(titre0)):
            t = titre0[i]
            c = contenu0[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
            
        title = etree.SubElement(station,'a'+titre1[0])   
        for i in range(1,len(titre1)):
            t = titre1[i]
            c = contenu1[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
          
        title = etree.SubElement(station,'a'+titre3[0])
        for i in range(1,len(titre3)):
            t = titre3[i]
            c = contenu3[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
            
        title = etree.SubElement(station,'a'+titre4[0])
        for i in range(1,len(titre4)):
            t = titre4[i]
            c = contenu4[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
            
        title = etree.SubElement(station,'a'+titre5[0])
        for i in range(1,len(titre5)):
            t = titre5[i]
            c = contenu5[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
        
        title = etree.SubElement(station,'a'+titre6[0])
        for i in range(1,len(titre6)):
            t = titre6[i]
            c = contenu6[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
            
        title = etree.SubElement(station,'a'+titre8[0])
        for i in range(1,len(titre8)):
            t = titre8[i]
            c = contenu8[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
            
        title = etree.SubElement(station,'a'+titre9[0])
        for i in range(1,len(titre9)):
            t = titre9[i]
            c = contenu9[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
            
        title = etree.SubElement(station,'a'+titre10[0])
        for i in range(1,len(titre10)):
            t = titre10[i]
            c = contenu10[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
            
        title = etree.SubElement(station,'a'+titre12[0])
        for i in range(1,len(titre12)):
            t = titre12[i]
            c = contenu12[i]
            for k in range(len(liste)):
                if liste[k] in t :
                    t = 'a'+ t
            if t == '':
                t = 'empty'
                c = 'empty'
            t = etree.SubElement(title,t)
            t.text = c  
        
        #méthode générale, qui ne fonctionne pas
#        for i in range(len(titre)):
#            title = etree.SubElement(station,'a'+titre[i][0])
#            
#            for j in range(1,len(titre[0])):
#                
#                t = titre[i][j]
#                c = contenu[i][j]
#                print(c)
#                for k in range(len(liste)):
#                    if liste[k] in t :
#                        t = 'a'+ t
#                if t == '':
#                    t = 'empty'
#                    contenu = 'empty'
#                
#                t = etree.SubElement(title,t)
#                t.text = c
                    
                               
        #print(etree.tostring(station,pretty_print=True))
        
        #écriture du fichier en sortie
        output = path + self.nameStation + '.xml'
        
        doc.write(output, xml_declaration=True, encoding='utf-8')
        
        

"""
test de création d'un xml sur un fichier log
"""
test = Xml('apol','apol_20090629.log','/home/dpts/Bureau/ProjetDev/Logs/')
#test = Xml('grsf','grsf_20030418.log','/home/dpts/Bureau/ProjetDev/Logs/')
#test.create_tree('/home/dpts/Bureau/ProjetDev/xml/')
        
#titre0,contenu0,titre1,contenu1,titre3,contenu3,titre4,contenu4,titre5,contenu5,titre6,contenu6,titre8,contenu8,titre9,contenu9,titre10,contenu10,titre12,contenu12 = test.extraction()

        
"""
création des xml pour tous les logs
"""

#nom en 4 lettres des stations pour self.nameStation
nom_slr = ['glsl','lvil','maid','mail','koml','mdvl','siml','mdvs','altl','rigl','arkl','bail','svel','zell','badl','irkl','ktzl','octl','llcd','apol','mdol','yarl','godl','monl','ha4t','thtl','go1l','go4t','hall','wuhl','chal','beil','kogc','kogl','kasl','miul','tatl','beit','urul','lhal','beia','gmsl','daek','burf','sejl','arel','conl','sjul','bral','harl','cgll','wett','bref','metl','ziml','borl','kun2','kunl','sha2','thtf','sfef','sfel','stl3','strk','sosw','parf','graf','chaf','hlwl','riyl','grsl','potl','shal','sisl','grzl','herl','pot3','orrl','grsm','grsf','ajaf','strl','stal','matl','matm','wetl']


#obtention de la liste de tous les fichiers log contenus dans chemin      
chemin ='/home/dpts/Bureau/ProjetDev/Logs/'

fichier = open('log_names.txt','r')
liste = fichier.readlines()

fichier.close()

#formatage des données
for i in range(len(liste)) :
    liste[i] = liste[i].rstrip('\n')  #suppression des \n
    liste[i] = liste[i].rstrip('\t')  #suppression des \t

        
#création d'un objet Xml pour chaque fichier log

for i in range(len(liste)):
    f = liste[i]
    for k in range(len(nom_slr)):
        if nom_slr[k] in f :
            code = nom_slr[k]
   
    temp = Xml(code,f,chemin)
    temp.create_tree('/home/dpts/Bureau/ProjetDev/xml2/')
        
        
        
        
        
        
        
        