# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:59:48 2022

@author: barthes
Exemple de lecture des fichiers json associés aux images de l'article 'Determining Chess Game State From an Image'
"""

import json

def loadjson(file):
    with open(file) as mon_fichier:
        data = json.load(mon_fichier)
        return data



if __name__ == "__main__":
    
    file = '0024.json'
    data = loadjson(file)
    print('Corners : ',data['corners'])
    print('\n')
    print('Pieces :',data['pieces'])
    
    

