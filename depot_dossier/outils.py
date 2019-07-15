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


def feuille_liste_totale(excel = None, nom_feuille = "", liste_postulant:list = []):
    """ Liste de les postulant
    Produit une feuille excel contenant la liste de tous les postulant.
    """
    if (not excel) or (not liste_postulant): raise ValueError('Les paramètres ne doivent pas être nuls')
    
    try: labels = list(liste_postulant[0].keys())
    except: raise TypeError('liste_postulant doit être une liste de dict()!!')
    
    format_entetes = excel.add_format({'bold': True, 'align': 'center', 'underline': True, 'font_name': 'Times New Roman',
                    'font_size': 12})
    format_donnees = excel.add_format({'align': 'center', 'text_wrap': True, 'font_name': 'Times New Roman', 'shrink': True})
    format_date = excel.add_format({'num_format': 'd mmmm yyyy', 'align': 'center'})
    
    feuille = excel.add_worksheet(nom_feuille)
    feuille.write_row('A1', labels, format_entetes)
    feuille.set_column(0, len(labels), 20)
    feuille.hide_gridlines(2)

    row  = 3
    for info in liste_postulant:
        col = 0
        for val in info.values():
            try: val.strftime('%Y-%m-%d')
            except :
                try : COUNTRIES[val] 
                except :
                    feuille.write(row, col, val, format_donnees)
                else: 
                    nom_pays = Country(val)
                    feuille.write(row, col, nom_pays.name, format_donnees)
            else: feuille.write_datetime(row, col, val, format_date)
            col += 1
        row += 1

def production_excel(request, niveau:str = ''):
    
    with Workbook('%s/depot_dossier_%s.xlsx'%(settings.BASE_DIR, niveau)) as excel_doc:
        excel_doc.set_properties({
            'title': 'Fiche de renseignements pour postulant %s'%(niveau.lower()),
            'subject': 'Résumé sur les postulants',
            'author': request.user,
            'manager': 'sidinfor',
            'company': 'Département Informatique de Université Ouaga I Pr. Joseph Ki-Zerbo',
            'keywords': 'sidifor',
            'status': 'En developpement',
            'create': datetime.today(),
            'comments': ''
        })
        liste_postulant = []
        with connection.cursor() as curseur:
            query = """
            SELECT dossier_id, nom_etablissement, nom, prenom AS prénom, sexe, date_naissance,
                num_tel AS contact, lieu_naissance, pays AS nationalité, intitule_diplome AS intitulé_diplôme,
                etat_diplome AS état_diplôme, annee_obtention AS année_obtention, moyenne_semestre1 AS moyenne_semestre_1,
                moyenne_semestre2 AS moyenne_semestre_2
            FROM common_personne
            INNER JOIN  depot_dossier_postulant ON common_personne.id = depot_dossier_postulant.personne_ptr_id
            INNER JOIN  depot_dossier_formation ON depot_dossier_postulant.formation_id = depot_dossier_formation.id
            LEFT JOIN depot_dossier_etablissement ON depot_dossier_postulant.etablissement_origine_id = depot_dossier_etablissement.id
            LEFT JOIN depot_dossier_universitaire ON depot_dossier_postulant.personne_ptr_id = depot_dossier_universitaire.etudiant_id AND niveau_etude = %s
            WHERE depot_dossier_formation.niveau = %s
            ORDER BY nom ASC
            """
            curseur.execute(query, ['Licence 3' if niveau == 'master' else 'Master 2',niveau,])
            liste_postulant = dictfetchall(curseur)

        feuille_liste_totale(excel = excel_doc, nom_feuille = "liste totale", liste_postulant = sorted(liste_postulant, key = lambda k: k['nom_etablissement']))
        #print(liste_postulant)
        #print(sorted(liste_postulant, key = lambda k: k['nom_etablissement']))

