# -*- conding:utf8 -*-
'''
Created on 22 mai 2018

@author: parice02
'''

from django.urls import path
from depot_rapport.views import mes_rapports, tous_rapports, ajax_recherche, resultats, rens_rapport, upload_fihier
from common.views import accueil

app_name = 'depot_rapport'
urlpatterns = [
    path('', accueil, name='accueil'),
    path('depotrapport/', rens_rapport, name = 'depotrapport'),
    path('mes_rapports/', mes_rapports, name = 'mes_rapports'),
    path('tous_rapports/', tous_rapports, name = 'tous_rapports'),
    path('recherche/', ajax_recherche, name = 'recherche'),
    path('resultats_rech/', resultats, name = 'resultats_rech'),
    path('upload_fichier/', upload_fihier, name = 'upload_fichier'),
]