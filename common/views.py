#!/usr/bin/env python
# -*- coding: utf8 -*-


'''
Created on 10 mai 2018

@author: parice02
'''

from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as logi, logout
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.db import IntegrityError
from django.conf import settings
from django.template.loader import get_template


from depot_rapport.models import Etudiant

from depot_dossier.models import Postulant, Master, UserCode, Dossier
from depot_dossier.forms import FormRensPostulant, FormFormation, FormDoctorat

from common.outils import formater, envoyer_mail, generateur_code, envoyer_mail_admins
from common.forms import LoginForm, FormCompte, FormEtudiant, FormPostulant, FormInfoSup
from common.models import Matiere, Semestre, Departement, Carousel

from crispy_forms.helper import FormHelper
from crispy_forms.utils import render_crispy_form

from wkhtmltopdf.utils import wkhtmltopdf
from wkhtmltopdf.views import PDFTemplateResponse






def user_form(request):
    """
    """
    if request.user.is_authenticated:
        if len(Etudiant.objects.filter(compte=request.user)) == 1:
            return Etudiant.objects.get(compte=request.user)
        elif len(Postulant.objects.filter(compte=request.user)) ==1:
            return Postulant.objects.get(compte=request.user)
        return None
    return None


def login(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        return redirect('/accueil')
    form = LoginForm(data = request.POST or None)
    if form.is_valid():
        user_pseudo = form.cleaned_data['pseudo']
        user_password = form.cleaned_data['password']
        user = authenticate(request, username=user_pseudo, password=user_password)
        if user:
            if user.is_active:
                logi(request, user)
                #request.session.set_expiry(0)
                if user.is_superuser:
                    return redirect('/admin')
                url = request.META['HTTP_REFERER'].split('=')
                if len(url) == 2:
                    return redirect(url[1])
                return redirect('/accueil')
        return render(request, 'index.html', {'form': form, 'info': "Identifiant et/ou mot de passe incorrecte."})              
    return render(request, 'index.html', {'form': form})

def login_2(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        return redirect('/accueil')
    form = LoginForm(data = request.POST or None)
    if form.is_valid():
        user_pseudo = form.cleaned_data['pseudo']
        user_password = form.cleaned_data['password']
        user = authenticate(request, username=user_pseudo, password=user_password)
        if user:
            if user.is_active:
                logi(request, user)
                #request.session.set_expiry(0)
                url = request.META['HTTP_REFERER'].split('=')
                if len(url) == 2:
                    return redirect(url[1])
                return redirect('/accueil')
        return render(request, 'login.html', {'form': form, 'info': "Identifiant et/ou mot de passe incorrecte."})              
    return render(request, 'login.html', {'form': form})


def inscription(request):
    """
    """
    # récupération des données de formulaire
    etudiant = FormEtudiant(data= request.POST if request.POST and (request.POST['typeProfile'] == 'etudiant') else None, prefix='etud')
    postulant = FormPostulant(data= request.POST if request.POST and (request.POST['typeProfile'] == 'postulant') else None, prefix='post')
    formation = FormFormation(data= request.POST if request.POST and (request.POST['typeProfile'] == 'postulant') else None)
    compteEtudiant = FormCompte(data= request.POST if request.POST and (request.POST['typeProfile'] == 'etudiant') else None, prefix='etud')
    comptePostulant = FormCompte(data= request.POST if request.POST and (request.POST['typeProfile'] == 'postulant') else None, prefix='post')
    autre_info = FormInfoSup(data = request.POST if request.POST and (request.POST['typeProfile'] == 'etudiant') else None, prefix='etud')
    
    if request.POST:
        if (request.POST['typeProfile'] == 'etudiant') and etudiant.is_valid() and compteEtudiant.is_valid() and autre_info.is_valid():
            
            # création du compte de l'inscrit
            user = User.objects.create_user(username=compteEtudiant.cleaned_data['pseudo'], email=compteEtudiant.cleaned_data['email'],
                        password=compteEtudiant.cleaned_data['password'], is_staff=False, is_active=False,
                        first_name=etudiant.cleaned_data['prenom'], last_name=etudiant.cleaned_data['nom'])
            
            autre_info.save()
            etudiant.instance.infosup = autre_info.instance
            
            # création du profile de l'inscrit 
            etudiant.instance.compte = user
            etudiant.save()
            
            # envoi de mails au postulant et à (aux) admin(s)
            mail_envoye = envoyer_mail(type_mail = 'inscription', regime = 'Etudiant', inscrit = user)
            envoyer_mail_admins(type_mail = 'inscription', inscrit = etudiant.instance, mail_envoye = mail_envoye)
            
        elif (request.POST['typeProfile'] == 'postulant') and postulant.is_valid() and comptePostulant.is_valid() :
            
            # création du compte de l'inscrit
            user = User.objects.create_user(username=comptePostulant.cleaned_data['pseudo'], email=comptePostulant.cleaned_data['email'],
                        password=comptePostulant.cleaned_data['password'], is_staff=False, is_active=False,
                        first_name=postulant.cleaned_data['prenom'], last_name=postulant.cleaned_data['nom'])
            
            # sauvegarde des données sur la formation
            if request.POST['niveau'] == 'master':
                f = Master.objects.get(pk = request.POST['formation'])
                postulant.instance.formation = f
            elif request.POST['niveau'] == 'doctorat':
                dataDoct = {'ufr': request.POST['ufr'], 'dpt': request.POST['dpt'], 'these_doctorat': request.POST['formation'], 
                        'niveau': request.POST['niveau'], 'directeur_these': ''}
                doctorat = FormDoctorat(data=dataDoct)
                if doctorat.is_valid():
                    doctorat.save()
                    postulant.instance.formation = doctorat.instance
            
            # création du profile de l'inscrit
            postulant.instance.compte = user
            postulant.save()
            
            # création du dossier du postulant
            numero = postulant.instance.id
            numero = str(formater(numero, 5))+str(request.POST['niveau'][0]).upper()
            dossier = Dossier.objects.create(numero_dossier = numero, etat_traitement = 'incomplet')
            postulant.instance.dossier = dossier
            postulant.save()
            
            # création du code d'activation du compte du postualt
            while True:
                try:
                    code_user = generateur_code()
                    UserCode.objects.create(user = user, code = code_user)
                except IntegrityError: pass
                else: break
             
            # envoi de mails au postulant et à (aux) admin(s)        
            mail_envoye = envoyer_mail(type_mail = 'inscription', regime = 'Postulant', inscrit = user, code = code_user)
            envoyer_mail_admins(type_mail = 'inscription', inscrit = postulant.instance, mail_envoye = mail_envoye)
        else:
            return render(request, 'inscription.html', {'etudiant': etudiant, 'compteEtudiant': compteEtudiant,
                                                            'comptePostulant': comptePostulant, 'postulant': postulant, 'formation': formation,
                                                            'autre_info': autre_info})
        
        activation =  """Veuillez consulter vos mail, nous vous avons envoyé un mail."""
        return render(request, 'confirmation.html', {'activation': activation})    
    return render(request, 'inscription.html', {'etudiant': etudiant, 'compteEtudiant': compteEtudiant,
                                    'comptePostulant': comptePostulant, 'postulant': postulant, 'formation': formation,
                                    'autre_info': autre_info})
    

def accueil (request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        images_carousel = Carousel.objects.all()
        return render(request, 'accueil.html', {'user': logged_user, 'images_carousel': images_carousel})
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


def index (request):
    """
    """
    logged_user = user_form(request)
    images_carousel = Carousel.objects.all()
    if logged_user:
        return render(request, 'index.html', {'user': logged_user, 'images_carousel': images_carousel})
    else:
        form = LoginForm()
        return render(request, 'index.html', {'form': form, 'images_carousel': images_carousel})

def profile(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        return render(request, 'profile.html', {'user': logged_user,})
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 
   
def deconnexion(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        logout(request)
    return redirect('/')



def programmes(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        semestres = Semestre.objects.exclude(uniteenseignement__code = None)
        matieres = Matiere.objects.all()
        return render(request, 'programmes.html', {'user': logged_user, 'matieres': matieres, 'semestres': semestres})
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


def programmes_pdf(request, semestre):
 
    matieres = Matiere.objects.filter(ue__semestre__nom_semestre = semestre)
    context = dict(semestre = semestre, matieres = matieres)  
    return PDFTemplateResponse(
        request = request, template = 'programmes_pdf.html', context = context,
        filename = 'programmes.pdf', show_content_in_browser = False)



def modifierProfile(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        personne = ''
        if type(logged_user) == Etudiant:
            personne = FormEtudiant(data = request.POST or None, instance = logged_user)
        elif type(logged_user) == Postulant:
            personne = FormRensPostulant(data = request.POST or None, instance = logged_user)
        if request.POST:
            if personne.is_valid() and personne.has_changed():
                personne.save()
            return redirect('/profile')
        return render(request, 'modif_profile.html', {'user': logged_user, 'form': personne})
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    

def ajax_verification(request):
    """
    """
    if request.is_ajax() and request.GET:
        if ('type' in request.GET) and ('valeur' in request.GET):
            message, statut, test = '', '', ''
            if request.GET['type'] == 'email':
                try:
                    test = forms.EmailField().clean(request.GET['valeur'])
                except forms.ValidationError:
                    message, statut = "Ceci n'est pas une adresse électronique.", 'erreur'
                else:
                    users = User.objects.all()
                    trouve = False
                    for user in users:
                        if user.email == test:
                            trouve = True
                            break
                    if trouve:
                        message, statut = "Cette adresse électronique est déjà prise.", 'warning'
            elif request.GET['type'] == 'pseudo':
                try:
                    test = forms.CharField(min_length=3).clean(request.GET['valeur'])
                except forms.ValidationError:
                    message, statut = "Ceci ne peux être un nom d'utilisateur.", 'erreur'
                else:
                    try:
                        User.objects.get(username = test)
                    except User.DoesNotExist:
                        pass
                    else:
                        message, statut = "Ce nom d'utilisateur est déjà pris.", 'warning'        
            return JsonResponse({'statut': statut, 'message': message})
    return JsonResponse({'erreur': 'Problème de connexion au serveur'})    


def ajax_changer_departement(request):
    """
    """
    if request.is_ajax() and request.GET:
        if ('ufr' in request.GET) and ('niveau' in request.GET):
            departement = serialize(format = 'json', queryset = Departement.objects.filter(ufr = request.GET['ufr']))
            if request.GET['niveau'] == 'Master':
                formation = serialize(format = 'json', queryset = Master.objects.filter(ufr = request.GET['ufr'], niveau = request.GET['niveau']))
            donnees = {'departement': departement, 'formation': formation if (request.GET['niveau'] == 'Master') else None}
            return JsonResponse(donnees)
    return JsonResponse({'erreur': 'Problème de connexion  au serveur'})


def ajax_changer_formation(request):
    """
    """
    if request.is_ajax() and request.GET:
        if ('dpt' in request.GET) and ('niveau' in request.GET):
            class ChampsFormation(forms.Form):
                if request.GET['niveau'] == 'master':
                    formation = forms.ModelChoiceField(queryset=Master.objects.filter(dpt = request.GET['dpt'] or None), empty_label = '--------')
                elif request.GET['niveau'] == 'doctorat':
                    formation = forms.CharField(label='Thèse', max_length=1000)
                
                @property
                def helper(self):
                    helper = FormHelper()
                    helper.form_tag = False
                    helper.disable_csrf = True
                    helper.include_media = False
                    helper.form_class ='form-horizontal'
                    helper.label_class = 'col-4'
                    helper.field_class = 'col-8'
                    return helper
            champ = render_crispy_form(ChampsFormation())
            donnees = {'formation': champ}
            
            return JsonResponse(data = donnees, safe = False)
    return  JsonResponse({'erreur': 'Problème de connexion  au serveur'})
