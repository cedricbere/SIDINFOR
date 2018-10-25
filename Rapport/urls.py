'''
Created on 22 mai 2018

@author: parice02
'''

from django.urls import path
from Rapport.views import consulterMesRapports, consulterLesRapports, ajax_recherche, resultats, rens_rapport

app_name = 'Rapport'
urlpatterns = [
    path('depotRapport/', rens_rapport, name = 'depotRapport'),
    path('mesRapports/', consulterMesRapports, name = 'consulterMesRapports'),
    path('lesRapports/', consulterLesRapports, name = 'consulterLesRapports'),
    path('recherche/', ajax_recherche, name = 'recherche'),
    path('resultats', resultats, name = 'resultats'),
]