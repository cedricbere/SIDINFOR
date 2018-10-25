from django.shortcuts import render, redirect
from django.db.models import Q
from Rapport.forms import FormRapport, FormStage, FormSoutenance
from Rapport.models import Stage, Rapport, Soutenance
from Stage.views import user_form
from Stage.outils import nettoyage


# Create your views here.

def rens_rapport(request):
    """
        Vue permettant de gérer les formulaire d'un stage, d'un rapport de stage et d'une soutenance ainsi que leur modification respective.
        Les modifications sont sauvegardées dans la base par cette même vue.
    """
    
    logged_user = user_form(request)
    if not logged_user:
        return redirect('/login')
    try:
        stage = Stage.objects.get(stagiaire = logged_user)#.exclude(etat = 'Fini')
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
        
    formStage = FormStage(data = request.POST if request.POST and (request.POST['type_form'] == 'form_stage') else None, instance = stage)
    formRapport = FormRapport(data = request.POST if request.POST and (request.POST['type_form'] == 'form_rapport') else None,
       files = request.FILES if request.POST and (request.POST['type_form'] == 'form_rapport') else None, instance = rapport)
    formSoutenance = FormSoutenance(data = request.POST if request.POST and (request.POST['type_form'] == 'form_soutenance') else None,
                                    instance = soutenance)
    
    if request.POST and (request.POST['type_form'] == 'form_stage'):
        if formStage.has_changed() and formStage.is_valid():
            formStage.save()
            formStage.instance.stagiaire = logged_user
            return redirect('/accueil')
    elif request.POST and (request.POST['type_form'] == 'form_rapport'):
        if formRapport.has_changed() and formRapport.is_valid():
            if stage is not None:
                formRapport.instance.auteur = logged_user
                formRapport.instance.anneeAcademique = logged_user.promotion
                formRapport.instance.stage = stage
                formRapport.save()
                return redirect('/accueil')
            else:
                pass
    elif request.POST and (request.POST['type_form'] == 'form_soutenance'):
        if formSoutenance.has_changed() and formSoutenance.is_valid():
            if (stage is not None) and (rapport is not None):
                formSoutenance.instance.etudiant = logged_user
                formSoutenance.instance.rapport = rapport
                formSoutenance.instance.stage = stage
                formSoutenance.save()
                return redirect('/accueil')
            else:
                pass
    return render(request, 'stage.html', {'stage': formStage, 'rapport': formRapport, 'soutenance': formSoutenance, 'user': logged_user,})    
    
    
def consulterMesRapports(request):
    """
        Vue affichant l'ensemble des stages (finis et encours) sauvegardés par l'instance étudiant encours.
    """
    logged_user = user_form(request)
    if logged_user:
        stages = Stage.objects.filter(stagiaire = logged_user)        
        return render(request, 'mesrapports.html', {'user': logged_user, 'stages': stages,})
    else:
        return redirect('/login')
    
    
    
    
def consulterLesRapports(request):
    """
        Vue affichant l'ensemble des satges finis sauvegardés dans la base de données.
    """
    logged_user = user_form(request)
    if logged_user:
        stages = Stage.objects.all()#.filter(etat = 'Fini')
        return render(request, 'consulterrapports.html',{'user': logged_user, 'stages': stages,})
    else:
        return redirect('/login')
    
    

def ajax_recherche(request):
    """
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


    
def resultats(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        if request.method == 'GET' and 'champ' in request.GET:
            if len(request.GET['champ']) == 0:
                return render(request, 'resultats.html', {'user': logged_user})
            else:
                donnees = nettoyage(request.GET['champ'])
                if len(donnees) == 0:
                    return render(request, 'resultats.html', {'user': logged_user})
                else:
                    stages = Stage.objects.filter(Q(stagiaire__nom__in = donnees) | Q(stagiaire__prenom__in = donnees) | 
                                                 Q(rapport__theme__icontains = ' '.join(donnees)) | 
                                                 Q(rapport__motsCle__icontains = ' '.join(donnees)) )#.filter(etat = 'Fini')
                    return render(request, 'resultats.html', {'user': logged_user, 'stages': stages})
    else:
        return redirect('/login')
        
    