'''
Created on 2 oct. 2018

@author: parice02
'''

from django.urls import path
from depot_dossier.views import depot_doss, annuler_reprendre_dos, t_admin, fichier_excel, activation_compte


app_name = 'depot_dossier'
urlpatterns = [
    path('', depot_doss, name = 'renseignements'),
    path('renseignements/', depot_doss, name = 'renseignements'),
    path('changement_etat/', annuler_reprendre_dos, name = 'changement_etat'),
    path('t_admin/', t_admin, name = 't_admin'),
    path('t_admin/<str:niveau>', t_admin, name = 't_admin'),
    path('fichier_excel/<str:niveau>', fichier_excel, name = 'fichier_excel'),
    path('activation_compte/', activation_compte, name = 'activation_compte'),
    path('activation_compte/<str:user_name>', activation_compte, name = 'activation_compte'),
    path('activation_compte/<str:user_name>/<str:code_activation>', activation_compte, name = 'activation_compte'),
    ]