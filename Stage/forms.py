'''
Created on 10 mai 2018

@author: parice02
'''

from django import forms
from Rapport.models import Etudiant
from DepotDoc.models import Postulant
from crispy_forms.layout import Layout, Submit, HTML, Column, Fieldset, Div
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper


class LoginForm(forms.Form):
    pseudo = forms.CharField(label = 'Identifiant', widget = forms.TextInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre pseudo.',
        'placeholder': 'Identifiant',
        'class': 'form-control'}))
    password = forms.CharField(label = 'Mot de passe', widget = forms.PasswordInput(attrs={
        'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre mot de passe.',
        'placeholder': 'Mot de passe',
        'class': 'form-control'})) 
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.include_media = False
        self.helper.form_class = 'form-signin'
        self.helper.layout = Layout(
                'pseudo',
                'password',
            Column(
                 Submit('submit', 'Se Connecter',),
                 HTML("<a href='%s' class='btn btn-secondary float-right'> %s </a>" % ("{% url 'inscription' %}","S'inscrire")),
                 ),           
            )
        
    
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Adresse et/ou mot de passe incorrecte.")


    
class FormEtudiant(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FormEtudiant, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.include_media = False
        self.helper.form_class ='form-horizontal'
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-8'
        self.helper.layout = Layout(
            Div(
            'nom', 'prenom', 'sexe', 'dateNaissance', 'niveau', 'filiere', 'promotion', 'matricule'),           
            )
        
        
        
    class Meta:
        model = Etudiant
        exclude = ('id', 'compte', 'email','numTel')
        widgets = {
            'dateNaissance': DatePickerInput(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez entrer votre date de naissance.'}),
            #'dateNaissance': forms.DateInput(attrs={'type': 'date', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre date de naissance.', }),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom','data-toggle': 'popover', 'data-content':'Veuillez saisir votre nom de famille.', }),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre (vos) prénom(s).', }),
            'matricule': forms.TextInput(attrs={'placeholder': 'votre matricule', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre matricule.', }),
            'sexe': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre sexe.'}),
            'niveau': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre niveau.'}),
            'filiere': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre filière.'}),
            'promotion': forms.Select(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez choisir votre promotion.'}),
            }
        
    
    def clean(self):
        cleaned_data = super(FormEtudiant, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")


class FormPostulant(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FormPostulant, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.form_class ='form-horizontal'
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-8'
        
        
    class Meta:
        model = Postulant
        fields = ('nom', 'prenom', 'sexe', 'dateNaissance', 'pays')
        widgets = {
            'dateNaissance': DatePickerInput(attrs={'data-toggle': 'popover', 'data-content': 'Veuillez entrer votre date de naissance.'}),
            #'dateNaissance': forms.DateInput(attrs={'type': 'date', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre date de naissance.'}),
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
    
    def __init__(self, *args, **kwargs):
        super(FormCompte, self).__init__(*args, *kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.include_media = False
        self.helper.form_class ='form-horizontal'
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-8'
    
    
    
    def clean(self):
        cleaned_data = super(FormCompte, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        