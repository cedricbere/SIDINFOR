#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
Created on 22 mai 2018

@author: parice02
'''

from django import forms
from depot_rapport.models import Rapport, Stage, Soutenance
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Hidden, Div#, Reset
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput



class FormStage(forms.ModelForm):
    
    class Meta:
        model = Stage
        exclude = ('stagiaire',)
        widgets = {
            'lieu_stage': forms.TextInput(attrs={'placeholder': "Nom de structure d'accueil"}),
            'date_debut': DatePickerInput(options = {'format': 'DD/MM/YYYY'},
                        attrs={'placeholder': 'format: dd-mm-aaaa'}),
            'etat_stage': forms.Select(attrs={'placeholder': "Choisir l'état d'avancement de votre stage"}),
            'maitre_stage': forms.TextInput(attrs={'placeholder': 'Ex:, Titre Prénom(s) Nom(s), Fonction'}),
            'superviseur_stage': forms.TextInput(attrs={'placeholder': 'Ex:, Titre Prénom(s) Nom(s), Fonction'}),
            }
        
    @property   
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='form-horizontal mb-5'
        helper.label_class = 'col-3'
        helper.field_class = 'col-6'
        helper.layout = Layout(
            'lieu_stage', 'etat_stage', 'date_debut', 'superviseur_stage', 'maitre_stage',
            Hidden('type_form', 'form_stage'),
            Div(
                Submit('submit', 'Sauvegarder'),
                #Reset('reset', 'Tout effacer'),
                css_class='btn btn-group mt-5'))
        return helper
    
    def clean(self):
        cleaned_data = super(FormStage, self).clean()
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError('Veuillez vérifier les information saisies.', code = 'invalid')



class FormRapport(forms.ModelForm):
    
    class Meta:
        model = Rapport
        exclude = ('date_premier_chargement', 'date_modification', 'auteur', 'annee_academique', 'stage')
        widgets = {
            'theme': forms.TextInput(attrs={'placeholder': '---ici le thème ---'}),
            'domaine_metier': forms.TextInput(attrs={'placeholder': '---domaine métier---'}),
            'resume': forms.Textarea(attrs={'cols':25, 'rows': 3, 'placeholder': '--- ici le résumé de votre rapport---',}),
            'mots_cles': forms.TextInput(attrs={'placeholder': '--- mots clés liés au thème ---'}),
            'fichier_rapport': forms.ClearableFileInput(attrs={'accept': '.pdf'}),
            }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='form-horizontal mb-5'
        helper.label_class = 'col-3'
        helper.field_class = 'col-6'
        helper.layout = Layout(
            'theme', 'domaine_metier', 'resume', 'mots_cles', 'fichier_rapport',
            Div(
                Div(css_class='offset-3'),
                Div(Div(css_id='barre_progression'), css_class='col-4'),
                Div(css_id='pourcentage', css_class='col-2'),
                css_class='row invisible', css_id='div_progress'),
            Hidden('type_form', 'form_rapport'),
            Div(
                Submit('submit', 'Sauvegarder'),
                #Reset('reset', 'Tout effacer'),
                css_class='btn btn-group mt-5'))
        return helper
        
        
    def clean(self):
        cleaned_data = super(FormRapport, self).clean()
        
        if cleaned_data:
            if cleaned_data['fichier_rapport'].content_type != 'application/pdf':
                raise forms.ValidationError("Votre fichier n'est pas un document PDF.", code = 'invalid')  
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.", code = 'invalid')
              


        
        
class FormSoutenance(forms.ModelForm):
    
    class Meta:
        model = Soutenance
        exclude = ('jury', 'pv', 'etudiant', 'note', 'stage', 'rapport')
        widgets = {
            'date_prevue': DatePickerInput(options = {'format': 'DD/MM/YYYY'}, attrs={'placeholder': 'format: dd-mm-aaaa'}),
            'date_effective': DatePickerInput(options = {'format': 'DD/MM/YYYY'}, attrs={'placeholder': 'format: dd-mm-aaaa'}),
            'heure': TimePickerInput(attrs={'placeholder': 'format: hh:mm'}),
            'salle': forms.TextInput(attrs={'placeholder': 'salle de soutenance'})
            }
        
    @property   
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='form-horizontal mb-5'
        helper.label_class = 'col-3'
        helper.field_class = 'col-6'
        helper.layout = Layout(
            'date_prevue', 'date_effective', 'salle', 'heure',
            Hidden('type_form', 'form_soutenance'),
            Div(
                Submit('submit', 'Sauvegarder'),
                #Reset('reset', 'Tout effacer'), 
                css_class='btn btn-group mt-5'))
        return helper
    
    
    def clean(self):
        cleaned_data = super(FormSoutenance, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.", code = 'invalid')