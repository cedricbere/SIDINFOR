'''
Created on 26 sept. 2018

@author: parice02
'''

from django import forms
from Rapport.models import UFR, Departement
from DepotDoc.models import Postulant, Formation, DocumentId, Dossier
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.layout import Layout, Div, Submit, Hidden
from crispy_forms.helper import FormHelper

class FormRensPostulant(forms.ModelForm):
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_show_labels = False
        helper.include_media = False
        helper.layout = Layout(
            Div(
                Div('nom', 'dateNaissance', 'ville', 'numTel', css_class = 'col-md-4 mb-3'),
                Div('prenom', 'lieuNaissance', 'region', css_class = 'col-md-4 mb-3'),
                Div('sexe', 'nationalite', 'pays', css_class = 'col-md-4 mb-3'),
                css_class = 'form-row'
                ),
                Hidden('type_form', 'postulant'),
                Submit('submit', 'Sauvergarder'),)
        return helper
    
    class Meta:
        model = Postulant
        exclude = ('compte', 'formation', 'documentId', 'dossier')
        widgets = {
            'dateNaissance': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                    attrs={'data-toggle': 'popover', 'data-content': 'Veuillez entrer votre date de naissance.'}),
            #'dateNaissance': forms.DateInput(attrs={'type': 'date', 'data-toggle': 'popover', 'data-content': 'Veuillez saisir votre date de naissance.', 'class': 'form-control  form-group',}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre nom de famille.', 'class': 'form-control  form-group',}),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre (vos) prénom(s).', 'class': 'form-control form-group',}),
            'numTel': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'numéro de téléphone', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre numéro de téléphone.', 'class': 'form-control form-group',}),
            'nationalite': forms.TextInput(attrs={'placeholder': 'nationalité', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre nationalité.', 'class': 'form-control form-group',}),
            'ville': forms.TextInput(attrs={'placeholder': 'ville de résidence', 'data-toggle': 'popover', 'data-content':'Veuillez saisir le nom de la ville où vous vivez.', 'class': 'form-control form-group',}),
            'lieuNaissance': forms.TextInput(attrs={'placeholder': 'lieu de naissance', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre lieu de naissance.', 'class': 'form-control form-group',}),
            'region': forms.TextInput(attrs={'placeholder': 'région (état) de résidence', 'data-toggle': 'popover', 'data-content':'Veuillez saisir votre région (état).', 'class': 'form-control form-group',}),
            'sexe': forms.Select(attrs = {'class': 'form-control form-group'}),
            'pays': forms.Select(attrs = {'class': 'form-control form-group'}),        
            }
        
        
    def clean(self):
        cleaned_data = super(FormRensPostulant, self).clean()       
        if cleaned_data:
            return cleaned_data
        raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
        
        
        
class FormFormation(forms.Form):
    ufr = forms.ModelChoiceField(label = 'UFR', queryset = UFR.objects.all(), empty_label = '--------')
    dpts = forms.ModelChoiceField(label = 'Département', queryset= Departement.objects.all(), empty_label = '--------')
    niveaux = forms.ChoiceField(label = 'Niveau', choices = (('master', 'Master'), ('doctorat','Doctorat')), )
    formation = forms.ModelChoiceField(queryset= Formation.objects.all(), empty_label = '--------')
     
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        return helper
    
    def clean(self):
        data_cleaned = super(FormFormation, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")


class FormDocumentId(forms.ModelForm):
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        helper.layout = Layout(
            'type_doc', 'numero_doc', 'lieuEtablissement', 'dateEtablissement', 'dateExpiration',
            Hidden('type_form', 'documentId'),
            Submit('submit', 'Sauvegarder'),
            )
        return helper
    
    
    class Meta:
        model = DocumentId
        fields = '__all__'
        widgets = {
            'numero_doc': forms.TextInput(attrs={'placeholder': 'Entrez le numéro du document'}),
            'lieuEtablissement': forms.TextInput(attrs={'data-toggle': 'popover', 'data-content': "Veuillez entrer le lieu d'établissement du document."}),
            'dateEtablissement': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                attrs={'data-toggle': 'popover', 'data-content': "Veuillez entrer la date d'établissement du document."}),
            'dateExpiration': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                attrs={'data-toggle': 'popover', 'data-content': "Veuillez entrer la date d'expiration du document."}),
            }
        
    def clean(self):
        data_cleaned = super(FormDocumentId, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
        
class FormDossier(forms.ModelForm):
    
    class Meta:
        model = Dossier
        fields = ('numero', 'etat_traitement',)
        
    def clean(self):
        data_cleaned = super(FormDossier, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        