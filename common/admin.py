#!/usr/bin/env python
# -*- coding: utf8 -*-


'''
Created on 22 déc. 2018

@author: parice02
'''

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.urls import path
from django.template.response import TemplateResponse, get_template
from django.shortcuts import redirect
from django.db import connection

from common.models import UFR, Departement, Filiere, Matiere,\
    UniteEnseignement,  Semestre,  Classe, Carousel
from common.outils import dictfetchall

from depot_dossier.models import Postulant, Universitaire, Autre,\
    Fichiers, Stage, Professionnel, AttestationStage,\
    AttestationTravail, AttestationAutre
from depot_dossier.forms import FormValidation
from depot_dossier.outils import production_excel

from wkhtmltopdf.views import PDFTemplateResponse
from depot_rapport.models import Etudiant


class NewAdminSite(AdminSite):
    """
    Surcharge de classe django.contrib.admin.AdminSite
    """
    site_header = "SIDINFOR"
    site_title = 'sidinfor'
    index_title = "Site d'administration sidinfor"
    index_template = get_template(template_name = "index_admin.html", using = None) 


    def get_urls(self):
        urls = super().get_urls()
        
        added_urls = [
            path('activation_comptes/', self.admin_view(self.activation_comptes, cacheable = True), name = 'activation_comptes'),
            path('gestion/', self.admin_view(self.gestion, cacheable = True), name = 'gestion'),
            path('gestion/fiche_personnelle/', self.admin_view(self.fiche_perso, cacheable = True), name = 'fiche_personnelle'),
            path('gestion/<str:niveau>/', self.admin_view(self.gestion, cacheable = True), name = 'gestion'),
            path('gestion/<str:niveau>/fiche_personnelle/', self.admin_view(self.fiche_perso, cacheable = True), name = 'fiche_personnelle'),
            path('gestion/fiche_personnelle/<str:id_postulant>/', self.admin_view(self.fiche_perso, cacheable = True), name = 'fiche_personnelle'),
            path('gestion/<str:niveau>/fiche_personnelle/<str:id_postulant>/', self.admin_view(self.fiche_perso, cacheable = True),
                 name = 'fiche_personnelle'),
            path('gestion/etat_stages/', self.admin_view(self.etat_stages, cacheable = True), name = 'etat_stages'),
            path('gestion/etat_stages/<str:niveau>/', self.admin_view(self.etat_stages, cacheable = True), name = 'etat_stages'),
            path('fichier_excel/', self.admin_view(self.fichier_excel, cacheable = True), name = 'fichier_excel'),
            path('fichier_excel/<str:niveau>/', self.admin_view(self.fichier_excel, cacheable = True), name = 'fichier_excel'),
            path('liste_definitive/', self.admin_view(self.liste_definitive, cacheable = True), name = 'liste_definitive'),
            path('liste_definitive/<str:niveau>/', self.admin_view(self.liste_definitive, cacheable = True), name = 'liste_definitive'),
            path('liste_definitive_web/<str:niveau>/', self.admin_view(self.liste_definitive_web, cacheable = True), name = 'liste_definitive_web'), #debug
            path('reinitialiser/', self.admin_view(self.reinitialiser_dossiers, cacheable = True), name = 'reinitialiser'),
            path('reinitialiser/<str:niveau>/', self.admin_view(self.reinitialiser_dossiers, cacheable = True), name = 'reinitialiser'),
            ]
        return urls + added_urls

  
    def gestion(self, request, niveau=''):
        request.current_app = self.name
        if niveau:
            
            liste_postulant = Postulant.objects.filter(formation__niveau = niveau, compte__is_active = True).order_by('-sexe', '-date_naissance')
            niveau_etude = 'Licence 3' if niveau == 'master' else 'Master 2'
            parcours_univ = Universitaire.objects.filter(niveau_etude = niveau_etude)
            context = dict(self.each_context(request), liste_postulant= liste_postulant, niveau = niveau, title = 'Gestionnaire', parcours_univ = parcours_univ)
            return TemplateResponse(request, 'liste_postulants.html', context)
        else:
            context = dict(self.each_context(request), title = 'Gestionnaire')
            return TemplateResponse(request, 'gestion_admin.html', context)
        
    
    def fiche_perso(self, request, niveau = '', id_postulant = ''):
        request.current_app = self.name
        try: int(id_postulant)
        except Exception: 
            context = dict(self.each_context(request), trouve = False, title = 'Fiche Personnelle')
            return TemplateResponse(request, 'fiche_postulant.html', context)
        else:
            try: postulant = Postulant.objects.get(pk = id_postulant, formation__niveau = niveau, compte__is_active = True)
            except Exception:
                context = dict(self.each_context(request), trouve = False, title = 'Fiche Personnelle')
                return TemplateResponse(request, 'fiche_postulant.html', context)
            else:
                form_dos = FormValidation(data = request.POST or None, instance = postulant.dossier)
                if request.POST and 'validation' in request.POST:
                    if form_dos.has_changed() and form_dos.is_valid():
                        form_dos.save()
                univ = Universitaire.objects.filter(etudiant__id = id_postulant).order_by('-annee_univ')
                stage = Stage.objects.filter(stagiaire__id = id_postulant).order_by('-annee_stage')
                autre = Autre.objects.filter(employe__id = id_postulant).order_by('-annee_autre')
                travail = Professionnel.objects.filter(employe__id = id_postulant).order_by('-annee_travail')
                try: pieces_jointes = Fichiers.objects.get(postulant__id = id_postulant)
                except: pieces_jointes = None
                attestation_stage = AttestationStage.objects.filter(stage__in = stage)
                attestation_travail = AttestationTravail.objects.filter(emploi__in = travail)
                attestation_autre = AttestationAutre.objects.filter(emploi_autre__in = autre)
                context = dict(self.each_context(request), trouve = True, postulant = postulant,
                    univs = univ, stages = stage, autres = autre, travail = travail,
                    pieces_jointes = pieces_jointes, attestation_stage = attestation_stage,
                    attestation_travail = attestation_travail, attestation_autre = attestation_autre,
                    title = 'Fiche Personnelle', form_dos = form_dos)
                return TemplateResponse(request, 'fiche_postulant.html',  context)

   
    def etat_stages(self, request, niveau = ''):
        request.current_app = self.name
        with connection.cursor() as curseur:
            requete = """
            SELECT matricule, nom, prenom, etat_stage, theme, superviseur_stage, maitre_stage, date_prevue
            FROM common_classe, common_personne
            INNER JOIN depot_rapport_etudiant ON depot_rapport_etudiant.personne_ptr_id = common_personne.id
            LEFT JOIN depot_rapport_stage ON depot_rapport_stage.stagiaire_id = common_personne.id
            LEFT JOIN depot_rapport_rapport ON depot_rapport_rapport.auteur_id = common_personne.id AND
                depot_rapport_rapport.stage_id = depot_rapport_stage.id
            LEFT JOIN depot_rapport_soutenance ON depot_rapport_soutenance.etudiant_id = common_personne.id AND
                depot_rapport_soutenance.stage_id = depot_rapport_stage.id AND
                depot_rapport_soutenance.rapport_id = depot_rapport_rapport.id
            WHERE depot_rapport_etudiant.classe_id = common_classe.id AND common_classe.nom_classe = %s
            """
            curseur.execute(requete, [niveau])
            donnees = dictfetchall(cursor = curseur)
        
        context = dict(self.each_context(request), donnees = donnees, niveau = niveau, title = 'Etat des stages')
        
        return TemplateResponse(request, 'suivi_stages.html', context)
    
    def fichier_excel(self, request, niveau = ''):
        request.current_app = self.name
        """
        """       
        production_excel(request = request, niveau = niveau)
    
        return redirect('/admin/gestion/%s' % niveau)
    
    def liste_definitive(self, request, niveau = ''):
        request.current_app = self.name
        liste_def = Postulant.objects.all()
        
        context = dict(liste_def = liste_def, niveau = niveau)
        return PDFTemplateResponse(
            request = request, template = 'liste_definitive.html', context = context,
            filename = 'liste_definitive.pdf', show_content_in_browser = False)
        
    def liste_definitive_web(self, request, niveau = ''):
        request.current_app = self.name
        liste_def = Postulant.objects.all()
        
        context = dict(liste_def = liste_def, niveau = niveau)
        return TemplateResponse(request, 'liste_definitive.html', context = context)
    
    def activation_comptes(self, request):
        request.current_app = self.name
        liste_compte = []
        if request.POST:
            for p in request.POST.keys():
                if 'etud_' in p:
                    try:
                        etudiant =  Etudiant.objects.get(pk = request.POST[p])
                        liste_compte.append(User.objects.get(etudiant = etudiant))
                    except: pass
            for compte in liste_compte:
                compte.is_active = True
                compte.save()
        liste_etudiants = Etudiant.objects.filter(compte__is_active = False)
        context = dict(self.each_context(request), title = 'Gestionnaire', liste_etudiants = liste_etudiants, page_ok = True)
        return TemplateResponse(request, 'activation_compte_etudiant.html', context)
      
    def reinitialiser_dossiers(self, request, niveau = ''):
        request.current_app = self.name
        for p in Postulant.objects.filter(formation__niveau = niveau):
            p.dossier.validation = None
            p.dossier.save()
        return redirect('/admin/gestion/%s' % niveau)

    
site_admin = NewAdminSite('admin')

site_admin.register(User)
site_admin.register(Classe)
site_admin.register(UFR)
site_admin.register(Departement)
site_admin.register(Filiere)
site_admin.register(Matiere)
site_admin.register(UniteEnseignement)
site_admin.register(Semestre)
site_admin.register(Carousel)