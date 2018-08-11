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
from django.contrib import admin
from Stage.views import login, inscription, accueil, profile, deconnexion, programmes, modifierProfile, ajax_email, ajax_pseudo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Rapport/', include('Rapport.urls')),
    path('', login),
    path('login/', login, name = 'login'),
    path('inscription/', inscription, name = 'inscription'),
    path('accueil/', accueil, name = 'accueil'),
    path('profile/', profile, name = 'profile'),
    path('deconnexion/', deconnexion, name = 'deconnexion'),
    path('programmes/', programmes, name = 'programmes'),
    path('modifierProfile/', modifierProfile, name = 'modifProfile'),
    path('verificationEmail', ajax_email, name = 'verificationEmail'),
    path('verificationPseudo', ajax_pseudo, name = 'verificationPseudo'),
]
