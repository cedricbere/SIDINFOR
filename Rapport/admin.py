from django.contrib import admin
from Rapport.models import Etudiant, MaitreStage, Supersiveur, Classe, Soutenance, UFR, Departement,\
    Filiere, Rapport, Promotion, Stage, Matiere, UniteEnseignement,  Semestre

# Register your models here.

admin.site.register(Etudiant)
admin.site.register(MaitreStage)
admin.site.register(Supersiveur)
admin.site.register(Classe)
#admin.site.register(Soutenance)
admin.site.register(UFR)
admin.site.register(Departement)
admin.site.register(Filiere)
#admin.site.register(Rapport)
#admin.site.register(Stage)
admin.site.register(Promotion)
admin.site.register(Matiere)
admin.site.register(UniteEnseignement)
admin.site.register(Semestre)
