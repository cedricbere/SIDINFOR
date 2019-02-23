# -*- conding:utf8 -*-
'''
Created on 10 mai 2018

@author: parice02
'''

from django import forms
from depot_rapport.models import Etudiant
from depot_dossier.models import Postulant
from crispy_forms.layout import Layout, Submit, HTML, Column, Div
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper


class LoginForm(forms.Form):
    """
    """
    pseudo = forms.CharField(label = 'Identifiant', widget = forms.TextInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre pseudo.',
        'placeholder': 'Identifiant',
        'class': 'form-control'}))
    password = forms.CharField(label = 'Mot de passe', widget = forms.PasswordInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre mot de passe.',
        'placeholder': 'Mot de passe',
        'class': 'form-control',})) 
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_show_labels = False
        helper.include_media = False
        helper.form_class = 'form-signin'
        helper.layout = Layout(
                'pseudo',
                'password',
            Column(
                 Submit('submit', 'Se Connecter',),
                 HTML("<a href='%s' class='btn btn-secondary float-right'> %s </a>" % ("{% url 'inscription' %}","S'inscrire")),
                 ),           
            )
        return helper
        
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Adresse et/ou mot de passe incorrecte.")

  
class FormEtudiant(forms.ModelForm):
    """
    """
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        helper.layout = Layout(
            Div(
            'nom', 'prenom', 'sexe', 'dateNaissance', 'niveau', 'filiere', 'promotion', 'matricule'),           
            )
        return helper
        
        
    class Meta:
        model = Etudiant
        exclude = ('id', 'compte', 'email','numTel')
        widgets = {
            'dateNaissance': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                attrs={'data-toggle': 'popover', 'data-content': 'Veuillez entrer votre date de naissance.'}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom de famille','data-toggle': 'popover', 'data-content':'Veuillez saisir votre nom de famille.', }),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre (vos) prénom(s)', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre (vos) prénom(s).', }),
            'matricule': forms.TextInput(attrs={'placeholder': 'votre matricule', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre matricule.', }),
            'sexe': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre sexe.'}),
            'niveau': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre niveau.'}),
            'filiere': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre filière.'}),
            'promotion': forms.TextInput(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre promotion.', 'placeholder': 'votre promotion Ex: 2017 - 2018'}),
            }
        
    
    def clean(self):
        cleaned_data = super(FormEtudiant, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")


class FormPostulant(forms.ModelForm):
    """
    """
    @property
    def helper(self):
        helper = FormHelper()
        helper.disable_csrf = True
        helper.form_tag = False
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        return helper
        
        
    class Meta:
        model = Postulant
        fields = ('nom', 'prenom', 'sexe', 'dateNaissance', 'pays')
        widgets = {
            'dateNaissance': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                attrs={'data-toggle': 'popover', 'data-content': 'Veuillez entrer votre date de naissance.'}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre nom de famille.',}),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre (vos) prénom(s).',}),            
            'sexe': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre sexe.'}),
            'pays': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre pays.'}),
            }

    def clean(self):
        cleaned_data = super(FormPostulant, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")    



class FormCompte(forms.Form):
    """
    """
    pseudo = forms.CharField(label = 'Identifiant', widget = forms.TextInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre pseudo.',
        'placeholder': 'identifiant',}))
    email = forms.EmailField(label = 'Adresse électronique', widget = forms.EmailInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre adresse électronique.',
        'placeholder': 'adresse électronique',}))
    password = forms.CharField(label = 'Mot de passe', widget = forms.PasswordInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre mot de passe.',
        'placeholder': 'mot de passe'}))
    dPassword = forms.CharField(label = 'Confirmer', widget = forms.PasswordInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez re-saisir votre mot de passe.',
        'placeholder': 'confirmez votre mot de passe'}))
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.disable_csrf = True
        helper.form_tag = False
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        return helper
    
    
    
    def clean(self):
        cleaned_data = super(FormCompte, self).clean()
        
        if cleaned_data:
            if cleaned_data['password'] != cleaned_data['dPassword']:
                raise forms.ValidationError("Les mots de passe sont different.") 
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        