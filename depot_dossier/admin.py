#!/usr/bin/env python
# -*- coding: utf8 -*-

from common.admin import site_admin
from depot_dossier.models import Master, Etablissement#, Postulant, DocumentId, Dossier, Doctorat, Formation, Professionnel, Autre, Fichiers,\
    #Universitaire, Stage, UserCode, AttestationAutre, AttestationStage, AttestationTravail

# Register your models here.

site_admin.register(Master)
site_admin.register(Etablissement)
#site_admin.register(Formation)
#site_admin.register(Doctorat)
#site_admin.register(Postulant)
#site_admin.register(Dossier)
#site_admin.register(DocumentId)
#site_admin.register(Scolaire)
#site_admin.register(Universitaire)
#site_admin.register(Professionnel)
#site_admin.register(Autre)
#site_admin.register(Fichiers)
#site_admin.register(Stage)
#site_admin.register(UserCode)
#site_admin.register(AttestationAutre)
#site_admin.register(AttestationStage)
#site_admin.register(AttestationTravail)