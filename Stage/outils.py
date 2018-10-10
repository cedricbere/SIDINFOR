'''
Created on 9 oct. 2018

@author: parice02
'''

def formater(entier, val_max = 1):
    """
    """
    try:
        entier, val_max = int(entier), int(val_max)
        if val_max > len(str(entier)):
            return '0'*(val_max - len(str(entier))) + str(entier)
        elif val_max == len(str(entier)):
            return entier
        else:
            print("'val_max' doit être plus grand que le nombre de chiffre dans 'entier'")
    except ValueError:
        print('Veillez sais un entier positif')
    except NameError:
        print('Variable non défini')
        
        

def nettoyage(chaine = ''):
    """
    """
    try:
        str(chaine)
        ponctuation = (',', '.', ';', '!', '?', '&', '-', '_', '(', ')', '=', '"', '*', '#', '<', '>', '/', ':', '\\', '|', '[', ']', '{', '}',"'")
        newChaine = ''
        for car in chaine :
            if car in ponctuation:
                newChaine += ' '
            else:
                newChaine += car
        liste = []
        for mot in newChaine.split(' '):
            if mot != '':
                liste.append(mot)
        return liste
    except:
        return None