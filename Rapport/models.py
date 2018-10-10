from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Personne (models.Model):
    id = models.AutoField(primary_key = True)
    nom = models.CharField("Nom", max_length = 30)
    prenom = models.CharField("Prénom", max_length = 30)
    Homme,Femme = 'Homme', 'Femme'
    SEXE = ((Homme, 'Homme'), (Femme, 'Femme'))
    sexe = models.CharField(choices = SEXE, max_length = 5, default = Homme, null = False)
    numTel = models.CharField("Téléphone", max_length = 25, unique = True, null = True, blank=True)
    type_personne = ''
    
    def __str__(self):
        return self.prenom+' '+self.nom
    
    
    
class Classe(models.Model):
    nom_classe = models.CharField("Classe", max_length = 20, unique = True)
    
    def __str__(self):
        return self.nom_classe
    
class Semestre(models.Model):
    nom_semestre = models.CharField("Semestre", max_length = 15, unique = True)
    niveau = models.ForeignKey(Classe, on_delete=models.SET_NULL, null = True)
    
    
    def __str__(self):
        return self.nom_semestre
    
class Promotion(models.Model):
    promo = models.CharField('Promtion', max_length = 11)
    
    def __str__(self):
        return self.promo
    
    
class Etudiant(Personne):
    dateNaissance = models.DateField("Date de Naissance", null = False)
    niveau = models.ForeignKey(Classe, default = None, null = True, on_delete = models.SET_NULL)
    filiere = models.ForeignKey('Filiere', verbose_name = "Filière", default = None, null = True, on_delete = models.SET_NULL)
    matricule = models.CharField(max_length = 10, unique = True)
    promotion = models.ForeignKey('Promotion', verbose_name = 'Promotion', on_delete=models.SET_NULL, null = True)
    compte = models.OneToOneField(User, on_delete=models.SET_NULL, null = True)
    type_personne = 'Etudiant'
    
    def __str__(self):
        return self.nom+' '+self.prenom+' '+self.matricule
    
    
    
class UFR(models.Model):
    nom_ufr = models.CharField("UFR", max_length = 50, unique = True)
    
    def __str__(self):
        return self.nom_ufr
    
    
    
class Departement(models.Model):
    nom_dpt = models.CharField("Département", max_length = 50)
    ufr = models.ForeignKey(UFR, null = True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return self.nom_dpt
    
    
    
class Filiere(models.Model):
    nom_filiere = models.CharField("Filière", max_length = 50)
    dpt = models.ForeignKey(Departement, null = True, on_delete = models.SET_NULL)
    
    def __str__(self):
        return self.nom_filiere
    
    
    
    
    
class MaitreStage(Personne):
    profession = models.CharField(max_length = 50)
    employeur = models.CharField(max_length = 100)
    
class Supersiveur(Personne):
    titre = models.CharField(max_length = 20)
    


class Stage(models.Model):
    lieu = models.CharField(max_length = 100)
    dateDebut = models.DateField('Stage début le',null = True)
    debute, encours, non_trouve, fini = 'Débuté', 'Encours', 'Non trouvés', 'Fini'
    Etat = ((debute, 'Débuté'), (encours, 'Encours'), (non_trouve, 'Non trouvé'), (fini, 'Fini'))
    etat = models.CharField("État", choices = Etat, max_length = 20)
    superviseur = models.ForeignKey(Supersiveur, null = True, on_delete = models.SET_NULL)
    maitreStage = models.ForeignKey(MaitreStage, verbose_name = "Maître de Stage", null = True, on_delete = models.SET_NULL)
    stagiaire = models.ForeignKey(Etudiant, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return 'Stage: '+self.stagiaire.niveau.nom_classe+' '+self.lieu
    
    
    
class Rapport(models.Model):
    theme = models.CharField("Thème", max_length = 200)
    resume = models.TextField("Résumé")
    motsCle = models.CharField("Mots clés", max_length = 200, null = True, blank = True)
    fichier = models.FileField(max_length = 100, upload_to='uploads/')
    dateEnvoi = models.DateTimeField(auto_now_add = True)
    dateModif = models.DateTimeField(auto_now = True)
    anneeAcademique = models.ForeignKey(Promotion, verbose_name="Année académique", on_delete=models.SET_NULL, null=True)
    auteur = models.ForeignKey(Etudiant, null = True, on_delete = models.SET_NULL)
    stage = models.OneToOneField(Stage, on_delete = models.SET_NULL, null=True)
    
    def __str__(self):
        return 'Rapport: '+self.theme[:30]




class Soutenance(models.Model):
    datePrevu = models.DateField("Date de Soutenance", null = True)
    dateEffective = models.DateField("Date effective", null = True, blank = True)
    heure = models.TimeField("Heure de soutenance", null = True)
    salle = models.CharField(max_length = 50)
    note = models.IntegerField(null = True)
    jury = models.CharField(max_length = 200, null = True)
    pv = models.CharField("Procès verbal", max_length = 200, null = True)
    rapport = models.OneToOneField(Rapport, null=True, on_delete = models.SET_NULL)
    stage = models.OneToOneField(Stage, null=True, on_delete=models.SET_NULL)
    etudiant = models.ForeignKey(Etudiant, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return 'Soutenance: '+self.etudiant.__str__()+' '+str(self.datePrevu)+' '+self.salle
    
    

class UniteEnseignement(models.Model):
    code = models.CharField(max_length = 11, unique = True, null = True)
    nom_unite = models.CharField("Unité d'enseignement", max_length = 100)
    semestre = models.ForeignKey(Semestre, on_delete=models.SET_NULL, null = True)
    
    
    def __str__(self):
        return self.nom_unite



    
class Matiere(models.Model):
    credits = models.IntegerField('Crédits')
    nom_matiere = models.CharField('Nom de la matière', max_length = 100)
    ue = models.ForeignKey(UniteEnseignement, verbose_name = "Unité d'enseignement", on_delete=models.SET_NULL, null = True)
    
    
    def __str__(self):
        return self.nom_matiere+'\t'+str(self.credits)
    

    
    