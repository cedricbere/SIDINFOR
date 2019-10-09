#!/usr/bin/env python
# -*- coding: utf8 -*-


'''
Created on 26 sept. 2018

@author: parice02
'''

from django import forms

from common.models import UFR, Departement

from depot_dossier.models import Postulant, DocumentId, Stage, Professionnel, Master,\
    Doctorat, Autre, Universitaire, Fichiers,\
    AttestationTravail, AttestationAutre, AttestationStage, Dossier
from depot_dossier.get_user import get_user

from bootstrap_datepicker_plus import DatePickerInput#, YearPickerInput

from crispy_forms.layout import Layout, Div, Submit, Hidden#, Reset, HTML
#from crispy_forms.bootstrap import UneditableField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML

 


class FormRensPostulant(forms.ModelForm):
    """
    Formulaire plus complet sur un postulant
    """
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_class = 'mb-5 mt-5'
        helper.label_class = ''
        helper.field_class = 'col-8'
        helper.include_media = False
        helper.layout = Layout(
            Div(
                Div(Div('nom', css_class='col-6'), Div('prenom', css_class='col-6'), css_class='row'),
                Div(Div('date_naissance', css_class='col-6'), Div('lieu_naissance', css_class='col-6'), css_class='row'),
                Div(Div('sexe', css_class='col-6'), Div('ville', css_class='col-6'), css_class='row'),
                Div(Div('region', css_class='col-6'), Div('pays', css_class='col-6'), css_class='row'),
                Div(Div('etablissement_origine', css_class='col-6'), Div('statut_post', css_class='col-6'), css_class='row'),
                Div(Div('num_tel', css_class='col-6'), css_class='row'),
                css_class = 'form-group'),
            Div(
                Hidden('type_form', 'postulant'),
                Submit('submit', 'Sauvergarder'),
                #Reset('reset', 'Effacer'),
            css_class='btn btn-group mt-5'))
        return helper
    
    class Meta:
        model = Postulant
        exclude = ('compte', 'formation', 'documentId', 'dossier', 'fichiers_post')
        widgets = {
            'date_naissance': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                    attrs={'data-toggle': 'popover', 'data-content': 'votre date de naissance.'}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom', 'data-toggle': 'popover',
                'data-content':'votre nom de famille.', 'class': 'form-control  form-group',}),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover',
                'data-content':'votre (vos) prénom(s).', 'class': 'form-control form-group',}),
            'num_tel': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'numéro de téléphone',
                'data-toggle': 'popover', 'data-content':'Veuillez saisir votre numéro de téléphone.', 'class': 'form-control form-group',}),
            #'nationalite': forms.TextInput(attrs={'placeholder': 'nationalité', 'data-toggle': 'popover',
                #'data-content':'Veuillez saisir votre nationalité.', 'class': 'form-control form-group',}),
            'ville': forms.TextInput(attrs={'placeholder': 'ville de résidence', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir le nom de la ville où vous vivez.', 'class': 'form-control form-group',}),
            'statut_post': forms.TextInput(attrs={'placeholder': 'Statut', 'data-toggle': 'popover',
                'data-content':'Votre statut professionel.', 'class': 'form-control  form-group',}),
            'lieu_naissance': forms.TextInput(attrs={'placeholder': 'lieu de naissance', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir votre lieu de naissance.', 'class': 'form-control form-group',}),
            'region': forms.TextInput(attrs={'placeholder': 'région (état) de résidence', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir votre région (état).', 'class': 'form-control form-group',}),
            'etablissement_origine': forms.Select(attrs={'data-toggle': 'popover',
                'data-content':"Veuillez saisir votre établissement d'origine.", 'class': 'form-control form-group',}),
            'sexe': forms.Select(attrs = {'class': 'form-control form-group'}),
            'pays': forms.Select(attrs = {'class': 'form-control form-group'}),        
            }
        
    def clean(self):
        cleaned_data = super(FormRensPostulant, self).clean()       
        if cleaned_data:
            return cleaned_data
        raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
               
class FormFormation(forms.Form):
    """
    """
    ufr = forms.ModelChoiceField(label = 'UFR', queryset = UFR.objects.all(), empty_label = '--------')
    dpt = forms.ModelChoiceField(label = 'Département', queryset= Departement.objects.all(), empty_label = '--------')
    niveau = forms.ChoiceField(label = 'Niveau', choices = (('master', 'Master'), ('doctorat','Doctorat')))
    formation = forms.ModelChoiceField(queryset= Master.objects.all(), empty_label = '--------')
     
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.disable_csrf = True
        helper.include_media = False
        helper.form_class = 'form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        helper.layout = Layout(
            Div('ufr', css_id='div_ufr'),
            Div('dpt', css_id='div_dpt'),
            Div('niveau', css_id='div_niveau'),
            Div('formation', css_id='div_formation'))
        return helper
    
    def clean(self):
        data_cleaned = super(FormFormation, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")


class FormDoctorat(forms.ModelForm):
    """
    """
    class Meta:
        model = Doctorat
        fields = '__all__'
        widgets = {
            #'niveau': forms.Select(attrs={'disabled': 'disabled'}),
            'directeur_these': forms.TextInput(attrs={'placeholder': 'Saisir le nom suivit de la fonction du directeur de thèse',
                    'data-toggle': 'popover', 'data-content':'Veuillez saisir le nom de votre directeur de thèse.',}),
            'these_doctorat' :forms.TextInput(attrs={'placeholder': 'Saisir le titre de votre thèse',
                    'data-toggle': 'popover', 'data-content':'Veuillez saisir le titre de votre thèse.',})}
        
    def clean(self):
        data_cleaned = super(FormDoctorat, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='mb-5 mt-5 form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-5'
        helper.add_input(Hidden('type_form', 'formation'))
        helper.add_input(Submit('submit', 'Sauvegarder', css_class='btn mt-5'))
        #helper.add_input(Submit('reset', 'Effacer', css_class='btn mt-5'))
        return helper


class FormMaster(forms.ModelForm):
    """
    """
    class Meta:
        model = Master
        exclude = ('directeur_these', )
        widgets = {
            #'niveau': forms.Select(attrs={'disabled': 'disabled'}),
            }
        
    def clean(self):
        data_cleaned = super(FormMaster, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='mb-5 mt-5 form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-5'
        helper.add_input(Hidden('type_form', 'formation'))
        helper.add_input(Submit('submit', 'Sauvegarder', css_class='btn btn-group mt-5'))
        #helper.add_input(Submit('reset', 'Effacer', css_class='btn mt-5'))
        return helper


class FormDocumentId(forms.ModelForm):
    """
    """
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_class ='mb-5 mt-5 form-horizontal'
        helper.label_class = 'col-4'
        helper.field_class = 'col-5'
        helper.layout = Layout(
            'type_doc', 'numero_doc', 'lieu_etablissement', 'date_etablissement', 'date_expiration',
            Div(
            Hidden('type_form', 'documentId'),
            Submit('submit', 'Sauvegarder'),
            #Reset('reset', 'Effacer'),
            css_class='btn btn-group mt-5'))
        return helper
    

    class Meta:
        model = DocumentId
        fields = '__all__'
        widgets = {
            'numero_doc': forms.TextInput(attrs={'placeholder': 'Entrez le numéro du document', 'data-toggle': 'popover',
                                                'data-content': "Veuillez entrer le numéro du document."}),
            'lieuEtablissement': forms.TextInput(attrs={'data-toggle': 'popover',
            'data-content': "Veuillez entrer le lieu d'établissement du document.", 'placeholder': "Lieu d'établissement de la pièce d'identité"}),
            'dateEtablissement': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                attrs={'data-toggle': 'popover', 'data-content': "Veuillez entrer la date d'établissement du document.",
                       'placeholder': "Date d'établissement du document d'identité"}),
            'dateExpiration': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                attrs={'data-toggle': 'popover', 'data-content': "Veuillez entrer la date d'expiration du document.",
                       'placeholder': "Date d'expiration du document d'identité"}),
            }
        
    def clean(self):
        data_cleaned = super(FormDocumentId, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        

'''      
class FormParcoursScolaireHelper(FormHelper):
    """
    """
    def __init__(self, *args, **kwargs): 
        super(FormParcoursScolaireHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.label_class = ''
        self.field_class = ''
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('etablissement_sco', css_class='col-5'),
                Div('classe', css_class='col-2'),
                Div('moyenne_ann', css_class='col-2'),
                Div('annee_sco', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row'),
            HTML('<hr style="border-width: 3px; border-color: #000;">')
            )
        

class FormParcoursScolaire(forms.ModelForm):
    """
    """
    class Meta:
        model = Scolaire
        exclude = ('eleve',)
        widgets = {
            'etablissement_sco': forms.TextInput(attrs = {'placeholder': "Nom de l'établissement"}),
            'classe': forms.TextInput(attrs = {'placeholder': "Classe"}),
            'moyenne_ann': forms.NumberInput(attrs = {'placeholder': "Moyenne annuelle"}),
            'annee_sco': forms.TextInput(attrs = {'placeholder': "Année soclaire"}),
            #'annee_sco': YearPickerInput(options={'format': 'YYYY - YYYY'}, attrs = {'placeholder': "Année universitaire"}),
        }
    
    
    def clean(self):
        data_cleaned = super(FormParcoursScolaire, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
'''

class FormParcoursUniversitaire(forms.ModelForm):
    """
    """
    class Meta:
        model = Universitaire
        exclude = ('etudiant',)
        widgets = {
            'etablissement_univ': forms.TextInput(attrs = {'placeholder': "Nom de l'établissement"}),
            'formation': forms.TextInput(attrs = {'placeholder': "Formation suivie"}),
            'niveau_etude': forms.TextInput(attrs = {'placeholder': "Niveau étude"}),
            'moyenne_semestre1': forms.NumberInput(attrs={'placeholder': 'Moy. 1er semestre'}),
            'moyenne_semestre2': forms.NumberInput(attrs={'placeholder': 'Moy. 2ème semestre'}),
            'intitule_diplome': forms.TextInput(attrs = {'placeholder': "Intitulé du diplôme obtenu"}),
            'etat_diplome': forms.Select(attrs = {}),
            'annee_obtention': forms.DateInput(attrs={'placeholder': "Année d'otention"}),
            #'annee_obtention': YearPickerInput(options={'format': 'YYYY'}, attrs={'placeholder': "Année d'otention"}),
            #'annee_univ': YearPickerInput(options={'format': 'YYYY - YYYY'}, attrs = {'placeholder': "Année universitaire"}),
            'annee_univ': forms.DateInput(attrs = {'placeholder': "Année académique"}),
            }
        
    def clean(self):
        data_cleaned = super(FormParcoursUniversitaire, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
        
class FormParcoursUniversitaireHelper(FormHelper):
    """
    """
    def __init__(self, *args, **kwargs): 
        super(FormParcoursUniversitaireHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('annee_univ', css_class='col-2'),
                Div('etablissement_univ', css_class='col-3'),
                Div('niveau_etude', css_class='col-2'),
                Div('formation', css_class='col-3'),
                Div('moyenne_semestre1', css_class='col-2'),
                Div('moyenne_semestre2', css_class='col-2'),
                Div('intitule_diplome', css_class='col-3'),
                Div('etat_diplome', css_class='col-2'),
                Div('annee_obtention', css_class='col-3'), 
                Div('DELETE', css_class='col-1 delete'),
                css_class = 'form-row'),
            HTML('<hr style="border-width: 3px; border-color: #000;">')
            )

class FormStage(forms.ModelForm):
    """
    """
    class Meta:
        model = Stage
        exclude = ('stagiaire',)
        widgets = {
            'structure': forms.TextInput(attrs={'placeholder': "Structure d'accueil"}),
            'theme': forms.TextInput(attrs={'placeholder': "Thème de stage"}),
            'annee_stage': forms.TextInput(attrs={'placeholder': "Période"}),
            }
        
    def clean(self):
        data_cleaned = super(FormStage, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
        
class FormStageHelper(FormHelper):
    """
    """
    def __init__(self, *args, **kwargs): 
        super(FormStageHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('structure', css_class='col-3'),
                Div('type_structure', css_class='col-2'),
                Div('theme', css_class='col-4'),
                Div('annee_stage', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row'),
            HTML('<hr style="border-width: 3px; border-color: #000;">')
            )
 
        
class FormParcoursProfessionnel(forms.ModelForm):
    """
    """
    class Meta:
        model = Professionnel
        exclude = ('employe',)
        widgets = {
            'employeur': forms.TextInput(attrs={'placeholder': "Nom de l'entreprise"}),
            'poste': forms.TextInput(attrs={'placeholder': "Poste occupé"}),
            'annee_travail': forms.TextInput(attrs={'placeholder': "Période"}),
            }
        
    def clean(self):
        data_cleaned = super(FormParcoursProfessionnel, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
   
class FormParcoursProfessionnelHelper(FormHelper):
    """
    """
    def __init__(self, *args, **kwargs): 
        super(FormParcoursProfessionnelHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('employeur', css_class='col-5'),
                Div('poste', css_class='col-4'),
                Div('annee_travail', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row'),
            HTML('<hr style="border-width: 3px; border-color: #000;">')
            )
        

class FormAutreParcours(forms.ModelForm):
    """
    """
    class Meta:
        model = Autre
        exclude =('employe',)
        widgets={
            'type': forms.TextInput(attrs={'placeholder': 'Saisir de la structure'}),
            'structure': forms.TextInput(attrs={'placeholder': 'Saisir le nom de la structure'}),
            'annee_autre': forms.TextInput(attrs={'placeholder': 'Période'}),
            'poste': forms.TextInput(attrs={'placeholder': 'poste occupé'}),
            }
        
    def clean(self):
        data_cleaned = super(FormAutreParcours, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")

     
class FormAutreParcoursHelper(FormHelper):
    """
    """
    def __init__(self, *args, **kwargs): 
        super(FormAutreParcoursHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('type', css_class='col-3'),
                Div('structure', css_class='col-4'),
                Div('poste', css_class='col-2'),
                Div('annee_autre', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row'),
            HTML('<hr style="border-width: 3px; border-color: #000;">')
            )
        
        
class FormFichiers(forms.ModelForm):
    """
    """
    class Meta:
        model = Fichiers
        exclude = ('postulant', )
        widgets={
            'photoId': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            'carteId_recto': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            'carteId_verso': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            'passport': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            'curriculum_file': forms.ClearableFileInput(attrs={'accept':'.pdf'}),
            'diplome_bac': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            'attestation_licence': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            'attestation_master': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            }
        
    def clean(self):
        cleaned_data = super(FormFichiers, self).clean()
        
        if cleaned_data:
            if (cleaned_data['curriculum_file'] and (cleaned_data['curriculum_file'].name[-4:] != '.pdf')):
                valid_error = {}
                valid_error['curriculum_file'] = forms.ValidationError("""Votre fichier n'est pas un document PDF ou pourait être corrompu.""", code = 'invalid')
                raise forms.ValidationError(valid_error)
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.form_tag = False
        helper.disable_csrf = True
        helper.label_class = 'col-3'
        helper.field_class = 'offset-4 col-5'
        helper.layout = Layout(
            Div('photoId'),
            Div('carteId_recto'),
            Div('carteId_verso'),
            Div('passport'),
            Div('curriculum_file'),
            Div('diplome_bac'),
            Div('attestation_licence'),
            Div('attestation_master'),
            )
        return helper


class FormAttestationTravail(forms.ModelForm):
    
    def __init__(self, user = get_user(), *args, **kwargs):
        #compte = kwargs.pop('user', None)
        super(FormAttestationTravail, self).__init__(*args, **kwargs)
        self.fields['emploi'].queryset = Professionnel.objects.filter(employe__compte = user)

    class Meta:
        model = AttestationTravail
        fields = '__all__'
        widgets = {
            'nom_att_tra': forms.TextInput(attrs={'placeholder': "Intitulé de l'att. de travail"}),
            'attestation_travail': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            }
            
    def clean(self):
        cleaned_data = super(FormAttestationTravail, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        

class  FormAttestationTravailHelper(FormHelper):
    """
    """
    
    def __init__(self, *args, **kwargs): 
        super(FormAttestationTravailHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.render_required_fields = True
        self.label_class = 'sr-only'
        #self.form_show_labels = False
        self.field_class = 'col-10'
        self.layout = Layout(
            Div(
                Div('nom_att_tra', css_class='col-4'),
                Div('emploi', css_class='col-3'),
                Div('attestation_travail', css_class='col-3'),
                Div('DELETE', css_class='col-1'),  css_class='row'),
            )


class FormAttestationStage(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        compte = kwargs.pop('user', None)
        super(FormAttestationStage, self).__init__(*args, **kwargs)
        self.fields['stage'].queryset = Stage.objects.filter(stagiaire__compte = compte)
    
    class Meta:
        model = AttestationStage
        fields = '__all__'
        widgets = {
            'nom_att_sta': forms.TextInput(attrs={'placeholder': "Intitulé de l'att. de stage"}),
            'attestation_stage': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            }
        
    def clean(self):
        cleaned_data = super(FormAttestationStage, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        

class  FormAttestationStageHelper(FormHelper):
    """
    """
    
    def __init__(self, *args, **kwargs): 
        super(FormAttestationStageHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.render_required_fields = True
        self.label_class = 'sr-only'
        #self.form_show_labels = False
        self.field_class = 'col-10'
        self.layout = Layout(
            Div(
                Div('nom_att_sta', css_class='col-4'),
                Div('stage', css_class='col-3'),
                Div('attestation_stage', css_class='col-3'),
                Div('DELETE', css_class='col-1'), css_class='row'),
            )
        

class FormAttestationAutre(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        compte = kwargs.pop('user', None)
        super(FormAttestationAutre, self).__init__(*args, **kwargs)
        self.fields['emploi'].queryset = Autre.objects.filter(employe__compte = compte)
    
    class Meta:
        model = AttestationAutre
        fields = '__all__'
        widgets = {
            'nom_att_au': forms.TextInput(attrs={'placeholder': "Intitulé de l'att. autre"}),
            'attestation_autre': forms.ClearableFileInput(attrs={'accept':'image/*'}),
            }
        
    def clean(self):
        cleaned_data = super(FormAttestationAutre, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
  
        
class  FormAttestationAutreHelper(FormHelper):
    """
    """
    
    def __init__(self, *args, **kwargs): 
        super(FormAttestationAutreHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.render_required_fields = True
        self.label_class = 'sr-only'
        #self.form_show_labels = False
        self.field_class = 'col-10'
        self.layout = Layout(
            Div(
                Div('nom_att_au', css_class='col-4'),
                Div('emploi_autre', css_class='col-3'),
                Div('attestation_autre', css_class='col-3'),
                Div('DELETE', css_class='col-1'), css_class='row'),
            )

class FormValidation(forms.ModelForm):
    """
    """
    class Meta:
        model = Dossier
        fields = ('commentaire_dos', 'observation_dos', 'validation')
        widgets = {
            'commentaire_dos': forms.Textarea(attrs={'placeholder': "Commentaire..."}),
            'observation_dos': forms.Textarea(attrs={'placeholder': "Observation..."}),
            }
        
    def clean(self):
        cleaned_data = super(FormValidation, self).clean()
        
        if cleaned_data:
            return cleaned_data
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
    
    @property
    def helper(self):
        helper = FormHelper()
        helper.include_media = False
        helper.label_class = 'sr-only'
        #helper.field_class = 'col-9'
        helper.form_show_labels = False
        helper.layout = Layout(
            Div(
                Div('commentaire_dos', css_class='col-4'),
                Div('observation_dos', css_class='col-4'),
                Div('validation', css_class='col-3'),
                Div(
                    Submit('submit', 'Sauvergarder'), 
                    Hidden('valid', 'valid'), css_class='btn btn-group mt-5'), css_class = 'row')
            )
        return helper
