from django.contrib import admin
from depot_rapport.models import Etudiant, Soutenance,  Rapport, Stage
from common.models import UFR, Departement, Filiere, Matiere, UniteEnseignement,  Semestre,  Classe

# Register your models here.

admin.site.register(Etudiant)
admin.site.register(Classe)
admin.site.register(Soutenance)
admin.site.register(UFR)
admin.site.register(Departement)
admin.site.register(Filiere)
admin.site.register(Rapport)
admin.site.register(Stage)
admin.site.register(Matiere)
admin.site.register(UniteEnseignement)
admin.site.register(Semestre)
