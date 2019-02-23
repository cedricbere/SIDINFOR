from django.db import models
from django.contrib.auth.models import User
#from phonenumber_field.modelfields import PhoneNumberField
from common.models import Personne, Classe, Filiere
from common.outils import chemin_sauvegarde_rapport

# Create your models here.
     
    
class Etudiant(Personne):
    niveau = models.ForeignKey(Classe, null = True, on_delete = models.SET_NULL)
    filiere = models.ForeignKey(Filiere, verbose_name = "Filière", null = True, on_delete = models.SET_NULL)
    matricule = models.CharField(max_length = 10, unique = True)
    promotion = models.CharField('Promotion', max_length=12)
    compte = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    type_personne = 'Etudiant'
    
    def __str__(self):
        return self.nom+' '+self.prenom+' '+self.matricule


class Stage(models.Model):
    lieu = models.CharField(max_length = 100, verbose_name = "Structure d'accueil")
    dateDebut = models.DateField('Stage début le')
    debute, encours, non_trouve, fini = 'Débuté', 'Encours', 'Non trouvés', 'Fini'
    Etat = ((debute, 'Débuté'), (encours, 'Encours'), (non_trouve, 'Non trouvé'), (fini, 'Fini'))
    etat = models.CharField("État d'avancement", choices = Etat, max_length = 20)
    superviseur = models.CharField('Superviseur', max_length=200)
    maitreStage = models.CharField("Maître de Stage", max_length=200)
    stagiaire = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return 'Stage: '+self.stagiaire.niveau.nom_classe+' '+self.lieu


'''
class FichierRapport(models.Model):
    intitule = models.CharField(max_length=200)
    fichier_rapport = models.FileField(max_length = 100, upload_to=chemin_sauvegarde_rapport, verbose_name='Votre rapport de stage (pdf)')
    
    def __str__(self):
        return self.intitule
'''
   
    
#fichier_param : upload_to=chemin_sauvegarde_rapport
class Rapport(models.Model):
    theme = models.CharField("Thème", max_length = 200)
    domaine_metier = models.CharField('Domaine métier', max_length = 200)
    resume = models.TextField("Résumé")
    motsCle = models.CharField("Mots clés", max_length = 200, blank = True)
    fichier_rapport = models.FileField(max_length = 100, upload_to=chemin_sauvegarde_rapport, verbose_name='Votre rapport de stage (pdf)')
    date_premierChargement = models.DateTimeField(auto_now_add = True)
    date_modification = models.DateTimeField(auto_now = True)
    annee_academique = models.CharField("Année académique", max_length=12)
    auteur = models.ForeignKey(Etudiant, on_delete = models.DO_NOTHING)
    stage = models.OneToOneField(Stage, on_delete = models.DO_NOTHING)
    
    def __str__(self):
        return 'Rapport: '+self.theme[:30]




class Soutenance(models.Model):
    datePrevu = models.DateField("Date de Soutenance")
    dateEffective = models.DateField("Date effective", null = True, blank = True)
    heure = models.TimeField("Heure de soutenance", null = True)
    salle = models.CharField(max_length = 50)
    note = models.IntegerField(null = True)
    jury = models.CharField(max_length = 200, null = True)
    pv = models.CharField("Procès verbal", max_length = 200, null = True)
    rapport = models.OneToOneField(Rapport, on_delete = models.DO_NOTHING)
    stage = models.OneToOneField(Stage, on_delete=models.DO_NOTHING)
    etudiant = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return 'Soutenance: '+self.etudiant.__str__()+' '+str(self.datePrevu)+' '+self.salle
    
    

    
    