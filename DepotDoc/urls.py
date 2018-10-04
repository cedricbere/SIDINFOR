'''
Created on 2 oct. 2018

@author: parice02
'''

from django.urls import path
from DepotDoc.views import depot_doss 


app_name = 'DepotDoc'
urlpatterns = [
    path('renseignement/', depot_doss, name = 'renseignement')
    ]