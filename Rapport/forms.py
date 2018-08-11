'''
Created on 22 mai 2018

@author: parice02
'''

from django import forms
from Rapport.models import Rapport, Stage, Soutenance


class FormRapport(forms.ModelForm):
    
    class Meta:
        model = Rapport
        exclude = ('dateEnvoi', 'dateModif', 'auteur', 'anneeAcademique')
        widgets = {
            'theme': forms.TextInput(attrs={'placeholder': '---ici le thème ---'}),
            'resume': forms.Textarea(attrs={'cols':25, 'rows': 3, 'placeholder': '--- ici le résumé de votre rapport---',}),
            'motsCle': forms.TextInput(attrs={'placeholder': '--- mots clés liés au thème ---'})
            }
        
    def __init__(self, auteur , *args, **kwargs):
        super(FormRapport, self).__init__(*args, **kwargs)
        self.instance.auteur = auteur
        self.instance.anneeAcademique = auteur.promotion
        self.fields['stage'].queryset = Stage.objects.filter(stagiaire = self.instance.auteur).exclude(etat = 'Fini')
        
        
    def clean(self):
        cleaned_data = super(FormRapport, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
              
                        

class FormStage(forms.ModelForm):
    
    class Meta:
        model = Stage
        exclude = ('stagiaire',)
        widgets = {
            'dateDebut': forms.DateInput(attrs={'type': 'date',},),
            }
        
    def __init__(self, stagiaire, *args, **kwargs):
        super(FormStage, self).__init__(*args, **kwargs)
        self.instance.stagiaire = stagiaire
    
    def clean(self):
        cleaned_data = super(FormStage, self).clean()
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError('Veuillez vérifier les information saisies.', code = 'invalid')
        
        
        
class FormSoutenance(forms.ModelForm):
    
    class Meta:
        model = Soutenance
        exclude = ('jury', 'pv', 'etudiant', 'note')
        widgets = {
            'datePrevu': forms.DateInput(attrs = {'type': 'date',}),
            'dateEffective': forms.DateInput(attrs = {'type': 'date',}),
            'heure': forms.TimeInput(attrs = {'type': 'time',}),}
        
    def __init__(self, etudiant, *args, **kwargs):
        super(FormSoutenance, self).__init__(*args, **kwargs)
        self.instance.etudiant = etudiant
        self.fields['stage'].queryset = Stage.objects.filter(stagiaire = self.instance.etudiant)
        self.fields['rapport'].queryset = Rapport.objects.filter(auteur = self.instance.etudiant)
        
        
    def clean(self):
        cleaned_data = super(FormSoutenance, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")