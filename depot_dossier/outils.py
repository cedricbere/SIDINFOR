'''
Created on 12 nov. 2018

@author: parice02
'''
from xlsxwriter import Workbook
from datetime import datetime
#import re

def retourne_labels_liste(formulaire):
    """
    retourne un liste des labels du formulaire entré en paramète.
    """
    liste = list()
    for field in formulaire:
        liste.append(field.label)
    return liste 

'''
def controleur_annee(periode_annee):
    comp = re.compile('\d{4} - \d{4}', re.I)
    if comp.match(periode_annee):
        return True
    else:
        return False
'''
def production_excel(dict_donnees = dict(), niveau = ''):
    
    excel_doc = Workbook('dépôt_dossier_%s.xlsx'%niveau)
    feuille, i = [0,], 0
    for nom_feuille, block_donnees in dict_donnees.items():
        feuille[i] = excel_doc.add_worksheet(nom_feuille)
        format_entetes = excel_doc.add_format({'bold': True, 'italic': True, 'align': 'center'})
        format_donnees = excel_doc.add_format({'align': 'center'})
        format_date = excel_doc.add_format({'num_format': 'd mmmm yyyy', 'align': 'center'})
        feuille[i].set_column(0, len(block_donnees['labels']), 20)
        feuille[i].write_row('A1', block_donnees['labels'], format_entetes)
        row, col = 1, 0
        if block_donnees['donnees_postulants']:
            for info in block_donnees['donnees_postulants']:
                date_str = datetime.strptime(str(info.dateNaissance), '%Y-%m-%d') if info.dateNaissance  else None
                feuille[i].write(row, col, info.nom, format_donnees)
                feuille[i].write(row, col + 1, info.prenom, format_donnees)
                feuille[i].write(row, col + 2, info.sexe, format_donnees)
                feuille[i].write(row, col + 3, date_str, format_date)
                feuille[i].write(row, col + 4, info.numTel, format_donnees)
                feuille[i].write(row, col + 5, info.lieuNaissance, format_donnees)
                feuille[i].write(row, col + 6, info.nationalite, format_donnees)
                feuille[i].write(row, col + 7, info.ville, format_donnees)
                feuille[i].write(row, col + 8, info.region, format_donnees)
                feuille[i].write(row, col + 9, info.pays.name, format_donnees)
                row += 1
        i += 1    
    excel_doc.close()