'''
Created on 10 mai 2018

@author: parice02
'''

from django import forms
from Rapport.models import Etudiant

class LoginForm(forms.Form):
    pseudo = forms.CharField(label = 'Identifiant', widget = forms.TextInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre pseudo.',
        'placeholder': 'Identifiant',}))
    password = forms.CharField(label = 'Mot de passe', widget = forms.PasswordInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre mot de passe.',
        'placeholder': 'Mot de passe'}))    
       
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Adresse et/ou mot de passe incorrecte.")


    
class FormEtudiant(forms.ModelForm):
    class Meta:
        model = Etudiant
        exclude = ('id', 'compteUser', 'email',)
        widgets = {
            'dateNaissance': forms.DateInput(attrs={'type': 'date', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre date de naissance.'}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom','data-toggle': 'popover', 'data-content':'Veuillez saisir votre nom de famille.',}),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre (vos) prénom(s).',}),
            'numTel': forms.TextInput(attrs={'placeholder': 'votre téléphone', 'data-toggle': 'popover', 'data-content':'Veuillez saisir un numéro de téléphone valide.', 'type': 'tel',}),
            'matricule': forms.TextInput(attrs={'placeholder': 'votre matricule', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre matricule.',}),
            }
        
    
    def clean(self):
        cleaned_data = super(FormEtudiant, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")





class FormCompte(forms.Form):
    pseudo = forms.CharField(label = 'Identifiant', widget = forms.TextInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre pseudo.',
        'placeholder': 'identifiant',}))
    email = forms.EmailField(label = 'Adresse électronique', widget = forms.EmailInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre e-mail.',
        'placeholder': 'adresse électronique',}))
    password = forms.CharField(label = 'Mot de passe', widget = forms.PasswordInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre mot de passe.',
        'placeholder': 'mot de passe'}))
    dPassword = forms.CharField(label = 'Confirmer', widget = forms.PasswordInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez re-saisir votre mot de passe.',
        'placeholder': 'confirmez votre mot de passe'}))
    
    def clean(self):
        cleaned_data = super(FormCompte, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")