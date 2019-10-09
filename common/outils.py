#!/usr/bin/env python
# -*- coding: utf8 -*-


'''
Created on 9 oct. 2018

@author: parice02
'''
# Ce fichier contient toute fonction du project qui n'est pas une vue, un modèle ou autre module django.
# Ces fonctions permettent 

from secrets import choice
from string import ascii_letters, digits
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Proposition de django
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def envoyer_mail_admins(type_mail = '', inscrit = '', mail_envoye = ''):
    """
    """
    
    sujet = 'Nouvelle inscription'
    contenu_html = render_to_string(template_name = 'envoi_mail.html', context = {'type_mail': type_mail, 'regime': 'admin', 'identite': inscrit.prenom+' '+inscrit.nom,
            'email': inscrit.compte.email, 'date_inscription': inscrit.compte.date_joined.strftime('%A, %d %B %Y %H:%M:%S'),
            'type': inscrit.type_personne, 'statut': 'Envoyé' if mail_envoye else 'Non envoyé'})

    contenu_texte = strip_tags(contenu_html)
    
    mail_admins(subject = sujet, message = contenu_texte, html_message = contenu_html)


def envoyer_mail(type_mail = '', regime = '', inscrit = '', code = ''):
    """
    Permet l'envoi de mail à un utilisateur nouvellement inscrit.
    """
    if (regime == None or regime == '') and (inscrit == None or inscrit == ''):
        raise ValueError('Veuillez bien reseigner les valeurs des arguments')
    
    if regime == 'Postulant':
        if (type_mail == 'inscription') and (code == None or code == ''):
            raise ValueError("Impossible d'envoyer ce mail sans code d'activation")


    sujet, destinataire, envoyeur = 'Inscription sur SIDINFOR', inscrit.email, 'parice02@hotmail.com'
    contenu_texte, contenu_html = '', ''

    if regime == 'Etudiant':
        contenu_html = render_to_string(template_name = 'envoi_mail.html', context = {'type_mail': type_mail, 'regime': 'étudiant'})
        contenu_texte = strip_tags(contenu_html)
         
    elif (regime == 'Postulant') and (code != ''):
        contenu_html = render_to_string(template_name = 'envoi_mail.html', context = {'type_mail': type_mail, 'regime': 'postulant', 'user_name': inscrit.username, 'code': code})
        contenu_texte = contenu_html
    else:
        raise ValueError("Ce régime: '%s' n'est pas pris en compte." % (regime,))
        
    mail_envoye = send_mail(subject = sujet, message = contenu_texte, from_email = envoyeur, recipient_list = [destinataire], html_message = contenu_html)
    if mail_envoye != 0: return True
    else: return False



def sauver_fichier(file_path, file):
    with open(file_path, 'wb+') as destionaion:
        for chunck in file.chunks():
            destionaion.write(chunck)
            
def chemin_sauvegarde_carousel(instance, filename):
    """
    """
    return "carousel/{0}".format(filename)



def chemin_sauvegarde_rapport(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un rapport/mémoire dans un dossier portant le nom de l'étudiant.
    """
    nom = instance.auteur.nom
    prenom = instance.auteur.prenom
    matricule = instance.auteur.matricule
    return 'uploads/rapport_stages/rapport_{0}/{1}'.format(matricule+'_'+prenom.lower()+'_'+nom.lower(), filename)



def chemin_sauvegarde_fichier(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un document relatif à un postulant dans un dossier portant son nom.
    """
    nom = instance.postulant.nom
    prenom = instance.postulant.prenom
    niveau = instance.postulant.formation.niveau
    num_dos = instance.postulant.dossier.numero_dossier
    return 'uploads/recrutement/{0}/dossier_{1}/{2}'.format(niveau, num_dos+'_'+prenom+'_'+nom, filename)



def chemin_sauvegarde_attestation_stage(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un document relatif à un postulant dans un dossier portant son nom.
    """
    nom = instance.stage.stagiaire.nom
    prenom = instance.stage.stagiaire.prenom
    niveau = instance.stage.stagiaire.formation.niveau
    num_dos = instance.stage.stagiaire.dossier.numero_dossier
    return 'uploads/recrutement/{0}/dossier_{1}/{2}'.format(niveau, num_dos+'_'+prenom+'_'+nom, filename)

def chemin_sauvegarde_attestation_travail(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un document relatif à un postulant dans un dossier portant son nom.
    """
    nom = instance.emploi.employe.nom
    prenom = instance.emploi.employe.prenom
    niveau = instance.emploi.employe.formation.niveau
    num_dos = instance.emploi.employe.dossier.numero_dossier
    return 'uploads/recrutement/{0}/dossier_{1}/{2}'.format(niveau, num_dos+'_'+prenom+'_'+nom, filename)

def chemin_sauvegarde_attestation_autre(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un document relatif à un postulant dans un dossier portant son nom.
    """
    nom = instance.emploi_autre.employe.nom
    prenom = instance.emploi_autre.employe.prenom
    niveau = instance.emploi_autre.employe.formation.niveau
    num_dos = instance.emploi_autre.employe.dossier.numero_dossier
    return 'uploads/recrutement/{0}/dossier_{1}/{2}'.format(niveau, num_dos+'_'+prenom+'_'+nom, filename)



def formater(entier, val_max = 1):
    """
    Fonction permettant le formatage de chiffre. Ex.00004 au de 4.
    Elle prend en paramètre l'entier à paramétrer en premier, puis le nombre de chiffre désiré pour le formatage.
    Elle retourne un entier après le formatage.
    """
    try:
        entier, val_max = int(entier), int(val_max)
        if val_max > len(str(entier)):
            return '0'*(val_max - len(str(entier))) + str(entier)
        elif val_max == len(str(entier)):
            return entier
        else:
            raise ValueError
    except ValueError:
        raise ValueError
    except NameError:
        raise NameError


      
# Le code généré est envoiyé à l'utilisateur (Postulant) pour lui permettre d'activer son compte de façon automatique.
def generateur_code():
    """
    Retourne 8 caractères tirés au hasard parmi les lettres ASCII et les 10 chiffres.
    """
    alphabet = ascii_letters + digits
    return ''.join(choice(alphabet) for i in range(8))
   


def nettoyage(chaine = ''):
    """
    Fonction permettant de nettoyer la saisie de l'utilisateur des caractères non désirés pour les recherches.
    Nettoie tout caractère qui n'est pas une lettre.
    Elle prends en paramètre la valeur champ de recherche et retourne une liste des mots utiles c-à-d sans sysmboles
    """
    try:
        str(chaine)
        ponctuation = (',', '.', ';', '!', '?', '&', '-', '_', '(', ')', '=', '"', '*', '#', '<', '>', '/', ':', '\\', '|', '[', ']', '{', '}')
        newChaine = ''
        for car in chaine :
            if car in ponctuation:
                newChaine += ' '
            else:
                newChaine += car
        newChaine = newChaine.split(' ')
        for mot in newChaine:
            if mot == '':
                newChaine.remove(mot)
        return newChaine
    except:
        return None