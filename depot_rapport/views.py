# -*- conding:utf8 -*-

from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.forms import FileField
from depot_rapport.forms import FormRapport, FormStage, FormSoutenance
from depot_rapport.models import Stage, Rapport, Soutenance
from common.views import user_form
from common.outils import nettoyage, sauver_fichier
from django.views.decorators.csrf import csrf_protect



# Create your views here.

# Charment de fichier via XHR à finir
# Barre de recherche pas efficace




@csrf_protect
def rens_rapport(request):
    """
        Vue permettant de gérer les formulaire d'un stage, d'un rapport de stage et d'une soutenance ainsi que leur modification respective.
        Les modifications sont sauvegardées dans la base par cette même vue.
    """
    
    logged_user = user_form(request)
    if not logged_user:
        return redirect('/login')
    try:
        stage = Stage.objects.exclude(etat = 'Fini').get(stagiaire = logged_user)
    except Exception:
        stage = None
        
    try:
        rapport = Rapport.objects.get(stage = stage)
    except Exception:
        rapport = None
        
    try:
        soutenance = Soutenance.objects.get(rapport = rapport)
    except Exception:
        soutenance = None
    total_fini = len(Stage.objects.filter(stagiaire=logged_user, etat='Fini'))
    stage_encours = len(Stage.objects.filter(stagiaire=logged_user).exclude(etat='Fini'))
    
       
    formStage = FormStage(data = request.POST if request.POST and (request.POST['type_form'] == 'form_stage') else None, instance = stage)
    formRapport = FormRapport(data = request.POST if request.POST and (request.POST['type_form'] == 'form_rapport') else None,
       files = request.FILES if request.POST and (request.POST['type_form'] == 'form_rapport') else None, instance = rapport)
    
    
    formSoutenance = FormSoutenance(data = request.POST if request.POST and (request.POST['type_form'] == 'form_soutenance') else None,
                                    instance = soutenance)
    
    erreur_stage, erreur_rapport, erreur_soutenance = '', '', ''
    ancre = ''
    
    if request.POST:
        if request.POST['type_form'] == 'form_stage':
            ancre = '#stage'
            formStage.instance.stagiaire = logged_user
            if formStage.has_changed() and formStage.is_valid():
                formStage.save()
                return redirect('/depot_rapport/depotrapport/'+ancre)
            erreur_stage = "Veuillez vous reconnecter et réessayer!"
        elif request.POST['type_form'] == 'form_rapport':
            ancre = '#rapport'
            formRapport.instance.auteur = logged_user
            formRapport.instance.annee_academique = logged_user.promotion
            formRapport.instance.stage = stage
            if formRapport.has_changed() and formRapport.is_valid():
                if stage is not None:
                    formRapport.save()
                    sauver_fichier(file_path=formRapport.instance.fichier_rapport.path, file=request.FILES['fichier_rapport'])
                    return redirect('/depot_rapport/depotrapport/'+ancre)              
            erreur_rapport = "Veuillez d'abord remplir l'onglet Stage!"
        elif request.POST['type_form'] == 'form_soutenance':
            ancre = '#soutenance'
            formSoutenance.instance.etudiant = logged_user
            formSoutenance.instance.rapport = rapport
            formSoutenance.instance.stage = stage
            if formSoutenance.has_changed() and formSoutenance.is_valid():
                if (stage is not None) and (rapport is not None):
                    formSoutenance.save()
                    return redirect('/depot_rapport/depotrapport/'+ancre)
            erreur_soutenance = "Vérifiez que vous avez déjà sauvegardé un stage et rapport!"
        #return redirect('/depot_rapport/depotrapport/'+ancre)
    return render(request, 'rens_stage.html', {'stage': formStage,
                                               'rapport': formRapport,
                                               'soutenance': formSoutenance,
                                               'user': logged_user,
                                               'erreur_stage': erreur_stage,
                                               'erreur_rapport': erreur_rapport,
                                               'erreur_soutenance': erreur_soutenance,
                                               'total_fini': total_fini,
                                               'stage_encours': stage_encours})    
    
# Fonctionnel    
def mes_rapports(request):
    """
        Vue affichant l'ensemble des stages (finis et encours) sauvegardés par l'instance étudiant encours.
    """
    logged_user = user_form(request)
    if logged_user:
        stages = Stage.objects.filter(stagiaire = logged_user)        
        return render(request, 'mes_rapports.html', {'user': logged_user, 'stages': stages})
    else:
        return redirect('/login')
    
    
    
# Fonctionnel    
def tous_rapports(request):
    """
        Vue affichant l'ensemble des satges finis sauvegardés dans la base de données.
    """
    logged_user = user_form(request)
    if logged_user:
        stages = Stage.objects.all().filter(etat = 'Fini')
        return render(request, 'tous_rapports.html',{'user': logged_user, 'stages': stages,})
    else:
        return redirect('/login')
    
    
# Cette vue n'est pas utilisé
# Code incomplet
def ajax_recherche(request):
    """
    Vue permettant de faire une recherche via AJX.
    """
    print('réception')
    if (request.GET) and ('donnees' in request.GET):
        logged_user = user_form(request)
        if logged_user:
            print('données reçues')
            donnees = nettoyage(request.GET['donnees'])
            if len(donnees) == 0:
                return render(request, 'resultats.html', {'user': logged_user})
            else:
                
                return render(request, 'resultats.html', {'user': logged_user})
        else:
            return redirect('/login')


# Ne renvoie des résultats que quand le nom et/ou le prénom de auteur son exacte par rapport aux données de recherches.
# Recherche un moyen pour effectuer les recherches dans le thème, les mots clés et les noms et prénoms des perviseurs.
def resultats(request):
    """
    Vue pour les resultats d'une recherches
    """
    logged_user = user_form(request)
    if logged_user:
        if request.method == 'POST' and 'champ' in request.POST:
            if len(request.POST['champ']) == 0:
                return render(request, 'resultats.html', {'user': logged_user})
            else:
                donnees = nettoyage(request.POST['champ']) or ''
                print(donnees)
                if len(donnees) == 0:
                    return render(request, 'resultats.html', {'user': logged_user})
                else:
                    stages = Stage.objects.filter(Q(stagiaire__nom__in = donnees) | Q(stagiaire__prenom__in = donnees)# | 
                                                #Q(rapport__theme__icontains = ' '.join(donnees)) | 
                                                #Q(rapport__motsCle__icontains = ' '.join(donnees))
                                                 )#.filter(etat = 'Fini')
                    return render(request, 'resultats.html', {'user': logged_user, 'stages': stages})
    else:
        return redirect('/login')


# Fonctionnel
# Récupère le fichier mais problème pour le lier au fumulaire encours de saisi
# 
# code incomplet 
  
def upload_fihier(request):
    """
    Vue pour le téléversement du rappart/mémoire de stage.
    """
    #file = request.FILES['fichier']
    #print(request.FILES)
    if True:
        print('reçu')
        fichier = FileField().clean(request.FILES['fichier'])
        print(fichier.name)
        print(request.user.etudiant)
        
        return HttpResponse()
    print('Non reçu')
    return HttpResponse()
        
    