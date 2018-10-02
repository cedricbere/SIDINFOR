from django.contrib import admin
from DepotDoc.models import Formation, Pays, Postulant, Dossier

# Register your models here.

admin.site.register(Formation)
admin.site.register(Pays)
admin.site.register(Postulant)
admin.site.register(Dossier)