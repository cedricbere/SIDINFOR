#!/usr/bin/env python
# -*- coding: utf8 -*-


from django.db import models
from django.contrib.auth.models import User

from common.models import Departement, UFR, Personne
from common.outils import chemin_sauvegarde_attestation_stage, chemin_sauvegarde_attestation_autre,\
    chemin_sauvegarde_attestation_travail, chemin_sauvegarde_fichier

from depot_dossier.outils import limiter_choix, limiter_choix_stagiaire

from django_countries.fields import CountryField #  Application django permettant l'affichage d'une liste de pays

#from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


####### Modèle pour le code d'activation ######

class UserCode(models.Model):
    """
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=8, unique=True, null=False)
    
    def __str__(self):
        return self.user.__str__() 

    class Meta:
        verbose_name = 'Code utilisateur'
        verbose_name_plural = 'Codes utilisateurs'
        
        

####### Information Personnelles #####

class Postulant (Personne):
    """
    Classe contenant les infomations personnelles sur un postulant
    """
    lieu_naissance = models.CharField('Lieu de naissance', max_length = 100, null=True, blank=True)
    #nationalite = models.CharField("Nationalité", max_length = 100, null = True, blank=True)
    statut_post = models.CharField('Statut', max_length = 100, null=True, blank=True)
    ville = models.CharField(verbose_name = 'Vile de résidence',max_length = 100, null = True, blank=True)
    etablissement_origine = models.ForeignKey('Etablissement', verbose_name = "Établissement d'origine",
                                              on_delete = models.DO_NOTHING, null = True, blank=True)
    region = models.CharField("Région / Etat", max_length = 100, null = True, blank=True)
    pays = CountryField(verbose_name = 'Nationalité', null=True, blank_label = 'Choisir votre pays')
    compte = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    formation = models.ForeignKey('Formation', on_delete=models.SET_NULL, null = True, blank=True)
    documentId = models.OneToOneField('DocumentId', on_delete=models.SET_NULL, null = True, blank=True)
    dossier = models.OneToOneField('Dossier', on_delete=models.SET_NULL, null = True, blank=True)
    type_personne = 'Postulant'
    
    def __str__(self):
        return self.prenom+' '+self.nom
    
class DocumentId(models.Model):
    """
    Classe contenant les information sur la pièce d'identié du postulant
    """
    carteId, passeport, carteRefuge, carteCons, autre = "CNI",  "Passport", 'CR', 'CC', 'Autre'
    TYPE = ((carteId, "Carte nationale d'identité"), (passeport, "Passeport"), (carteRefuge, "Carte de refugé"),
            (carteCons, 'Carte consulaire'), (autre, 'Autre'))
    type_doc = models.CharField(choices = TYPE, null = True, max_length = 100, verbose_name = "Type du document")
    numero_doc = models.CharField("Numéro du document", max_length = 20, null=True, blank=True, unique=True)
    lieu_etablissement = models.CharField("Lieu d'établissement", max_length = 100, null = True, blank=True)
    date_etablissement = models.DateField("Date d'établissement", null = True, blank=True)
    date_expiration = models.DateField("Date d'expiration", null = True, blank=True)
     
    def __str__(self):
        return self.type_doc+'\t'+self.numero_doc
    
    
    class Meta:
        verbose_name = 'Document ID'
        verbose_name_plural = 'Documents IDs'
        

########## Formations ######################
 
class Formation(models.Model):
    """
    Classe regroupant l'ensemble des formation des parcours et des formations proposées par l'université
    """
    ufr = models.ForeignKey(UFR, on_delete=models.SET_NULL, null=True, verbose_name = 'UFR')
    dpt = models.ForeignKey(Departement, verbose_name = 'Dépatement',on_delete=models.SET_NULL, null=True)
    niveau = models.CharField("Niveau d'étude", choices=(('master', 'Master'), ('doctorat', 'Doctorat')), max_length=10, null=True)
        
    def __str__(self):
        return self.dpt.nom_dpt+' '+self.niveau
  
   
     
class Master(Formation):
    """
    Classe dérivé de Formation, consacré au niveau Master
    """
    formation_master = models.CharField('Formation master', max_length = 200, null=True, unique = True)
    
    def __str__(self):
        return self.formation_master
 
     
        
class Doctorat(Formation):
    """
    Classe dérivé de Formation, consacré au niveau Doctorat
    """
    directeur_these = models.CharField('Directeur de thèse', max_length = 200, null=True, blank=True)
    these_doctorat = models.CharField('Thèse', max_length = 200, null=True, blank=True)
    
    def __str__(self):
        return self.these_doctorat
    
# Créer juste une nouvelle classe dérivée de Formation pour ajouter un nouveau niveau (ex. Licence(Formation))
    
    
##################  Parours ##################
  
'''    
class Scolaire (models.Model):
    """
    """
    etablissement_sco = models.CharField('Etablissement', max_length = 200)
    classe = models.CharField(max_length = 20)
    moyenne_ann = models.DecimalField('Moyenne annuelle', max_digits = 4, decimal_places=2)
    annee_sco = models.CharField('Années scolaire', null=True, max_length = 12)
    eleve = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.classe+' '+self.annee+' '+self.eleve
'''


class Professionnel(models.Model):
    """
    """
    employeur = models.CharField(verbose_name = 'Structure', max_length = 200, null=True)
    poste = models.CharField(max_length = 200, null=True)
    annee_travail = models.CharField('Période', max_length = 12, null=True)
    employe = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)

   
    def __str__(self):
        return self.employeur+' '+self.poste
 
  
class Universitaire(models.Model):
    """
    """
    etablissement_univ = models.CharField('Etablissement', null=True, max_length=200)
    formation = models.CharField(max_length = 200, null = True, blank = True)
    niveau_etude = models.CharField(max_length = 30) 
    moyenne_semestre1 = models.DecimalField('Moyenne semestre 1', max_digits = 4, decimal_places=2, null=True)
    moyenne_semestre2 = models.DecimalField('Moyenne semestre 2', max_digits = 4, decimal_places=2, null=True, blank = True)
    intitule_diplome = models.CharField('intitulé du diplôme', null = True, max_length = 200, blank = True)
    etat_diplome = models.CharField('Encours ou Obtenu', choices = (('obtenu', 'diplôme obtenu'), ('encours', 'obtention encours')),
                            null = True, max_length = 20, blank = True)
    annee_obtention = models.IntegerField("Année d'obtention", null = True, blank = True)
    annee_univ = models.CharField('Années académique', null = True, max_length = 12)
    etudiant = models.ForeignKey(Postulant, on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.formation+' '+self.etudiant.__str__()

       
class Stage(models.Model):
    """
    """
    structure = models.CharField(max_length = 200, null = False)
    ong, entreprise = 'ONG', 'Entreprise'
    TYPE = ((ong, 'ONG'), (entreprise, 'Entreprise'))
    type_structure = models.CharField('Type de la structure', choices = TYPE, null=True, max_length = 15)
    annee_stage = models.CharField('Période', null=True, max_length=12)
    theme = models.CharField('Thème', max_length = 200)
    stagiaire = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        return self.structure+' '+self.theme[:30]
    

class Autre(models.Model):
    """
    """
    type = models.CharField(max_length = 100, null=True)
    annee_autre = models.CharField('Période', null=True, max_length=12)
    structure = models.CharField(max_length = 100)
    poste = models.CharField('Occupation', null=True, max_length=200)
    employe = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        return self.structure+' '+self.duree+' '+self.employe
    
    
################ Autres ###################

class Dossier(models.Model):
    """
    """
    numero_dossier = models.CharField(max_length = 20, primary_key = True)
    date_inscription = models.DateTimeField(auto_now_add=True, null=False, blank = False)
    date_modif = models.DateTimeField(auto_now=True, null=False, blank = False)
    commentaire_dos = models.TextField("Commentaire", null = True, blank = True, max_length = 200)
    observation_dos = models.TextField("Observation", null = True, blank = True, max_length = 200)
    etat_traitement = models.CharField(choices = (('complet', 'Complet'), ('incomplet', 'Incomplet'),('annulé', 'Annulé')), max_length = 20, null = True, blank = True)
    validation = models.CharField(choices = (('validé', 'Validé'), ('attente', 'En attente'),('rejeté', 'Rejeté')), max_length = 20, null = True, blank = True)
    
    def __str__(self):
        return self.numero_dossier+' - '+ self.date_inscription.strftime('%A, %d %B %Y %H:%M:%S') +' - '+self.etat_traitement

    

#Paramètre upload_to = depot_dossier/uploads    
class Fichiers(models.Model):
    """
    """
    photo_id = models.ImageField("Photo d'identité", upload_to = chemin_sauvegarde_fichier, null=True, blank=True)
    carteid_recto = models.ImageField("Carte d'identité (recto)", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    carteid_verso = models.ImageField("Carte d'identité (verso)", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    passport= models.ImageField("Passeport", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    curriculum_file = models.FileField("Curriculum Vitae, (daté et signé en pdf)", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    diplome_bac = models.ImageField('Votre Baccalauréat', null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    attestation_licence = models.ImageField('Attestation de Licence', null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    attestation_master = models.ImageField('Attestation de Master', null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    postulant = models.OneToOneField(Postulant, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.postulant.__str__()
    
    class Meta:
        verbose_name = 'Pièce jointe'
        verbose_name_plural = 'Pièces jointes'
 
    
    
############## Attestations ########################   

class AttestationTravail(models.Model):
    """
    """
    nom_att_tra = models.CharField(max_length=200, null=True, blank=True)
    attestation_travail = models.ImageField("Attestation de travail", null=True,upload_to=chemin_sauvegarde_attestation_travail)
    emploi = models.OneToOneField(Professionnel, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.nom_att_tra

    
class AttestationStage(models.Model):
    """
    """
    nom_att_sta = models.CharField(max_length=200, null=True, blank=True)
    attestation_stage = models.ImageField("Attestation de stage", null=True, upload_to=chemin_sauvegarde_attestation_stage)
    stage = models.OneToOneField(Stage, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.nom_att_sta
    
    
class AttestationAutre(models.Model):
    """
    """
    nom_att_au = models.CharField(max_length=200, null=True, blank=True)
    attestation_autre = models.ImageField("Attestation pour autre activité", null=True, upload_to=chemin_sauvegarde_attestation_autre)
    emploi_autre = models.OneToOneField(Autre, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.nom_att_au

   
############ Autres ##############

class Etablissement(models.Model):
    """
    """
    nom_etablissement = models.CharField("Nom de l'établissement", max_length = 200, unique = True)
    adresse = models.CharField(max_length = 300, null = True, blank=True)
    tel_fixe = models.CharField("Téléphone fixe", max_length = 50, unique = True, null = True, blank=True)
    email_et = models.EmailField("Adresse courriel", null = True, blank=True, unique = True)
    site_web = models.URLField("Site Web", null = True, blank=True, unique = True)

    def __str__(self):
        return self.nom_etablissement
