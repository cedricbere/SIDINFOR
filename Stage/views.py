'''
Created on 10 mai 2018

@author: parice02
'''
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as logi, logout
from django.http import HttpResponse
from Stage.forms import LoginForm, FormEtudiant, FormCompte, FormPostulant
from Rapport.models import Etudiant,  Matiere, Semestre, Departement
from DepotDoc.models import Postulant, Formation
from django import forms
from DepotDoc.forms import FormRensPostulant, FormFormation, FormDossier
from crispy_forms.helper import FormHelper
from crispy_forms.utils import render_crispy_form
from Stage.outils import formater



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
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user_pseudo = form.cleaned_data['pseudo']
        user_password = form.cleaned_data['password']
        user = authenticate(request, username=user_pseudo, password=user_password)
        if user:
            if user.is_active:
                logi(request, user)
                request.session.set_expiry(0)
                return redirect('/accueil')
            return render(request, 'login.html', {'form': form, 'activer': """Ce compte n'est pas encore (ou n'est plus) activer. 
                Veuillez contacter l'admin pour plus d'information."""})
        return render(request, 'login.html', {'form': form, 'activer': "Identifiant et/ou mot de passe incorrecte."})              
    return render(request, 'login.html', {'form': form})

    



def inscription(request):
    """
    """
    etudiant = FormEtudiant(request.POST or None)
    postulant = FormPostulant(request.POST or None)
    formation = FormFormation(request.POST or None)
    compte = FormCompte(request.POST or None)
    
    if compte.is_valid():
        if request.POST['password'] == request.POST['dPassword']:
            if (request.POST['typeProfile'] == 'etudiant') and etudiant.is_valid():
                user = User.objects.create_user(username=request.POST['pseudo'], email=request.POST['email'], password=request.POST['password'],
                                   is_staff=False, is_active=False)
                etudiant.instance.email = request.POST['email']
                etudiant.instance.compte = user
                etudiant.save()
            elif (request.POST['typeProfile'] == 'postulant') and postulant.is_valid() and formation.is_valid():
                user = User.objects.create_user(username=request.POST['pseudo'], email=request.POST['email'], password=request.POST['password'],
                                    is_staff=False, is_active=False)
                numero = len(Postulant.objects.filter(formation__niveau = request.POST['niveaux'])) + 1
                numero = str(formater(numero, 3))+str(request.POST['niveaux'][0]).upper()
                dataDos = {'numero': numero, 'etat_traitement': 'attente'}
                dossier = FormDossier(data = dataDos)
                if dossier.is_valid():
                    dossier.save()
                postulant.instance.email = request.POST['email']
                f = Formation.objects.get(pk = request.POST['formation'])
                postulant.instance.formation = f
                postulant.instance.compte = user
                postulant.instance.dossier = dossier.instance
                postulant.save()
            # Code pour envoyer un mail
            else:
                return render(request, 'inscription.html', {'etudiant': etudiant, 'compte': compte, 'postulant': postulant, 'formation': formation})
            return render(request, 'login.html', {'activer': """Veuillez patienter jusqu'à l'activation de votre comptre (3 jours).
                     Si ce n'est pas fait après les 3 jours, veuillez contacter l'admin.""", 'form': LoginForm()})
        else:
            return render(request, 'inscription.html', {'etudiant': etudiant, 'postulant': postulant, 'formation': formation, 
                                                                'compte': compte, 'erreur': 'Mot de passe non identique'})   
    return render(request, 'inscription.html', {'etudiant': etudiant, 'compte': compte, 'postulant': postulant, 'formation': formation})
    

def accueil (request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        return render(request, 'accueil.html', {'user': logged_user})
    else:
        return redirect('/login')



def profile(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        return render(request, 'profile.html', {'user': logged_user,})
    else:
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
    else:
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
        return render(request, 'modifProfile.html', {'user': logged_user, 'form': personne})
    return redirect('/login')
    
   
    
def ajax_email(request):
    """
    """
    html = ''
    if (request.GET) and ('email' in request.GET):
        champ = forms.EmailField()
        try:
            champ.clean(request.GET['email'])
        except forms.ValidationError:
            html = """<p style='color: red;' class="message"> <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 8 8">
  <path d="M1.41 0l-1.41 1.41.72.72 1.78 1.81-1.78 1.78-.72.69 1.41 1.44.72-.72 1.81-1.81 1.78 1.81.69.72 1.44-1.44-.72-.69-1.81-1.78 1.81-1.81.72-.72-1.44-1.41-.69.72-1.78 1.78-1.81-1.78-.72-.72z" />
</svg> Ceci n'est pas une adresse électronique </p>"""
        else:
            try:
                User.objects.get(email = request.GET['email'])
                html = """<p style='color: blue;' class="message"> <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 8 8">
  <path d="M3.09 0c-.06 0-.1.04-.13.09l-2.94 6.81c-.02.05-.03.13-.03.19v.81c0 .05.04.09.09.09h6.81c.05 0 .09-.04.09-.09v-.81c0-.05-.01-.14-.03-.19l-2.94-6.81c-.02-.05-.07-.09-.13-.09h-.81zm-.09 3h1v2h-1v-2zm0 3h1v1h-1v-1z" />
</svg> Cette adresse électronique est déjà prise. </p>"""
            except Exception:
                html = ''
            
        finally:
            return HttpResponse(html)  
    else:
        return HttpResponse(html)
    
    
    
def ajax_pseudo(request):
    """
    """
    html = ''
    if (request.GET) and ('pseudo' in request.GET):
        champ = forms.CharField()
        try:
            champ.clean(request.GET['pseudo'])
        except forms.ValidationError:
            html = """<p style='color: red;' class="message"> <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 8 8">
  <path d="M1.41 0l-1.41 1.41.72.72 1.78 1.81-1.78 1.78-.72.69 1.41 1.44.72-.72 1.81-1.81 1.78 1.81.69.72 1.44-1.44-.72-.69-1.81-1.78 1.81-1.81.72-.72-1.44-1.41-.69.72-1.78 1.78-1.81-1.78-.72-.72z" />
</svg> Ceci ne peux être un pseudonyme </p>"""
        else:
            try:
                User.objects.get(username = request.GET['pseudo'])
                html = """<p style='color: blue;' class="message"> <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 8 8">
  <path d="M3.09 0c-.06 0-.1.04-.13.09l-2.94 6.81c-.02.05-.03.13-.03.19v.81c0 .05.04.09.09.09h6.81c.05 0 .09-.04.09-.09v-.81c0-.05-.01-.14-.03-.19l-2.94-6.81c-.02-.05-.07-.09-.13-.09h-.81zm-.09 3h1v2h-1v-2zm0 3h1v1h-1v-1z" />
</svg> Ce nom d'utilisateur est déjà pris. </p>"""
            except Exception:
                html = ''
            
        finally:
            return HttpResponse(html)  
    else:
        return HttpResponse(html)
    
    
    
def ajax_chargerDpt(request):
    """
    """
    if request.GET and ('ufr' in request.GET):
        
        class ChampsDpt(forms.Form):
            dpts = forms.ModelChoiceField(label = 'Département', queryset= Departement.objects.filter(ufr = request.GET['ufr'] or None), empty_label = '--------')
        
            def __init__(self, *args, **kwargs):
                super(ChampsDpt, self).__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_tag = False
                self.helper.disable_csrf = True
                self.helper.include_media = False
                self.helper.form_class ='form-horizontal'
                self.helper.label_class = 'col-md-4'
                self.helper.field_class = 'col-md-8'
        
        return HttpResponse(render_crispy_form(ChampsDpt()))
      
      
def ajax_chargerFormation(request):
    """
    """
    if request.GET and ('dpt' in request.GET) and ('niveau' in request.GET):
        class ChampsFormation(forms.Form):
            label = ''
            if request.GET['niveau'] == 'master':
                label = 'Formation'
            elif request.GET['niveau'] == 'doctorat':
                label = 'Spécialité'
            formation = forms.ModelChoiceField(label = label, queryset=Formation.objects.filter(dpt = request.GET['dpt'] or None, niveau = request.GET['niveau'] or None), empty_label = '--------') 
            
            def __init__(self, *args, **kwargs):
                super(ChampsFormation, self).__init__(*args, **kwargs)
                self.helper = FormHelper()
                self.helper.form_tag = False
                self.helper.disable_csrf = True
                self.helper.include_media = False
                self.helper.form_class ='form-horizontal'
                self.helper.label_class = 'col-4'
                self.helper.field_class = 'col-8'
        
        return HttpResponse(render_crispy_form(ChampsFormation()))
    


