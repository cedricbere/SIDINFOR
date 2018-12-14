from django.shortcuts import render, redirect
from django.forms.models import modelformset_factory
#from django.views.decorators.http import require_POST
from common.views import user_form
from depot_dossier.forms import FormRensPostulant, FormDocumentId, FormParcoursScolaireHelper, FormParcoursScolaire, FormStage, FormStageHelper,\
    FormParcoursProfessionnel, FormParcoursProfessionnelHelper, FormMaster, FormParcoursUniversitaire, FormParcoursUniversitaireHelper, \
    FormDoctorat, FormAutreParcours, FormAutreParcoursHelper, FormFichiers, FormAttestationTravail, FormAttestationTravailHelper,\
    FormAttestationAutre, FormAttestationAutreHelper, FormAttestationStage, FormAttestationStageHelper
from depot_dossier.models import Scolaire, Stage, Professionnel, Autre, Postulant, Universitaire, AttestationTravail, AttestationAutre, \
    AttestationStage, UserCode
#from crispy_forms.utils import render_crispy_form
from depot_dossier.outils import retourne_labels_liste, production_excel

# Create your views here.

# Onglet 'Pièces Jointe' à fini. Problème de création dynamique des pièces en fonction des parcours
# Onget 'Curriculum', excès de formulaire lors de l'affiche ==> Coup sur la gestion dynamiques des année. Fonction 'copier dernier formulaire'
    # non foctionel
# Onglet 'Formation', problème d'AJAX sur le triage des département et/ou des formations en fonction des ufr

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
        return render(request, 'activation_compte.html', {'activation': True})


def depot_doss(request):
    """
    """
    
    logged_user = user_form(request)
    if logged_user:
        postulant = FormRensPostulant(data = request.POST if request.POST and(request.POST['type_form'] == 'postulant') else None,
                                      instance = logged_user, prefix='post')
        
        if logged_user.formation.niveau == 'Master':
            formation = FormMaster(data = request.POST if request.POST and(request.POST['type_form'] == 'formation') else None,
                        instance=logged_user.formation.master)
        elif logged_user.formation.niveau == 'Doctorat':
            formation = FormDoctorat(data = request.POST if request.POST and(request.POST['type_form'] == 'formation') else None,
                        instance=logged_user.formation.doctorat)
            
        documentId = FormDocumentId(data = request.POST if request.POST and(request.POST['type_form'] == 'documentId') else None,
                                    instance = logged_user.documentId)
        
        #nombre_sco = Scolaire.objects.filter(eleve=logged_user).count()
        ParcoursScolaireFormSet = modelformset_factory(model=Scolaire, form=FormParcoursScolaire, exclude=('eleve',),
                             can_delete=True)
        parcoursScolaire = ParcoursScolaireFormSet(prefix='sco',
                data = request.POST if request.POST and(request.POST['type_form'] == 'scolaire') else None,
                queryset = Scolaire.objects.filter(eleve=logged_user))
        helperScolaire = FormParcoursScolaireHelper()
        
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
         
        fichiers_post = FormFichiers(data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                                files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,)
        
        AttestationTravailFormset = modelformset_factory(model=AttestationTravail, form=FormAttestationTravail, fields='__all__',
                            max_num=nombre_job, can_delete=True)
        attestation_taravail = AttestationTravailFormset(prefix='attestTra',
                data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                 files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,
                queryset= AttestationTravail.objects.filter(emploi__employe = logged_user))
        helperAttesationTravail = FormAttestationTravailHelper()
        
        AttestationStageFormset = modelformset_factory(model=AttestationStage, form=FormAttestationStage, fields='__all__',
                            max_num=nombre_stage, can_delete=True)
        attestation_stage = AttestationStageFormset(prefix='attestStage',
                data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                 files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,
                queryset= AttestationStage.objects.filter(stage__stagiaire = logged_user))
        helperAttesationStage = FormAttestationStageHelper()
        
        AttestationAutreFormset = modelformset_factory(model=AttestationAutre, form=FormAttestationAutre, fields='__all__',
                            max_num=nombre_autre, can_delete=True)
        attestation_autre = AttestationAutreFormset(prefix='attestAutre',
                data = request.POST if request.POST and(request.POST['type_form'] == 'pieces_jointes') else None,
                 files = request.FILES if request.FILES and(request.POST['type_form'] == 'pieces_jointes') else None,
                queryset= AttestationAutre.objects.filter(emploi__employe = logged_user))
        helperAttesationAutre = FormAttestationAutreHelper()
        
        
        if request.POST:
            ancre = ''
            sous_ancre = ''
            if request.POST['type_form'] == 'postulant':
                ancre = '#idContenu'
                if postulant.has_changed() and postulant.is_valid():
                    postulant.save()
            elif request.POST['type_form'] == 'formation':
                ancre = '#formationContenu'
                if formation.has_changed() and formation.is_valid():
                    formation.save()
                    logged_user.formation = formation.instance
                    logged_user.save()
            elif request.POST['type_form'] == 'documentId':
                ancre = '#docContenu'
                if documentId.has_changed() and documentId.is_valid():
                    documentId.save()
                    logged_user.documentId = documentId.instance
                    logged_user.save()
            elif request.POST['type_form'] == 'scolaire':
                ancre = '#curriculumContenu'
                sous_ancre = '/#scoContenu'
                if parcoursScolaire.has_changed() and parcoursScolaire.is_valid():
                    for form in parcoursScolaire:
                        form.instance.eleve = logged_user
                    parcoursScolaire.save()
            elif request.POST['type_form'] == 'universitaire':
                ancre = '#curriculumContenu'
                sous_ancre ='/#univContenu'
                if parcoursUniversitaire.has_changed() and parcoursUniversitaire.is_valid():
                    for form in parcoursUniversitaire:
                        form.instance.etudiant = logged_user
                    parcoursUniversitaire.save()
            elif request.POST['type_form'] == 'stage':
                ancre = '#curriculumContenu'
                sous_ancre = '/#stageContenu'
                if parcoursStage.has_changed() and parcoursStage.is_valid():
                    for form in parcoursStage:
                        form.instance.stagiaire = logged_user
                    parcoursStage.save()
            elif request.POST['type_form'] == 'professionnel':
                ancre = '#curriculumContenu'
                sous_ancre = '/#proContenu'
                if parcoursProfessionnel.has_changed() and parcoursProfessionnel.is_valid():
                    for form in parcoursProfessionnel:
                        form.instance.employe = logged_user
                    parcoursProfessionnel.save()
            elif request.POST['type_form'] == 'autre':
                ancre = '#curriculumContenu'
                sous_ancre = '/#autreContenu'
                if parcoursAutre.has_changed() and parcoursAutre.is_valid():
                    for form in parcoursAutre:
                        form.instance.employe = logged_user
                    parcoursAutre.save()
            return redirect('/depot_dossier/renseignements/'+ancre+sous_ancre)
        return render(request, 'rens_depot.html', {'user': logged_user,
                                                   'postulant': postulant,
                                                   'formation': formation,
                                                   'document': documentId,
                                                    'parcoursScolaire': parcoursScolaire,
                                                    'helperScolaire': helperScolaire,
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
    return redirect('/login')


def t_admin(request, niveau=''):
    if niveau:
        liste_postulant = Postulant.objects.filter(formation__niveau = niveau.title())
        return render(request, 't_admin.html', {'liste_postulant': liste_postulant, 'niveau': niveau})
    else:
        return render(request, 'l_admin.html')


def fichier_excel(request, niveau=''):
    donnees = Postulant.objects.filter(formation__niveau = niveau.title())
    liste_entetes = retourne_labels_liste(FormRensPostulant())
    dict_donnees = {
        'informations_personnelles': {'labels': liste_entetes, 'donnees_postulants':donnees},
     }
    production_excel(dict_donnees=dict_donnees, niveau = niveau)
    return redirect('/depot_dossier/t_admin/%s'%niveau)
    
def annuler_reprendre_dos(request):
    """
    """
    logged_user = user_form(request)
    if logged_user:
        if logged_user.dossier.etat_traitement == 'annulé':
            logged_user.dossier.etat_traitement = 'attente'
            logged_user.dossier.save()
        else:
            logged_user.dossier.etat_traitement = 'annulé'
            logged_user.dossier.save()
        return redirect('/depot_dossier/renseignements')
    return redirect('/login')
