# -*- conding:utf8 -*-
'''
Created on 9 oct. 2018

@author: parice02
'''
# Ce fichier contient toute fonction du project qui n'est pas une vue, un modèle ou autre module django.

from secrets import choice
from string import ascii_letters, digits
from django.core.mail import EmailMultiAlternatives, mail_admins


def envoyer_mail_admins(inscrit = '', mail_envoye = ''):
    if inscrit.type_personne == None:
        raise ValueError("%s n'est pas de type Personne")

    sujet = 'Nouvelle inscription'
    contenu_texte = str(
        "Une nouvelle inscription\n"+
        "Prénom et Nom: %s\n"+
        "email: %s\n"+
        "Date d'inscription: %s\n"+
        "Régime: %s\n"+
        "Statut du mail envoyé: %s") %(inscrit.prenom+' '+inscrit.nom, inscrit.compte.email,
                                       inscrit.compte.date_joined.strftime('%A, %d %B %Y %H:%M:%S'), inscrit.type_personne, str(mail_envoye))
    
    contenu_html = str('')
    
    mail_admins(subject = sujet, message = contenu_texte, html_message = contenu_html)


def envoyer_mail(regime = '', inscrit = '', code = ''):
    """
    Permet l'envoi de mail à un utilisateur nouvellement inscrit.
    """
    if (regime == None or regime == '') and (inscrit == None or inscrit == '') and (code == None):
        raise ValueError('Veuillez bien reseigner les valeurs des arguments')

    if inscrit.email == None:
        raise ValueError("%s n'est pas de type django.contrib.auth.models.User")

    sujet, destinataire, envoyeur = 'Inscription sur SIDINFOR', inscrit.email, 'parice02@hotmail.com'
    contenu_texte, contenu_html = '', ''

    if regime == 'Etudiant':
        contenu_texte = str(
        "Vous recevez ce mail suite à votre inscription sur la plateforme SIDINFOR en tant qu'étudiant.\n"+
        "Vontre identité sera vérifié avant l'activation de votre compte.\n"+
        "\t\tMerci de Patienter. Cordialement.")
        contenu_html = str('')
    elif (regime == 'Postulant') and (code != ''):
        contenu_texte = str(
        "Vous recevez ce mail suite à votre inscription sur la plateforme SIDINFOR en tant que postulant .\n"+
        "Veuillez suivre ce lien http://localhost:8000/depot_dossier/activation_compte/%s/%s pour activation automatique de votre compte."+
        "\t\tCordialement.") % (inscrit.username, code)
        contenu_html = str('')
    else:
        raise ValueError("Ce régime: '%s' n'est pas pris en compte." % (regime,))
        
    message_electronique = EmailMultiAlternatives(subject = sujet, body = contenu_texte, to = [destinataire], from_email = envoyeur)
    message_electronique.attach_alternative(contenu_html, 'text/html')
    mail_envoye = message_electronique.send()
    if mail_envoye != 0: return True
    else: return False



def sauver_fichier(file_path, file):
    with open(file_path, 'wb+') as destionaion:
        for chunck in file.chunks():
            destionaion.write(chunck)
            

def chemin_sauvegarde_rapport(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un rapport/mémoire dans un dossier portant le nom de l'étudiant.
    """
    nom = instance.auteur.nom
    prenom = instance.auteur.prenom
    matricule = instance.auteur.matricule
    return 'depot_rapport/static/uploads/rapport_{0}/{1}'.format(matricule+'_'+prenom.lower()+'_'+nom.lower(), filename)



def chemin_sauvegarde_fichier(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un document relatif à un postulant dans un dossier portant son nom.
    """
    nom = instance.postulant.nom
    prenom = instance.postulant.prenom
    num_dos = instance.postulant.dossier.numero_dossier
    return 'depot_rapport/static/uploads/dossier_{0}/{1}'.format(num_dos+'_'+prenom+'_'+nom, filename)



def chemin_sauvegarde_attestation(instance, filename):
    """
    Chemin racine pour la sauvegarde d'un document relatif à un postulant dans un dossier portant son nom.
    """
    nom = instance.emploi.employe.nom or instance.stage.stagiaire.nom
    prenom = instance.emploi.employe.prenom or instance.stage.stagiaire.prenom
    num_dos = instance.emploi.employe.dossier.numero_dossier or instance.stage.stagiaire.dossier.numero_dossier
    return 'depot_rapport/static/uploads/dossier_{0}/{1}'.format(num_dos+'_'+prenom+'_'+nom, filename)



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


      
# Le code généré doit être envoiyer à l'utilisateur pour lui permettre d'activer son compte de façon automatique.
# Fonction non utilisé
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