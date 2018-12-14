from django.contrib import admin
from depot_dossier.models import Postulant, DocumentId, Master, Dossier, Doctorat, Formation, Scolaire, Professionnel, Autre, Fichiers,\
    Universitaire, Stage, UserCode

# Register your models here.

admin.site.register(Master)
admin.site.register(Formation)
admin.site.register(Doctorat)
admin.site.register(Postulant)
admin.site.register(Dossier)
admin.site.register(DocumentId)
admin.site.register(Scolaire)
admin.site.register(Universitaire)
admin.site.register(Professionnel)
admin.site.register(Autre)
admin.site.register(Fichiers)
admin.site.register(Stage)
admin.site.register(UserCode)