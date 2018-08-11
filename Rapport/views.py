from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from Rapport.forms import FormRapport, FormStage, FormSoutenance
from Rapport.models import Stage, Rapport, Soutenance
from Stage.views import user_form


# Create your views here.

def rapportStage(request):
    """
        Vue permettant de gérer les formulaire d'un stage, d'un rapport de stage et d'une soutenance ainsi que leur modification respective.
        Les modifications sont sauvegardées dans la base par cette vue mais les formulaires sont affichés par d'autres vues ajax
        (ajax_modificatin...)
    """
    logged_user = user_form(request)
    if logged_user:
        dernierStage = Stage.objects.filter(stagiaire = logged_user).exclude(etat = 'Fini')
        if dernierStage:
            valeur = dernierStage[0]
        else:
            valeur = None
        
        if len(request.GET) == 0 and len(request.POST) == 0:
            stage = FormStage(stagiaire=logged_user)
            rapport = FormRapport(auteur=logged_user)
            soutenance = FormSoutenance(etudiant=logged_user)                
            return render(request, 'stage.html', {'stage': stage, 'rapport': rapport,
                            'soutenance': soutenance, 'user': logged_user, 'dernierStage': valeur,})   
        else:
            if ('modification' in request.GET) or ('modification' in request.POST):
                if len(request.GET) > 0 or len(request.POST) > 0:
                    if (request.GET) and (request.GET['type'] == 'stage'):
                        form = FormStage(data=request.GET, stagiaire=logged_user, instance=valeur)
                        if form.is_valid():
                            form.save()
                        return redirect('/Rapport/depotRapport')
                    elif (request.POST) and (request.POST['type'] == 'rapport'):
                        rapport = Rapport.objects.filter(auteur=logged_user, stage=valeur)[0]
                        form = FormRapport(data=request.POST, files=request.FILES, auteur=logged_user, instance=rapport)
                        if form.is_valid():
                            form.save()
                        return redirect('/Rapport/depotRapport')
                    elif (request.GET) and (request.GET['type'] == 'soutenance'):
                        rapport = Rapport.objects.filter(auteur=logged_user, stage=valeur)[0]
                        soutenance = Soutenance.objects.filter(etudiant=logged_user, stage=stage, rapport=rapport)[0]
                        form = FormSoutenance(data=request.GET, etudiant=logged_user, instance=soutenance)
                        if form.is_valid():
                            form.save()
                        return redirect('/Rapport/depotRapport')
            else:
                if len(request.GET) > 0 or len(request.POST) >0:
                    if (request.GET) and (request.GET['type'] == 'stage'):
                        stage = FormStage(data=request.GET, stagiaire=logged_user)
                        if stage.is_valid():
                            stage.instance.stagiaire.save()
                            stage.save()
                            return redirect('/Rapport/depotRapport')
                        else:
                            stage = FormStage(data=request.GET, stagiaire=logged_user)
                            rapport = FormRapport(auteur=logged_user)
                            soutenance = FormSoutenance(etudiant=logged_user)
                            return render(request, 'stage.html', {'stage': stage, 'rapport': rapport,
                            'soutenance': soutenance, 'user': logged_user, 'dernierStage': valeur,})
                            
                    elif (request.POST) and (request.POST['type'] == 'rapport'):
                        rapport = FormRapport(data = request.POST, files = request.FILES, auteur=logged_user)        
                        if rapport.is_valid():
                            rapport.instance.auteur.save()
                            rapport.instance.anneeAcademique.save()
                            rapport.save()
                            return redirect('/Rapport/depotRapport')
                        else:
                            stage = FormStage(stagiaire=logged_user)
                            rapport = FormRapport(data=request.POST, files=request.FILES, auteur=logged_user)
                            soutenance = FormSoutenance(etudiant=logged_user)
                            return render(request, 'stage.html', {'stage': stage, 'rapport': rapport,
                                'soutenance': soutenance, 'user': logged_user,'dernierStage': valeur,})
                            
                    elif (request.GET) and (request.GET['type'] == 'soutenance'):
                        soutenance = FormSoutenance(data = request.GET, etudiant=logged_user)
                        if soutenance.is_valid():
                            soutenance.instance.etudiant.save()
                            soutenance.save()
                            return redirect('/Rapport/depotRapport')
                        else:
                            stage = FormStage(stagiaire=logged_user)
                            rapport = FormRapport(auteur=logged_user)
                            soutenance = FormSoutenance(data=request.GET, etudiant=logged_user)
                            return render(request, 'stage.html', {'stage': stage, 'rapport': rapport,
                                'soutenance': soutenance, 'user': logged_user,'dernierStage': valeur,})                    
    else:
        return redirect('/login')
    
    
    

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
    
    
def ajax_modifStage(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        stage = Stage.objects.filter(stagiaire = logged_user).exclude(etat = 'Fini')[0]
        formStage = FormStage(instance = stage, stagiaire=logged_user).as_p()
        html = """<form method="get" action="" class="container">"""
        html += str(formStage)
        html += """
            <input type="submit" value="Enregistrer" class="btn btn-secondary"/>
            <input type="hidden" name="type" value="stage" />
            <input type="hidden" name="modification" value="modification"/>
            <a href="#" class="btn btn-danger" id="ann1">Annuler</a>
            </form>
        """
        return HttpResponse(html)
    else:
        return redirect('/login')
    

def ajax_modifRapport(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        stage = Stage.objects.filter(stagiaire = logged_user).exclude(etat = 'Fini')[0]
        rapport = Rapport.objects.filter(stage=stage, auteur=logged_user)[0]
        formRapport = FormRapport(instance = rapport, auteur=logged_user).as_p()
        return render(request, 'modifR.html', {'form': formRapport})
    else:
        return redirect('/login')


def ajax_modifSoutenance(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        stage = Stage.objects.filter(stagiaire = logged_user).exclude(etat = 'Fini')[0]
        rapport = Rapport.objects.filter(stage=stage, auteur=logged_user)[0]
        soutenance = Soutenance.objects.filter(etudiant=logged_user, stage=stage, rapport=rapport)[0]
        formSoutenance = FormSoutenance(instance = soutenance, etudiant=logged_user).as_p()
        html = """<form method="get" action="" class="container">"""
        html += str(formSoutenance)
        html += """
            <input type="submit" value="Enregistrer" class="btn btn-secondary"/>
            <input type="hidden" name="type" value="soutenance" />
            <input type="hidden" name="modification" value="modification"/>
            <a href="#" class="btn btn-danger" id="ann3">Annuler</a>
            </form
        """
        return HttpResponse(html)
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
    
    


def nettoyage(chaine = ''):
    """
    """
    try:
        str(chaine)
        ponctuation = (',', '.', ';', '!', '?', '&', '-', '_', '(', ')', '=', '"', '*', '#', '<', '>', '/', ':', '\\', '|', '[', ']', '{', '}',"'")
        newChaine = ''
        for car in chaine :
            if car in ponctuation:
                newChaine += ' '
            else:
                newChaine += car
        liste = []
        for mot in newChaine.split(' '):
            if mot != '':
                liste.append(mot)
        return liste
    except:
        return None
 
    
    
    