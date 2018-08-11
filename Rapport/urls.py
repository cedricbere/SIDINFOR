'''
Created on 22 mai 2018

@author: parice02
'''

from django.urls import path
from Rapport.views import rapportStage, consulterMesRapports, consulterLesRapports, ajax_modifStage, ajax_modifRapport,\
    ajax_modifSoutenance, ajax_recherche, resultats

app_name = 'Rapport'
urlpatterns = [
    path('depotRapport/', rapportStage, name = 'depotRapport'),
    path('mesRapports/', consulterMesRapports, name = 'consulterMesRapports'),
    path('lesRapports/', consulterLesRapports, name = 'consulterLesRapports'),
    path('modificationStage/', ajax_modifStage, name = 'modificationStage'),
    path('modificationRapport/', ajax_modifRapport, name = 'modificationRapport'),
    path('modificationSoutenance/', ajax_modifSoutenance, name = 'modificationSoutenance'),
    path('recherche/', ajax_recherche, name = 'recherche'),
    path('resultats', resultats, name = 'resultats'),
]