#!/usr/bin/env python
# -*- coding: utf8 -*-

from common.admin import site_admin
from depot_rapport.models import Soutenance, Etudiant,Rapport, Stage

# Register your models here.

#site_admin.register(Etudiant)
site_admin.register(Soutenance)
site_admin.register(Rapport)
site_admin.register(Stage)

