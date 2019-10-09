#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.conf import settings

from common.views import user_form
from common.outils import envoyer_mail_admins, envoyer_mail


from depot_dossier.forms import FormRensPostulant, FormDocumentId, FormStage, FormStageHelper,\
    FormParcoursProfessionnel, FormParcoursProfessionnelHelper, FormMaster, FormParcoursUniversitaire, FormParcoursUniversitaireHelper, \
    FormDoctorat, FormAutreParcours, FormAutreParcoursHelper, FormFichiers, FormAttestationTravail, FormAttestationTravailHelper,\
    FormAttestationAutre, FormAttestationAutreHelper, FormAttestationStage, FormAttestationStageHelper
from depot_dossier.models import Stage, Professionnel, Autre, Universitaire, AttestationTravail, AttestationAutre, \
    AttestationStage, UserCode, Fichiers

from json import loads


# Create your views here.

# Onglet 'Pièces Jointe' à finir.
# Onget 'Curriculum', excès de formulaire lors de l'affiche ==> Coup sur la gestion dynamiques des année. Fonction 'copier dernier formulaire'
    # non foctionel
# Onglet 'Formation', si l'utilisateur change formation ==> Problème de sauvegarde

def activation_compte(request, user_name = '', code_activation = ''):
    try:
        user_code = UserCode.objects.get(code = code_activation, user__username = user_name)
    except UserCode.DoesNotExist:
        return render(request, 'activation_compte.html', {'activation': False})
    else:
        user = user_code.user
        user.is_active = True
        user.save()
        user_code.delete()
        inscrit = User.objects.get(username = user_name)
        mail_envoye = envoyer_mail(type_mail = 'confirmation', regime = 'postulant', inscrit = inscrit)
        envoyer_mail_admins(type_mail = 'confirmation', inscrit = inscrit , mail_envoye = mail_envoye)
        return render(request, 'activation_compte.html', {'activation': True})


def depot_doss(request):
    """
    """
    
    logged_user = user_form(request)
    if logged_user:
        if logged_user.type_personne != 'Postulant':
            return redirect('/accueil')
        postulant = FormRensPostulant(data = request.POST if request.POST and(request.POST['type_form'] == 'postulant') else None,
                                      instance = logged_user, prefix='post')
        formation = None
        if logged_user.formation.niveau == 'master':
            formation = FormMaster(data = request.POST if request.POST and(request.POST['type_form'] == 'formation') else None,
                        instance=logged_user.formation.master)
        elif logged_user.formation.niveau == 'doctorat':
            formation = FormDoctorat(data = request.POST if request.POST and(request.POST['type_form'] == 'formation') else None,
                        instance=logged_user.formation.doctorat)
            
        documentId = FormDocumentId(data = request.POST if request.POST and(request.POST['type_form'] == 'documentId') else None,
                                    instance = logged_user.documentId)
        
        
        #nombre_univ = Universitaire.objects.filter(etudiant=logged_user).count()
        ParcoursUniversitaireFormSet = modelformset_factory(model=Universitaire, form=FormParcoursUniversitaire, exclude=('etudiant',),
                                can_delete=True)
        parcoursUniversitaire = ParcoursUniversitaireFormSet(prefix='univ',
                data = request.POST if request.POST and(request.POST['type_form'] == 'universitaire') else None,
                queryset = Universitaire.objects.filter(etudiant=logged_user))
        helperUniversitaire = FormParcoursUniversitaireHelper()
        
        nombre_stage = Stage.objects.filter(stagiaire=logged_user).count()
        StageFormSet = modelformset_factory(model=Stage, form=FormStage, exclude=('stagiaire',),  can_delete=True)
        parcoursStage = StageFormSet(prefix='stage', data = request.POST if request.POST and(request.POST['type_form'] == 'stage') else None,
                queryset = Stage.objects.filter(stagiaire=logged_user))
        helperStage = FormStageHelper()
        
        nombre_job = Professionnel.objects.filter(employe=logged_user).count()
        ParcoursProfessionnelFormSet = modelformset_factory(model=Professionnel, form=FormParcoursProfessionnel,
                        exclude=('employe',), can_delete=True)
        parcoursProfessionnel = ParcoursProfessionnelFormSet(prefix='pro',
                data = request.POST if request.POST and(request.POST['type_form'] == 'professionnel') else None,
                queryset = Professionnel.objects.filter(employe=logged_user))
        helperProfessionnel = FormParcoursProfessionnelHelper()
        
        nombre_autre = Autre.objects.filter(employe=logged_user).count()
        ParcoursAutreFormSet = modelformset_factory(model=Autre, form=FormAutreParcours,
                        exclude=('employe',), can_delete=True)
        parcoursAutre = ParcoursAutreFormSet(prefix='autre',
                data = request.POST if request.POST and(request.POST['type_form'] == 'autre') else None,
                queryset = Autre.objects.filter(employe=logged_user))
        helperAutre = FormAutreParcoursHelper()
        
        try: fichiers = Fichiers.objects.get(postulant = logged_user)
        except: fichiers = None 
        fichiers_post = FormFichiers(data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                                files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,
                                instance = fichiers)
        
        
        AttestationTravailFormset = modelformset_factory(model=AttestationTravail, form=FormAttestationTravail, fields='__all__',                                   extra=nombre_job, max_num=nombre_job, can_delete=True)
        attestation_taravail = AttestationTravailFormset(prefix='attestTra',
                data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                 files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,
                queryset= AttestationTravail.objects.filter(emploi__employe = logged_user))
        helperAttesationTravail = FormAttestationTravailHelper()
        
        AttestationStageFormset = modelformset_factory(model=AttestationStage, form=FormAttestationStage, fields='__all__', extra=nombre_stage,
                            max_num=nombre_stage, can_delete=True)
        attestation_stage = AttestationStageFormset(prefix='attestStage',
                data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                 files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,
                queryset= AttestationStage.objects.filter(stage__stagiaire = logged_user))
        helperAttesationStage = FormAttestationStageHelper()
        
        AttestationAutreFormset = modelformset_factory(model=AttestationAutre, form=FormAttestationAutre, fields='__all__', extra=nombre_autre,
                            max_num=nombre_autre, can_delete=True)
        attestation_autre = AttestationAutreFormset(prefix='attestAutre',
                data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                 files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,
                queryset= AttestationAutre.objects.filter(emploi_autre__employe = logged_user))
        helperAttesationAutre = FormAttestationAutreHelper()
        
        
        if request.POST:
            ancre = ''
            sous_ancre = ''
            if request.POST['type_form'] == 'postulant':
                ancre = '#idContenu'
                if postulant.has_changed() and postulant.is_valid():
                    postulant.save()
                    return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
            elif request.POST['type_form'] == 'formation':
                ancre = '#formationContenu'
                if formation.has_changed() and formation.is_valid():
                    formation.save()
                    logged_user.formation = formation.instance
                    logged_user.save()
                    return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
            elif request.POST['type_form'] == 'documentId':
                ancre = '#docContenu'
                if documentId.has_changed() and documentId.is_valid():
                    documentId.save()
                    logged_user.documentId = documentId.instance
                    logged_user.save()
                    return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
            elif request.POST['type_form'] == 'universitaire':
                ancre = '#curriculumContenu'
                sous_ancre ='/#univContenu'
                if parcoursUniversitaire.has_changed() and parcoursUniversitaire.is_valid():
                    for form in parcoursUniversitaire:
                        form.instance.etudiant = logged_user
                    parcoursUniversitaire.save()
                    return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
            elif request.POST['type_form'] == 'stage':
                ancre = '#curriculumContenu'
                sous_ancre = '/#stageContenu'
                if parcoursStage.has_changed() and parcoursStage.is_valid():
                    for form in parcoursStage:
                        form.instance.stagiaire = logged_user
                    parcoursStage.save()
                    return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
            elif request.POST['type_form'] == 'professionnel':
                ancre = '#curriculumContenu'
                sous_ancre = '/#proContenu'
                if parcoursProfessionnel.has_changed() and parcoursProfessionnel.is_valid():
                    for form in parcoursProfessionnel:
                        form.instance.employe = logged_user
                    parcoursProfessionnel.save()
                    return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
            elif request.POST['type_form'] == 'autre':
                ancre = '#curriculumContenu'
                sous_ancre = '/#autreContenu'
                if parcoursAutre.has_changed() and parcoursAutre.is_valid():
                    for form in parcoursAutre:
                        form.instance.employe = logged_user
                    parcoursAutre.save()
                    return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
            elif request.POST['type_form'] == 'pieces_jointes':
                ancre = '#piecesContenu'
                pass
        return render(request, 'rens_depot.html', {'user': logged_user,
                                                   'postulant': postulant,
                                                   'formation': formation,
                                                   'document': documentId,
                                                    'parcoursUniversitaire':parcoursUniversitaire,
                                                    'helperUniversitaire': helperUniversitaire,
                                                    'parcoursStage': parcoursStage,
                                                    'helperStage': helperStage,
                                                    'parcoursProfessionnel': parcoursProfessionnel,
                                                    'helperProfessionnel': helperProfessionnel,
                                                    'parcoursAutre':parcoursAutre,
                                                    'helperAutre': helperAutre,
                                                    'fichiers_post': fichiers_post,
                                                    'attestation_travail': attestation_taravail,
                                                    'helperAttestationTravail': helperAttesationTravail,
                                                    'attestation_stage': attestation_stage,
                                                    'helperAttestationStage': helperAttesationStage,
                                                    'attestation_autre': attestation_autre,
                                                    'helperAttestationAutre': helperAttesationAutre})
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 


def annuler_reprendre_dos(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        if logged_user.type_personne != 'Postulant':
            return redirect('/accueil')
        if logged_user.dossier.etat_traitement == 'annulé':
            logged_user.dossier.etat_traitement = 'incomplet'
            logged_user.dossier.save()
        else:
            logged_user.dossier.etat_traitement = 'annulé'
            logged_user.dossier.save()
        return redirect('/depot_dossier/renseignements')
    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))



def uploader_fichier(request):
    if request.POST and (request.POST['type_form'] == 'pieces_jointes'):
        
        logged_user = user_form(request)
        
        nombre_job = Professionnel.objects.filter(employe=logged_user).count()
        nombre_autre = Autre.objects.filter(employe=logged_user).count()
        nombre_stage = Stage.objects.filter(stagiaire=logged_user).count()
        
        try: fichiers = Fichiers.objects.get(postulant = logged_user)
        except: fichiers = None 
        fichiers_post = FormFichiers(data = request.POST, files = request.FILES, instance = fichiers)
        
        AttestationTravailFormset = modelformset_factory(model=AttestationTravail, form=FormAttestationTravail,
                        fields='__all__', extra=nombre_job, max_num=nombre_job, can_delete=True)
        attestation_taravail = AttestationTravailFormset(prefix='attestTra', data = request.POST, files = request.FILES,
                queryset= AttestationTravail.objects.filter(emploi__employe = logged_user))
        
        AttestationStageFormset = modelformset_factory(model=AttestationStage, form=FormAttestationStage,
                    fields='__all__', extra=nombre_stage, max_num=nombre_stage, can_delete=True)
        attestation_stage = AttestationStageFormset(prefix='attestStage', data = request.POST, files = request.FILES,
                queryset= AttestationStage.objects.filter(stage__stagiaire = logged_user))
        
        AttestationAutreFormset = modelformset_factory(model=AttestationAutre, form=FormAttestationAutre,
                    fields='__all__', extra=nombre_autre,  max_num=nombre_autre, can_delete=True)
        attestation_autre = AttestationAutreFormset(prefix='attestAutre', data = request.POST,  files = request.FILES,
                queryset= AttestationAutre.objects.filter(emploi_autre__employe = logged_user))
    
    #print(fichiers_post)    
    if fichiers_post.has_changed() or attestation_taravail.has_changed() or attestation_stage.has_changed() or attestation_autre.has_changed():    
        liste_errors = []
        if not fichiers_post.is_valid():
            try: liste_errors[0]
            except: liste_errors.append(loads(fichiers_post.errors.as_json())) 
            #liste_errors.append(fichiers_post.errors.as_json())
        if not attestation_taravail.is_valid():
            erreurs = [champs.errors.as_json() for champs in (form for form in attestation_taravail)]
            try: liste_errors[0]
            except: liste_errors.append(loads(erreurs[0]))
            else: liste_errors[0].update(loads(erreurs[0]))
            #liste_errors.extend(erreurs)
        if not attestation_stage.is_valid():
            erreurs = [champs.errors.as_json() for champs in (form for form in attestation_stage)]
            try: liste_errors[0]
            except: liste_errors.append(loads(erreurs[0]))
            else: liste_errors[0].update(loads(erreurs[0]))
            #liste_errors.extend(attestation_stage.errors)
        if not attestation_autre.is_valid():
            erreurs = [champs.errors.as_json() for champs in (form for form in attestation_stage)]
            try: liste_errors[0]
            except: liste_errors.append(loads(erreurs[0]))
            else: liste_errors[0].update(loads(erreurs[0]))
            #liste_errors.extend(attestation_autre.errors)
        print(liste_errors)
        if len(liste_errors) != 0:
            return JsonResponse(liste_errors[0])
        if fichiers_post.has_changed():
            fichiers_post.instance.postulant = logged_user
            fichiers_post.save()
        if attestation_stage.has_changed():
            attestation_stage.save()
        if attestation_taravail.has_changed():
            attestation_taravail.save()
        if attestation_autre.has_changed():
            attestation_autre.save()
        
    return HttpResponse('ok')