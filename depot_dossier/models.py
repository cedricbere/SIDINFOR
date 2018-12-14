from django.db import models
from django.contrib.auth.models import User
from depot_rapport.models import Personne
from common.models import Departement, UFR
from common.outils import chemin_sauvegarde_attestation, chemin_sauvegarde_fichier
from django_countries.fields import CountryField #  Application django permettant l'affichage d'une liste de pays


# Create your models here.


####### Modèle pour le code d'activation ######

class UserCode(models.Model):
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
    lieuNaissance = models.CharField('Lieu de naissance', max_length = 100, null=True, blank=True)
    nationalite = models.CharField("Nationalité", max_length = 100, null = True, blank=True)
    ville = models.CharField(max_length = 100, null = True, blank=True)
    region = models.CharField("Région / Etat", max_length = 100, null = True, blank=True)
    pays = CountryField(null=True, blank_label = 'Choisir votre pays')
    compte = models.OneToOneField(User, on_delete=models.SET_NULL, null = True, blank=True)
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
    carteId, passeport, carteRefuge, carteCons, autre = "Carte nationale d'identité",  "Passport", 'Carte de refugé', 'Carte consulaire', 'Autre'
    TYPE = ((carteId, "Carte nationale d'identité"), (passeport, "Passeport"), (carteRefuge, "Carte de refugé"),
            (carteCons, 'Carte consulaire'), (autre, 'Autre'))
    type_doc = models.CharField(choices = TYPE, null = True, max_length = 100, verbose_name = "Type du document")
    numero_doc = models.CharField("Numéro du document", max_length = 20, null=True, blank=True, unique=True)
    lieuEtablissement = models.CharField("Lieu d'établissement", max_length = 100, null = True, blank=True)
    dateEtablissement = models.DateField("Date d'établissement", null = True, blank=True)
    dateExpiration = models.DateField("Date d'expiration", null = True, blank=True)
    
    
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
    niveau = models.CharField("Niveau d'étude", choices=(('Master', 'Master'), ('Doctorat', 'Doctorat')), max_length=10, null=True)
        
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
    


class Professionnel(models.Model):
    """
    """
    employeur = models.CharField(max_length = 200, null=True)
    poste = models.CharField(max_length = 200, null=True)
    annee_travail = models.CharField('Année académique', max_length = 12, null=True)
    employe = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)

   
    def __str__(self):
        return self.entreprise+' '+self.employe+' '+self.periode
 
 
    
class Universitaire(models.Model):
    """
    """
    etablissement_univ = models.CharField('Etablissement', null=True, max_length=200)
    formation = models.CharField(max_length = 200)
    niveau_etude = models.CharField(max_length = 30) 
    moyenne_semestre = models.DecimalField('Moyenne semestre', max_digits = 4, decimal_places=2, null=True)
    annee_univ = models.CharField('Années universitaire', null=True, max_length = 12)
    etudiant = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.formation+' '+self.mention
    
    
class Stage(models.Model):
    """
    """
    structure = models.CharField(max_length = 200, null = False)
    ong, entreprise = 'ONG', 'Entreprise'
    TYPE = ((ong, 'ONG'), (entreprise, 'Entreprise'))
    type_structure = models.CharField('Type de la structure', choices = TYPE, null=True, max_length = 15)
    annee_stage = models.CharField('Année académique', null=True, max_length=12)
    theme = models.CharField('Thème', max_length = 200)
    stagiaire = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)

    
    def __str__(self):
        return self.structure+' '+self.theme[:30]
    

class Autre(models.Model):
    """
    """
    type = models.CharField(max_length = 100, null=True)
    annee_autre = models.CharField('Année académique', null=True, max_length=12)
    structure = models.CharField(max_length = 100)
    poste = models.CharField('Poste ocuppé', null=True, max_length=200)
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
    etat_traitement = models.CharField(choices = (('attente', 'En attente du remplissage'), ('encours', 'Encours'),
                                        ('rejeté', 'Rejeté'), ('validé', 'Validé'), ('annulé', 'Annulé')), max_length = 20)
    
    def __str__(self):
        return self.numero_dossier+' - '+ self.date_inscription.strftime('%A, %d %B %Y %H:%M:%S') +' - '+self.etat_traitement
    
    
#Paramètre upload_to = depot_dossier/uploads    
class Fichiers(models.Model):
    """
    """
    photoId = models.ImageField("Photo d'identité", upload_to = chemin_sauvegarde_fichier, null=True, blank=True)
    carteId_recto = models.ImageField("Carte d'identité (recto)", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    carteId_verso = models.ImageField("Carte d'identité (verso)", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    passport= models.ImageField("Passeport", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    curriculum = models.FileField("Curriculum Vitae, (daté et signé en pdf)", null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    diplome_bac = models.ImageField('Votre Baccalauréat', null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    attestation_licence = models.FileField('Attestation de Licence', null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    attestation_master = models.FileField('Attestation de Master', null=True, blank=True, upload_to = chemin_sauvegarde_fichier)
    postulant = models.OneToOneField(Postulant, on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.postulant.__str__()
    
    
    class Meta:
        verbose_name = 'Pièces jointes'
        verbose_name_plural = 'Pièces jointes'
 
    
    
############## Attestations ########################   
    
class AttestationTravail(models.Model):
    """
    """
    nom_AtTra = models.CharField(max_length=100, null=True, blank=True)
    attestation_travail = models.FileField("Attestation de travail", null=True,upload_to=chemin_sauvegarde_attestation)
    emploi = models.OneToOneField(Professionnel, on_delete=models.DO_NOTHING)
    
class AttestationStage(models.Model):
    """
    """
    nom_AtSta = models.CharField(max_length=100, null=True, blank=True)
    attestation_stage = models.FileField("Attestation de stage", null=True, upload_to=chemin_sauvegarde_attestation)
    stage = models.OneToOneField(Stage, on_delete=models.DO_NOTHING)
    
    
class AttestationAutre(models.Model):
    """
    """
    nom_AtAu = models.CharField(max_length=100, null=True, blank=True)
    attestation_autre = models.FileField("Attestation pour autre activité", null=True, upload_to=chemin_sauvegarde_attestation)
    emploi = models.OneToOneField(Autre, on_delete=models.DO_NOTHING)
    
    