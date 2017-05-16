# -*- coding: utf-8 -*-
"""
Created on Tue May 16 17:07:35 2017

@author: dpts
"""

import Xml as xml
import File as file
import Mail as mail


#chemin = répertoire du fichier log 
chemin = ''

fichier = file.File('mdol_20160309.log',chemin)

fichier_xml = xml.Xml('mdol','mdol_20160309.log',chemin)
fichier_xml.create_tree('')


fichier_mails = mail.Mail('slrmail.index','','result_mail.txt','')

fichier_mails.result_file()
