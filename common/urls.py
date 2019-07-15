#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Stage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf.urls.static import static

#from django.template.loader import get_template
from common import settings
from common.admin import site_admin
from common.views import login, inscription, accueil, profile, deconnexion, programmes, modifierProfile,\
     ajax_changer_departement, ajax_changer_formation, ajax_verification, index, programmes_pdf, login_2

from wkhtmltopdf.views import PDFTemplateView

app_name = 'common'

urlpatterns = [
    #path('', index, name = 'index'),
    path('', index, name = 'index'),
    path('admin/', site_admin.urls),
    path('depot_rapport/', include('depot_rapport.urls')),
    path('depot_dossier/', include('depot_dossier.urls')),
    path('login/', login, name = 'login'),
    path('login_page/', login_2, name = 'login_page'),
    path('inscription/', inscription, name = 'inscription'),
    path('accueil/', accueil, name = 'accueil'),
    path('profile/', profile, name = 'profile'),
    path('profile/modifier_profile/', modifierProfile, name = 'modifProfile'),
    path('deconnexion/', deconnexion, name = 'deconnexion'),
    path('programmes/', programmes, name = 'programmes'),
    path('programmes/programmes_pdf/<str:semestre>/', programmes_pdf, name = 'programmes_pdf'),
    path('ajax/verification/', ajax_verification, name = 'verification'),
    path('ajax/changer_departement/', ajax_changer_departement, name = 'changer_departement'),
    path('ajax/changer_formation/', ajax_changer_formation, name = 'changer_formation'),
    #path('pdf/', PDFTemplateView.as_view(template_name='programmes_pdf.html', filename = 'prog.pdf'), name='pdf'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)