'''
Created on 22 mai 2018

@author: parice02
'''

from django import forms
from Rapport.models import Rapport, Stage, Soutenance
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Reset, Hidden
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class FormStage(forms.ModelForm):
    
    class Meta:
        model = Stage
        exclude = ('stagiaire',)
        widgets = {
            'lieu': forms.TextInput(attrs={'placeholder': ''}),
            'dateDebut': DatePickerInput(options = {'format': 'DD/MM/YYYY'},
                        attrs={'placeholder': ''}),
            }
        
    @property   
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        helper.layout = Layout(
            'lieu', 'etat', 'dateDebut', 'superviseur', 'maitreStage',
            Hidden('type_form', 'form_stage'),
            Submit('submit', 'Sauvegarder'),
            Reset('reset', 'Tout effacer'))
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
        exclude = ('dateEnvoi', 'dateModif', 'auteur', 'anneeAcademique')
        widgets = {
            'theme': forms.TextInput(attrs={'placeholder': '---ici le thème ---'}),
            'resume': forms.Textarea(attrs={'cols':25, 'rows': 3, 'placeholder': '--- ici le résumé de votre rapport---',}),
            'motsCle': forms.TextInput(attrs={'placeholder': '--- mots clés liés au thème ---'})
            }
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        helper.layout = Layout(
            'theme', 'resume', 'motsCle', 'fichier',
            Hidden('type_form', 'form_rapport'),
            Submit('submit', 'Sauvegarder'),
            Reset('reset', 'Tout effacer'))
        return helper
        
        
    def clean(self):
        cleaned_data = super(FormRapport, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.", code = 'invalid')
              
        
        
class FormSoutenance(forms.ModelForm):
    
    class Meta:
        model = Soutenance
        exclude = ('jury', 'pv', 'etudiant', 'note')
        widgets = {
            'datePrevu': DatePickerInput(options = {'format': 'DD/MM/YYYY'}),
            'dateEffective': DatePickerInput(options = {'format': 'DD/MM/YYYY'}),
            'heure': TimePickerInput(),
            }
        
    @property   
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        helper.layout = Layout(
            'datePrevu', 'dateEffective', 'salle', 'heure',
            Hidden('type_form', 'form_soutenance'),
            Submit('submit', 'Sauvegarder'),
            Reset('reset', 'Tout effacer'))
        return helper
    
    
    def clean(self):
        cleaned_data = super(FormSoutenance, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.", code = 'invalid')