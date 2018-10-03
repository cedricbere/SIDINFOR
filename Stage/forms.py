'''
Created on 10 mai 2018

@author: parice02
'''

from django import forms
from Rapport.models import Etudiant, UFR, Departement
from DepotDoc.models import Postulant, Formation, Dossier

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
        exclude = ('id', 'compte', 'email','numTel')
        widgets = {
            'dateNaissance': forms.DateInput(attrs={'type': 'date', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre date de naissance.'}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom','data-toggle': 'popover', 'data-content':'Veuillez saisir votre nom de famille.',}),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre (vos) prénom(s).',}),
            'matricule': forms.TextInput(attrs={'placeholder': 'votre matricule', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre matricule.',}),
            }
        
    
    def clean(self):
        cleaned_data = super(FormEtudiant, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")


class FormPostulant(forms.ModelForm):
    class Meta:
        model = Postulant
        fields = ('nom', 'prenom', 'sexe', 'dateNaissance', 'pays')
        widgets = {
            'dateNaissance': forms.DateInput(attrs={'type': 'date', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre date de naissance.'}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre nom de famille.',}),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre (vos) prénom(s).',}),            
            }

    def clean(self):
        cleaned_data = super(FormPostulant, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
     
     
class FormFormation(forms.Form):
    ufr = forms.ModelChoiceField(label = 'UFR', queryset = UFR.objects.all(), empty_label = '--------')
    dpts = forms.ModelChoiceField(label = 'Département', queryset= Departement.objects.all(), empty_label = '--------')
    niveaux = forms.ChoiceField(label = 'Niveau', choices = (('master', 'Master'), ('doctorat','Doctorat')), )
    formation = forms.ModelChoiceField(queryset= Formation.objects.all(), empty_label = '--------')
    
    def clean(self):
        data_cleaned = super(FormFormation, self).clean()
        
        if data_cleaned:
            return data_cleaned
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
        