'''
Created on 10 mai 2018

@author: parice02
'''

from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as logi, logout
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db import IntegrityError

from depot_rapport.models import Etudiant

from depot_dossier.models import Postulant, Master, UserCode
from depot_dossier.forms import FormRensPostulant, FormFormation, FormDossier, FormDoctorat

from common.outils import formater, envoyer_mail, generateur_code, envoyer_mail_admins
from common.forms import LoginForm, FormCompte, FormEtudiant, FormPostulant
from common.models import Matiere, Semestre, Departement


# Envoi de mail: reste à faire le format html



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
                #if request.META['HTTP_REFERER']:
                    #print(request.META['HTTP_REFERER'])
                    #return redirect(request.META['HTTP_REFERER'])
                return redirect('/accueil')
        return render(request, 'login.html', {'form': form, 'activer': "Identifiant et/ou mot de passe incorrecte."})              
    return render(request, 'login.html', {'form': form})
    


def inscription(request):
    """
    """
    etudiant = FormEtudiant(data= request.POST if request.POST and (request.POST['typeProfile'] == 'etudiant') else None, prefix='etud')
    postulant = FormPostulant(data= request.POST if request.POST and (request.POST['typeProfile'] == 'postulant') else None, prefix='post')
    formation = FormFormation(data= request.POST if request.POST and (request.POST['typeProfile'] == 'postulant') else None)
    compteEtudiant = FormCompte(data= request.POST if request.POST and (request.POST['typeProfile'] == 'etudiant') else None, prefix='etud')
    comptePostulant = FormCompte(data= request.POST if request.POST and (request.POST['typeProfile'] == 'postulant') else None, prefix='post')
    
    if request.POST:
        if (request.POST['typeProfile'] == 'etudiant') and etudiant.is_valid() and compteEtudiant.is_valid():
            user = User.objects.create_user(username=compteEtudiant.cleaned_data['pseudo'], email=compteEtudiant.cleaned_data['email'],
                        password=compteEtudiant.cleaned_data['password'], is_staff=False, is_active=False,
                        first_name=etudiant.cleaned_data['prenom'], last_name=etudiant.cleaned_data['nom'])
            etudiant.instance.compte = user
            etudiant.save()
            mail_envoye = envoyer_mail(regime = 'Etudiant', inscrit = user)
            envoyer_mail_admins(inscrit = etudiant.instance, mail_envoye = mail_envoye)
            
        elif (request.POST['typeProfile'] == 'postulant') and postulant.is_valid() and comptePostulant.is_valid() :
            user = User.objects.create_user(username=comptePostulant.cleaned_data['pseudo'], email=comptePostulant.cleaned_data['email'],
                        password=comptePostulant.cleaned_data['password'], is_staff=False, is_active=False,
                        first_name=postulant.cleaned_data['prenom'], last_name=postulant.cleaned_data['nom'])
            
            numero = len(Postulant.objects.all()) + 1
            numero = str(formater(numero, 5))+str(request.POST['niveaux'][0]).upper()
            dataDos = {'numero_dossier': numero, 'etat_traitement': 'attente'}
            # Problème d'unicité
            dossier = FormDossier(data = dataDos)
            if dossier.is_valid():
                dossier.save()
            
            if request.POST['niveaux'] == 'Master':
                f = Master.objects.get(pk = request.POST['formation'])
                postulant.instance.formation = f
            elif request.POST['niveaux'] == 'Doctorat':
                dataDoct = {'ufr': request.POST['ufr'], 'dpt': request.POST['dpts'], 'these_doctorat': request.POST['formation'], 
                        'niveau': request.POST['niveaux'], 'directeur_these': ''}
                doctorat = FormDoctorat(data=dataDoct)
                if doctorat.is_valid():
                    doctorat.save()
                    postulant.instance.formation = doctorat.instance
            postulant.instance.compte = user
            postulant.instance.dossier = dossier.instance
            postulant.save()
            
            while True:
                try:
                    code_user = generateur_code()
                    UserCode.objects.create(user = user, code = code_user)
                except IntegrityError: pass
                else: break
                    
            mail_envoye = envoyer_mail(regime = 'Postulant', inscrit = user, code = code_user)
            envoyer_mail_admins(inscrit = postulant.instance, mail_envoye = mail_envoye)
        else:
            return render(request, 'inscription.html', {'etudiant': etudiant, 'compteEtudiant': compteEtudiant,
                                                            'comptePostulant': comptePostulant, 'postulant': postulant, 'formation': formation})
        
        activation =  """Veuillez consulter vos mail, nous vous avons envoyé un mail."""
        return render(request, 'login.html', {'activation': activation, 'form': LoginForm()})    
    return render(request, 'inscription.html', {'etudiant': etudiant, 'compteEtudiant': compteEtudiant,
                                    'comptePostulant': comptePostulant, 'postulant': postulant, 'formation': formation})
    

def accueil (request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        return render(request, 'accueil.html', {'user': logged_user})
    return redirect('/login')



def profile(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        return render(request, 'profile.html', {'user': logged_user,})
    return redirect('/login')
    
def deconnexion(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        logout(request)
    return redirect('/login')



def programmes(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        semestres = Semestre.objects.exclude(uniteenseignement__code = None)
        matieres = Matiere.objects.all()
        return render(request, 'programmes.html', {'user': logged_user, 'matieres': matieres,
                                                   'semestres': semestres})
    return redirect('/login')



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
        if request.POST and personne.is_valid():
            if personne.has_changed():
                personne.save()
            return redirect('/profile')
        return render(request, 'modif_profile.html', {'user': logged_user, 'form': personne})
    return redirect('/login')
    
   
    
    

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
                            break;
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
    return JsonResponse({'erreur': 'Problème de connexion'})    


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
    return JsonResponse({'erreur': 'Problème de connexion'})


def ajax_changer_formation(request):
    """
    """
    if request.is_ajax() and request.GET:
        if ('dpt' in request.GET) and ('niveau' in request.GET):
            if request.GET['niveau'] == 'Master':
                formation = serialize(format = 'json', queryset = Master.objects.filter(dpt = request.GET['dpt'], niveau = request.GET['niveau']))
            donnees = {'formation': formation if (request.GET['niveau'] == 'Master') else None}
            return JsonResponse(donnees)
    return  JsonResponse({'erreur': 'Problème de connexion'})
