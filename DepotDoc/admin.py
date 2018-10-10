from django.contrib import admin
from DepotDoc.models import Formation, Postulant, Dossier, DocumentId

# Register your models here.

admin.site.register(Formation)
admin.site.register(Postulant)
admin.site.register(Dossier)
admin.site.register(DocumentId)