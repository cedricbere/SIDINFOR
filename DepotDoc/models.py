from django.db import models
from django.contrib.auth.models import User
from Rapport.models import Personne, Departement, UFR
from django_countries.fields import CountryField


# Create your models here.



####### Information Personnelles #####
class Postulant (Personne):
    dateNaissance = models.DateField('Date de naissance', null=True, blank=True)
    lieuNaissance = models.CharField('Lieu de naissance', max_length = 100, null=True, blank=True)
    nationalite = models.CharField("Nationalité", max_length = 100, null = True, blank=True)
    ville = models.CharField(max_length = 100, null = True, blank=True)
    region = models.CharField("Région / Etat", max_length = 100, null = True, blank=True)
    pays = CountryField(null=True, blank_label = 'Choisir votre pays')
    #codePostal = models.CharField('Code postal', max_length = 10, null = True)
    compte = models.OneToOneField(User, on_delete=models.SET_NULL, null = True, blank=True)
    formation = models.ForeignKey('Formation', on_delete=models.SET_NULL, null = True, blank=True)
    documentId = models.OneToOneField('DocumentId', on_delete=models.SET_NULL, null = True, blank=True)
    dossier = models.OneToOneField('Dossier', on_delete=models.SET_NULL, null = True, blank=True)
    type_personne = 'Postulant'
    
    def __str__(self):
        return self.nom+' '+self.prenom
    
    
class DocumentId(models.Model):
    carteId, passport, carteRefuge, carteCons = "Carte Nationale d'identité",  "Passport", 'Carte de refugé', 'Carte consulaire'
    TYPE = ((carteId, "Carte Nationale d'identité"), (passport, "Passport"), (carteRefuge, "Carte de refugé"), (carteCons, 'Carte consulaire'))
    type_doc = models.CharField(choices = TYPE, null = True, max_length = 100, default = passport, verbose_name = "Type du document")
    numero = models.CharField("Numéro", max_length = 20)
    dateEtablissement = models.DateField("Date d'établissement", null = True)
    dateExpiration = models.DateField("Date d'expiration", null = True)
    lieuEtablissement = models.CharField("Lieu d'établissement", max_length = 100, null = True)
    
    def __str__(self):
        return self.type_doc+'\t'+self.numero
    

########## Formation (seul l'admin y a accès) ######################
    
class Formation(models.Model):
        ufr = models.ForeignKey(UFR, on_delete=models.SET_NULL, null=True)
        dpt = models.ForeignKey(Departement, verbose_name = 'Dépatement',on_delete=models.SET_NULL, null=True)
        niveau = models.CharField(choices = (('master', 'Master'), ('doctorat', 'Doctorat')), max_length = 20, null=True)
        formation = models.CharField(max_length = 200, null=False, unique = True)
        
        def __str__(self):
            return self.formation
        
    
##################  Parours ##################
    
class Scolaire (models.Model):
    etablissement = models.CharField('Etablissement', max_length = 200)
    classe = models.CharField(max_length = 20)
    moyenne_ann = models.DecimalField(max_digits = 4, decimal_places=2)
    annee = models.CharField('Années scolaire', max_length = 12)
    eleve = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.classe+' '+self.annee+' '+self.eleve
    
class Professionel(models.Model):
    entreprise = models.CharField(max_length = 200)
    poste = models.CharField(max_length = 200)
    periode = models.CharField(max_length = 12)
    employe = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)
   
    def __str__(self):
        return self.entreprise+' '+self.employe+' '+self.periode
   
   
class Universitaire(models.Model):
    formation = models.CharField(max_length = 200)
    niveau_etude = models.CharField(max_length = 30)
    echec, passable, assezBien, bien, tresBien = 'Echec', 'Passable', 'Assez Bien', 'Bien','Trés Bien'
    MENTION = ((echec, 'Echec'), (passable, 'Passable'), (assezBien, 'Assez Bien'), (bien, 'Bien'), (tresBien, 'Trés Bien')) 
    mention = models.CharField(choices = MENTION, max_length = 20, default = passable)
    etudiant = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.formation+' '+self.mention+' '+self.etudiant
    
    
    
class Stage(models.Model):
    structure = models.CharField(max_length = 200, null = False)
    ong, entreprise = 'ONG', 'Entreprise'
    TYPE = ((ong, 'ONG'), (entreprise, 'Entreprise'))
    type_structure = models.CharField('Type de la structure', choices = TYPE, default = entreprise, max_length = 15)
    duree = models.IntegerField('Durée')
    theme = models.CharField('Thème', max_length = 200)
    stagiaire = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.structure+' '+self.duree+' '+self.stagiaire
    
class Autre(models.Model):
    type = models.CharField(max_length = 100)
    duree = models.IntegerField('Durée')
    structure = models.CharField(max_length = 100)
    employe = models.ForeignKey(Postulant, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.structure+' '+self.duree+' '+self.employe
    
    
################ Autres ###################

    
class Dossier(models.Model):
    numero = models.CharField(max_length = 20, primary_key = True)
    date_inscription = models.DateTimeField(auto_now_add=True, null=False, blank = False)
    date_modif = models.DateTimeField(auto_now=True, null=False, blank = False)
    etat_traitement = models.CharField(choices = (('attente', ('En attente du remplissage')), ('encours', 'Encours'), ('rejete', 'Rejeté'), ('valide', 'Validé')), max_length = 20)
    
    def __str__(self):
        return self.numero+' - '+self.etat_traitement