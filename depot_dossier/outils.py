#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
Created on 12 nov. 2018

@author: parice02
'''
from xlsxwriter import Workbook

from django.conf import settings
from django.db.models import Q
from django.db import connection

from datetime import datetime


from depot_dossier.get_user import get_user

from django_countries.data import COUNTRIES
from django_countries.fields import Country

from common.outils import dictfetchall

#import re

def limiter_choix_stagiaire():
    
    user = get_user()
    return Q(stagiaire__compte = user)

def limiter_choix():
   
    return Q(employe__compte = get_user())

#def controleur_annee(periode_annee):
#    comp = re.compile("\d{4} - \d{4}", re.I)
#    if comp.match(periode_annee):
#        return True
#    else:
#        return False


def feuille_liste_totale(excel = None, nom_feuille:str = "", liste_postulant:list = []):
    """ Liste de les postulant
    Produit une feuille excel contenant la liste de tous les postulant.
    """
    if (not excel) or (not liste_postulant): raise ValueError('Les paramètres ne doivent pas être nuls')
    
    try: labels = list(liste_postulant[0].keys())
    except: raise TypeError('liste_postulant doit être une liste de dict()!!')
    
    format_entetes = excel.add_format({'bold': True, 'align': 'center',
                'font_name': 'Times New Roman', 'font_size': 9, 'text_wrap': True})
    format_donnees = excel.add_format({'align': 'center', 'text_wrap': True,
                'font_name': 'Times New Roman', 'shrink': False, 'font_size': 9, 'bold': True,})
    format_date = excel.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center', 'font_size': 9})
    
    nom = nom_feuille if len(nom_feuille) < 25 else nom_feuille[:25] # maximum 25 caractères
    nom = convertir(nom)
    feuille = excel.add_worksheet(nom)
    feuille.write_row('A1', labels, format_entetes)
    feuille.set_column(0, len(labels), 20)
    feuille.hide_gridlines(2)

    row  = 3
    for info in liste_postulant:
        col = 0
        for val in info.values():
            try: val.strftime('%Y-%m-%d')
            except :
                try: int(val)
                except:
                    try : COUNTRIES[val] 
                    except :
                        feuille.write(row, col, val, format_donnees)
                    else: 
                        nom_pays = Country(val)
                        feuille.write(row, col, nom_pays.name, format_donnees)
                else:
                    feuille.write_number(row, col, val, format_donnees)
            else: feuille.write_datetime(row, col, val, format_date)
            col += 1
        row += 1

def production_excel(request, niveau:str = ''):
    
    with Workbook('%s/depot_dossier_%s_.xlsx'%(settings.BASE_DIR, niveau,)) as excel_doc:
        excel_doc.set_properties({
            'title': "Fiche d'état postulant %s"%(niveau.lower()),
            'subject': "Fiche d'état",
            'author': request.user,
            'manager': 'sidinfor',
            'company': 'Département Informatique de Université Joseph Ki-Zerbo',
            'keywords': 'sidifor',
            'status': 'En developpement',
            'create': datetime.today(),
            'comments': ''
        })
        liste_postulant = []
        with connection.cursor() as curseur:
            query = """
            SELECT dossier_id AS 'Numéro dossier', nom_etablissement AS 'Origine',
                prenom AS 'Prénoms', nom AS Nom, sexe AS Sexe, date_naissance AS 'Date de Naissance',
                num_tel AS Contact, etat_traitement AS Dossier, pays AS Nationalité,
                intitule_diplome AS 'Intitulé du diplôme', etat_diplome AS 'Diplôme obtenu ou encours',
                annee_obtention AS 'Année d obtention', moyenne_semestre1 AS S1,
                moyenne_semestre2 AS S2, statut_post AS Statut,
                commentaire_dos AS Commentaires, validation AS Retenu, observation_dos AS Observations
            FROM common_personne
            INNER JOIN  depot_dossier_postulant ON common_personne.id = depot_dossier_postulant.personne_ptr_id
            INNER JOIN  depot_dossier_formation ON depot_dossier_postulant.formation_id = depot_dossier_formation.id
            LEFT JOIN depot_dossier_dossier ON depot_dossier_postulant.dossier_id = depot_dossier_dossier.numero_dossier
            LEFT JOIN depot_dossier_etablissement ON depot_dossier_postulant.etablissement_origine_id = depot_dossier_etablissement.id
            LEFT JOIN depot_dossier_universitaire ON depot_dossier_postulant.personne_ptr_id = depot_dossier_universitaire.etudiant_id AND niveau_etude = %s
            WHERE depot_dossier_formation.niveau = %s
            ORDER BY nom ASC
            """
            var = [
                #'L3S5' if niveau == 'master' else 'M2S3',
                #'L3S6' if niveau == 'master' else 'M2S4',
                'Licence 3' if niveau == 'master' else 'Master 2',
                niveau,]
            curseur.execute(query, var)
            liste_postulant = dictfetchall(curseur)

        feuille_liste_totale(excel = excel_doc, nom_feuille = "liste totale", liste_postulant = liste_postulant)

        dictsort = triage_par_item(liste_postulant, 'Origine')
        
        for key, value in dictsort.items():
            feuille_liste_totale(excel = excel_doc, nom_feuille = key, liste_postulant = value)

        dictsort = triage_par_item(liste_postulant, 'Retenu')
        
        for key, value in dictsort.items():
            feuille_liste_totale(excel = excel_doc, nom_feuille = key, liste_postulant = value)

def triage_par_item(liste_postulant:list = [], item:str = '')->dict:
    """
    """
    dict_sort = {}
    for d in liste_postulant:
        origine = d[item] or 'None'
        if origine in dict_sort.keys():
            dict_sort[origine].append(d)
        else:
            dict_sort[origine] = [d,]
    return dict_sort

def convertir(chaine:str = "")->str:
    """
    """
    lettre = {
        'é': 'e', 'è': 'e', 'ê': 'e' , 'à': 'a', 'ï': 'i',
        'î': 'i', 'ç': 'c', '/': '-', '\/': '-', '[': '-',
        ']': '-', '*': '-', '?': '-'}

    for car in chaine:
        if car in lettre.keys():
            indice = chaine.index(car)
            chaine = chaine[:indice] + lettre[car] + chaine[indice + 1:]
    return chaine

