# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:24:50 2017

@author: dpts
"""




"""
classe permettant de gérer les fichiers logs et les fichiers xml de la bdd
"""


class File :
    
    """
    permet d'extraire les données des fichiers log
    une fonction par bloc à extraire
    toutes les fonctions prennent : 
    en entrée : void (self)
    en sortie : une liste qui contient les infos du bloc correspondant
    """
    
    def __init__(self,name,path):
        
        """
        name : nom du fichier, chaine de caractères
        path : chemin absolu du fichier, chaine de caractères
        """
        
        self.name = name
        self.path = path
    
    """
    extraction des données qui nous intéressent du fichier log
    """
    
    #blocs qui ont la même longueur dans tous les log    
    
    #récupération du bloc 0
    def form(self):    
        Form = []  #0
        f = open(self.path + self.name)
        temp = f.readlines()
        for i in range(len(temp)) :
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t
            if '0.' in temp[i] and 'Form' in temp[i]:
            #if temp[i]=='0.   Form ':
            #if temp[i]==' 0.   Form' or temp[i]=='0.   Form' or temp[i]=='  0.   Form':
                l1 = [0,3,4,5]     #dans le cas où on ne veut que quelques lignes, on renseigne leur indice dans l1
                for j in range(7):
                    if j in l1 :   #si la ligne nous intéresse, on l'ajoute à Form
                        Form.append(temp[i+j].split())
              
        return Form
        
    #fonction pour extraire le bloc 1 : srp
    #marche bien
    def srp(self):
        SRP = []   #1  
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)): 
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t        
            if '1.' in temp[i] and 'Identification of the Ranging System Reference Point (SRP)' in temp[i]:
            #if temp[i]=='1.   Identification of the Ranging System Reference Point (SRP) ':            
            #if temp[i]==' 1.   Identification of the Ranging System Reference Point (SRP)' or temp[i]=='1.   Identification of the Ranging System Reference Point (SRP)' or temp[i]=='  1.   Identification of the Ranging System Reference Point (SRP)': 
                l2 = [0,3,4,10,11]        
                for j in range(14):
                    if j in l2 :
                        SRP.append(temp[i+j].split())
        f.close()
        return SRP
    
    
    
         
    #blocs qui n'ont pas la même longueur 
    #méthode : comme pour les blocs précédents, on repère le titre du bloc
    #on note la ligne du titre du bloc k
    #boucle while sur k, tant qu'on n'a pas trouvé le titre suivant : on stocke les lignes, k+=1
                
            
    #fonction pour extraire le bloc 3
    #ça fonctionne
    def gsi(self):
        GeneralSystemInfo = []  #3
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t 
            #recherche du début du bloc general system information
            if '3.' in temp[i] and 'General System Information' in temp[i]:
            #if 'General System Information' in temp[i]:
            #if temp[i]== ' 3.   General System Information' or temp[i]== '3.   General System Information' or temp[i] == '  3.   General System Information' :
                GeneralSystemInfo.append(temp[i].split())
                k = i+1 #indice du début du bloc
        
        #à partir du début du bloc, on en cherche la fin
        if k < len(temp):
            while '4.' not in temp[k] and 'Telescope Information' not in temp[k]: 
            #while temp[k] not in ('4.   Telescope Information'):            
            #while temp[k] not in (' 4.   Telescope Information','4.   Telescope Information','  4.   Telescope Information'):
                #récupération d'une ligne
                c = temp[k].split()
                #parcours des éléments d'une liste pour trouver les mots clé souhaités
                for i in range(len(c)):
                    #si un mot clé est trouvé, on ajoute toute la ligne à la liste de sortie
                    if c[i]=='CDP'and c[i+1]=='System':   
                        GeneralSystemInfo.append(c)
                    if c[i]=='CDP' and c[i+1]== 'Occupation':
                        GeneralSystemInfo.append(c)
                    if c[i]=='North':
                        GeneralSystemInfo.append(c)
                    if c[i]=='East':
                        GeneralSystemInfo.append(c)
                    if c[i]=='Up':
                        GeneralSystemInfo.append(c)
                    if c[i]=='Installed':
                        GeneralSystemInfo.append(c)
                    if c[i]=='Removed':
                        GeneralSystemInfo.append(c)    
                k+=1
    
        f.close()
        return GeneralSystemInfo
    
             
    #récupération du bloc 4
    #ça fonctionne            
    def telescope_info(self): 
        TelescopeInfo = []  #4
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t 
        for  i in range(len(temp)):
            #if temp[i]=='4.   Telescope Information ':
            if '4.' in temp[i] and 'Telescope Information' in temp[i]:            
            #if temp[i]== ' 4.   Telescope Information' or temp[i]== '4.   Telescope Information' or temp[i] == '  4.   Telescope Information':
                TelescopeInfo.append(temp[i].split())
                k = i+1
      
        if k < len(temp):
            while 'Laser System Information' not in temp[k]:
            #while temp[k] not in ('  5.   Laser System Information'):
            #while temp[k] not in (' 5.   Laser System Information','5.   Laser System Information','  5.   Laser System Information',' 5.    Laser System Information','5.    Laser System Information','  5.   Laser System Information'):
                c = temp[k].split()
                for i in range(len(c)):
                    if c[i]=='Receiving' :
                        TelescopeInfo.append(c)
                    if c[i]=='Installed':
                        TelescopeInfo.append(c)
                    if c[i]=='Removed':
                        TelescopeInfo.append(c)
                k+=1
        f.close()
        return TelescopeInfo 
    
                    
    #récupération du bloc 5 
    #ça fonctionne
    def lsi(self):
        LaserSystInfo = []  #5 
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t 
        for  i in range(len(temp)):             
            if '5.' in temp[i] and 'Laser System Information' in temp[i]:
                LaserSystInfo.append(temp[i].split())
                k = i+1
        if k < len(temp):
            while '6.' not in temp[k] and 'Receiver System' not in temp[k]:
            #while temp[k] not in ('  6.   Receiver System'):
            #while temp[k] not in (' 6.   Receiver System','6.   Receiver System',' 6. Receiver System','  6.   Receiver System','  6.   Receiver System'):
                LaserSystInfo.append(temp[k].split())
                k+=1
        f.close()
        return LaserSystInfo
    
                
    #récupération du bloc 6
    #ça fonctionne            
    def receiver_syst(self):
        ReceiverSyst = []   #6
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t
        
        for  i in range(len(temp)):  
            #if temp[i]=='  6.   Receiver System ':
            #if temp[i]=='6.   Receiver System ':            
            #if temp[i]== ' 6.   Receiver System' or temp[i]== '6.   Receiver System' or temp[i]==' 6. Receiver System' or temp[i]=='  6.   Receiver System':
            if '6.' in temp[i] and 'Receiver System' in temp[i]:
                ReceiverSyst.append(temp[i].split())
                k = i+1
        if k < len(temp):
            while '7.' not in temp[k] and 'Tracking Capabilities' not in temp[k]:
            #while temp[k] not in ('7.   Tracking Capabilities'):
            #while temp[k] not in (' 7.   Tracking Capabilities','7.   Tracking Capabilities',' 7. Tracking Capabilities','  7.   Tracking Capabilities'):
                ReceiverSyst.append(temp[k].split())
                k+=1 
        f.close()
        return ReceiverSyst
    
                
    
    #récupération du bloc 8 
    #ça fonctionne           
    def calibration(self):
        Calibration = []   #8
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t
        for  i in range(len(temp)):        
            if '8.' in temp[i] and 'Calibration' in temp[i]:
                Calibration.append(temp[i].split())
                k=i+1
       
        if k < len(temp):
            while '9.' not in temp[k] and 'Time and Frequency Standards' not in temp[k]:
            #while temp[k] not in (' 9.   Time and Frequency Standards'):            
                Calibration.append(temp[k].split())
                k+=1
        f.close()
        return Calibration     
        
        
        
    #récupération du bloc 9
    #ça fonctionne         
    def tfs(self):
        TimeandFrequencyStd = []    #9
        f = open(self.path + self.name)
        temp = f.readlines()
       
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t
        for  i in range(len(temp)):         
            if '9.' in temp[i] and 'Time and Frequency Standards' in temp[i]:
                TimeandFrequencyStd.append(temp[i].split())
                k=i+1
        if k < len(temp):
            while '10.' not in temp[k] and 'Preprocessing Information' not in temp[k]:
            #while temp[k] not in ('10.   Preprocessing Information'):
            #while temp[k] not in ('10.   Preprocessing Information',' 10.   Preprocessing Information','  10.    Preprocessing Information'):
                TimeandFrequencyStd.append(temp[k].split())
                k+=1
        f.close()
        return TimeandFrequencyStd
        
    
    #récupération du bloc 10 
    #ça fonctionne           
    def pi(self):
        PreprocessingInfo = []   #10     
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t
        for i in range(len(temp)):  
            if '10.' in temp[i] and 'Preprocessing Information' in temp[i] : 
                PreprocessingInfo.append(temp[i].split())
                k = i+1
        if k < len(temp):
            while '11.' not in temp[k] and 'Aircraft Detection' not in temp[k]:
            #while temp[k] not in ('11.   Aircraft Detection'):
            #while temp[k] not in ('11.   Aircraft Detection',' 11.   Aircraft Detection','  11.    Aircraft Detection'):
                PreprocessingInfo.append(temp[k].split())
                k+=1
        f.close()
        return PreprocessingInfo
      
    
                
    #récupération bloc 12
    #ça fonctionne
    def meteo_instru(self):
        MeteorologicalInstru = []   #12      
        f = open(self.path + self.name)
        temp = f.readlines()
        for  i in range(len(temp)):
            #formatage des données
            temp[i] = temp[i].rstrip('\n')  #suppression des \n
            temp[i] = temp[i].rstrip('\t')  #suppression des \t
        for  i in range(len(temp)):      
            if '12.' in temp[i] and 'Meteorological Instrumentation' in temp[i]:
                MeteorologicalInstru.append(temp[i].split())
                k=i+1
        if k<len(temp):
            while '13.' not in temp[k] and 'Local Ties, Eccentricities, and Collocation Information' not in temp[k]: 
            #while temp[k] not in ('13.   Local Ties, Eccentricities, and Collocation Information'):
            #while temp[k] not in ('13.   Local Ties, Eccentricities, and Collocation Information',' 13.   Local Ties, Eccentricities, and Collocation Information','  13.   Local Ties, Eccentricities, and Collocation Information'):
                MeteorologicalInstru.append(temp[k].split())
                k+=1
        f.close()
        return MeteorologicalInstru
            
        
"""
essais 
"""        
#test = File('arkl_20120215.log','/home/dpts/Bureau/ProjetDev/Logs/')
#test2 = File('strk_20040810.log','/home/dpts/Bureau/ProjetDev/Logs/')

#temp = test.telescope_info()
#print(temp)