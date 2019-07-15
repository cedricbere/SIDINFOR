#!/usr/bin/env python
# -*- coding: utf8 -*-


'''
Created on 9 oct. 2018

@author: parice02
'''
from django.db import models
#from django.contrib.auth.models import User 

#from phonenumber_field.modelfields import PhoneNumberField
from common.outils import chemin_sauvegarde_carousel


class Personne (models.Model):
    """
    Modèle Personne. Permet de stocker des info sur une personne 
    """
    nom = models.CharField("Nom(s)", max_length = 30)
    prenom = models.CharField("Prénom(s)", max_length = 30)
    Homme,Femme = 'Homme', 'Femme'
    SEXE = ((Homme, 'Homme'), (Femme, 'Femme'))
    sexe = models.CharField(choices = SEXE, max_length = 5, default = Homme, null = False)
    date_naissance = models.DateField("Date de Naissance", null = True, blank=True)
    num_tel = models.CharField("Téléphone", max_length = 50, unique = True, null = True, blank=True)
    type_personne = ''
    
    def __str__(self):
        return self.prenom+' '+self.nom




class UFR(models.Model):
    """
    """
    nom_ufr = models.CharField("UFR", max_length = 50, unique = True)
    
    def __str__(self):
        return self.nom_ufr
    
    class Meta:
        verbose_name = 'UFR'
        verbose_name_plural = 'UFRs'
 
    
    
class Departement(models.Model):
    """
    """
    nom_dpt = models.CharField("Département", max_length = 50)
    ufr = models.ForeignKey(UFR, null = True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return self.nom_dpt
    
    class Meta:
        verbose_name = 'Département'
    
class Filiere(models.Model):
    """
    """
    nom_filiere = models.CharField("Filière", max_length = 50)
    dpt = models.ForeignKey(Departement, null = True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return self.nom_filiere
    
    class Meta:
        verbose_name = 'Filière'
    
    

class Semestre(models.Model):
    """
    """
    nom_semestre = models.CharField("Semestre", max_length = 15, unique = True)
    niveau = models.ForeignKey('Classe', on_delete=models.SET_NULL, null = True)
        
    def __str__(self):
        return self.nom_semestre



class Classe(models.Model):
    """
    """
    nom_classe = models.CharField("Classe", max_length = 20, unique = True)
    
    def __str__(self):
        return self.nom_classe
        


class UniteEnseignement(models.Model):
    """
    """
    code = models.CharField(max_length = 11, unique = True, null = True)
    nom_unite = models.CharField("Unité d'enseignement", max_length = 100)
    semestre = models.ForeignKey(Semestre, on_delete=models.SET_NULL, null = True)
    
    
    def __str__(self):
        return self.nom_unite


    class Meta:
        verbose_name = "Unité d'enseignement"
        verbose_name_plural = "Unités d'enseignements"



    
class Matiere(models.Model):
    """
    """
    credits = models.IntegerField('Crédits')
    nom_matiere = models.CharField('Nom de la matière', max_length = 100)
    ue = models.ForeignKey(UniteEnseignement, verbose_name = "Unité d'enseignement", on_delete=models.SET_NULL, null = True)
    
    
    def __str__(self):
        return self.nom_matiere+'\t'+str(self.credits)
    
    class Meta:
        verbose_name = 'Matière'

class Carousel(models.Model):
    """
    """
    nom_carousel = models.CharField("Titre de l'image", max_length = 100, unique = True)
    image_path = models.ImageField(verbose_name = "Image", upload_to = chemin_sauvegarde_carousel, null = False, blank = False, unique = True)
    description_image = models.TextField("Description de l'image", null = True, blank = True)
    adresse_web = models.URLField(max_length = 300, null = True, blank = True)

    def __str__(self):
        return self.nom_carousel
