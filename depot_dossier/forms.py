'''
Created on 26 sept. 2018

@author: parice02
'''

from django import forms
from common.models import UFR, Departement
from depot_dossier.models import Postulant, DocumentId, Scolaire, Stage, Professionnel, Master, Dossier, Doctorat, Autre, Universitaire, \
    Fichiers, AttestationTravail, AttestationAutre, AttestationStage
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.layout import Layout, Div, Submit, Hidden, Reset#, HTML
#from crispy_forms.bootstrap import UneditableField
from crispy_forms.helper import FormHelper


class FormRensPostulant(forms.ModelForm):
    """
    Formulaire plus complet sur un postulant
    """
    @property
    def helper(self):
        helper = FormHelper()
        helper.form_show_labels = False
        helper.form_class = 'mb-5'
        helper.include_media = False
        helper.layout = Layout(
            Div(
                Div('nom', 'dateNaissance', 'ville', 'numTel', css_class = 'col-md-4 mb-3'),
                Div('prenom', 'lieuNaissance', 'region', css_class = 'col-md-4 mb-3'),
                Div('sexe', 'nationalite', 'pays', css_class = 'col-md-4 mb-3'),
                css_class = 'form-row'
                ),
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
            'dateNaissance': DatePickerInput(options={'format': 'DD/MM/YYYY'},
                    attrs={'data-toggle': 'popover', 'data-content': 'Veuillez entrer votre date de naissance.'}),
            'nom': forms.TextInput(attrs={'placeholder': 'votre nom', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir votre nom de famille.', 'class': 'form-control  form-group',}),
            'prenom': forms.TextInput(attrs={'placeholder': 'votre prénom', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir votre (vos) prénom(s).', 'class': 'form-control form-group',}),
            'numTel': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'numéro de téléphone',
                'data-toggle': 'popover', 'data-content':'Veuillez saisir votre numéro de téléphone.', 'class': 'form-control form-group',}),
            'nationalite': forms.TextInput(attrs={'placeholder': 'nationalité', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir votre nationalité.', 'class': 'form-control form-group',}),
            'ville': forms.TextInput(attrs={'placeholder': 'ville de résidence', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir le nom de la ville où vous vivez.', 'class': 'form-control form-group',}),
            'lieuNaissance': forms.TextInput(attrs={'placeholder': 'lieu de naissance', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir votre lieu de naissance.', 'class': 'form-control form-group',}),
            'region': forms.TextInput(attrs={'placeholder': 'région (état) de résidence', 'data-toggle': 'popover',
                'data-content':'Veuillez saisir votre région (état).', 'class': 'form-control form-group',}),
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
    dpts = forms.ModelChoiceField(label = 'Département', queryset= Departement.objects.all(), empty_label = '--------')
    niveaux = forms.ChoiceField(label = 'Niveau', choices = (('Master', 'Master'), ('Doctorat','Doctorat')))
    formation = forms.ModelChoiceField(queryset= Master.objects.all(), empty_label = '--------', required=False)
     
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
            Div('ufr', css_id='div_ufr'),
            Div('dpts', css_id='div_dpt'),
            Div('niveaux', css_id='div_niveau'),
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
        helper.form_class ='form-horizontal mb-5'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
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
        helper.form_class ='form-horizontal mb-5'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
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
        helper.form_class ='form-horizontal mb-5'
        helper.label_class = 'col-4'
        helper.field_class = 'col-8'
        helper.layout = Layout(
            'type_doc', 'numero_doc', 'lieuEtablissement', 'dateEtablissement', 'dateExpiration',
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
        

       
class FormDossier(forms.ModelForm):
    """
    Formulaire permettant création du dossier étudiant
    """
    class Meta:
        model = Dossier
        fields = ('numero_dossier', 'etat_traitement',)
        
    def clean(self):
        data_cleaned = super(FormDossier, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")
        

       
class FormParcoursScolaireHelper(FormHelper):
    """
    """
    def __init__(self, *args, **kwargs): 
        super(FormParcoursScolaireHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.include_media = False
        self.form_show_labels = False
        self.label_class = 'sr-only'
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('etablissement_sco', css_class='col-5'),
                Div('classe', css_class='col-2'),
                Div('moyenne_ann', css_class='col-2'),
                Div('annee_sco', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row')
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
        }
    
    
    def clean(self):
        data_cleaned = super(FormParcoursScolaire, self).clean()
        
        if data_cleaned:
            return data_cleaned
        else:
            raise forms.ValidationError("Veuillez vérifier les information saisies.")


class FormParcoursUniversitaire(forms.ModelForm):
    """
    """
    class Meta:
        model = Universitaire
        exclude = ('etudiant',)
        widgets = {
            'etablissement_univ': forms.TextInput(attrs = {'placeholder': "Nom de l'établissement"}),
            'formation': forms.TextInput(attrs = {'placeholder': "Formation suivie"}),
            'niveau_etude': forms.TextInput(attrs = {'placeholder': "Semestre"}),
            'moyenne_semestre': forms.NumberInput(attrs={'placeholder': 'Moyenne Semestre'}),
            'annee_univ': forms.TextInput(attrs = {'placeholder': "Année universitaire"}),
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
        self.form_show_labels = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('etablissement_univ', css_class='col-2'),
                Div('niveau_etude', css_class='col-2'),
                Div('formation', css_class='col-3'),
                Div('moyenne_semestre', css_class='col-2'),
                Div('annee_univ', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row')
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
            'annee_stage': forms.TextInput(attrs={'placeholder': "Année académique"}),
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
        self.form_show_labels = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('structure', css_class='col-3'),
                Div('type_structure', css_class='col-2'),
                Div('theme', css_class='col-4'),
                Div('annee_stage', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row')
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
            'annee_travail': forms.TextInput(attrs={'placeholder': "Année académique"}),
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
        self.form_show_labels = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('employeur', css_class='col-5'),
                Div('poste', css_class='col-4'),
                Div('annee_travail', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row')
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
            'annee_autre': forms.TextInput(attrs={'placeholder': 'Année académique'}),
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
        self.form_show_labels = False
        self.render_required_fields = True
        self.layout = Layout(
            Div(
                Div('type', css_class='col-3'),
                Div('structure', css_class='col-4'),
                Div('poste', css_class='col-2'),
                Div('annee_autre', css_class='col-2'),
                Div('DELETE', css_class='col-1'),
                css_class = 'form-row')
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
            'curriculum': forms.ClearableFileInput(attrs={'accept':'.pdf'}),
            'diplome_bac': forms.ClearableFileInput(attrs={'accept':'.pdf, image/*'}),
            'attestation_licence': forms.ClearableFileInput(attrs={'accept':'.pdf'}),
            'attestation_master': forms.ClearableFileInput(attrs={'accept':'.pdf'}),
            }
        
    def clean(self):
        data_cleaned = super(FormFichiers, self).clean()
        
        if data_cleaned:
            return data_cleaned
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
            Div('curriculum'),
            Div('diplome_bac'),
            Div('attestation_licence'),
            Div('attestation_master'),
            )
        return helper
    
class FormAttestationTravail(forms.ModelForm):
    
    class Meta:
        model = AttestationTravail
        fields = '__all__'
        widgets = {
            'nom_AtTra': forms.TextInput(attrs={'placeholder': "Intitulé de l'attestation"}),
            }
        
    #def __init__(self, *args, **kwargs):
        #super(FormAttestationTravail, self).__init__(*args, kwargs)
        #self.fields['emploi'].queryset = Professionnel.objects.filter(employe=self.instance.emploi.employe)
        
    def clean(self):
        data_cleaned = super(FormAttestationTravail, self).clean()
        
        if data_cleaned:
            return data_cleaned
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
                Div('nom_AtTra', css_class='col-4'), Div('emploi', css_class='col-4'), Div('attestation_travail', css_class='col-4'),
                css_class='row')
            )


class FormAttestationStage(forms.ModelForm):
    
    class Meta:
        model = AttestationStage
        fields = '__all__'
        widgets = {
            'nom_AtSta': forms.TextInput(attrs={'placeholder': "Intitulé de l'attestation"}),
            }
        
    #def __init__(self, *args, **kwargs):
        #super(FormAttestationStage, self).__init__(*args, kwargs)
        #self.fields['stage'].queryset = Stage.objects.filter(stagiaire=self.instance.emploi.employe)
        
    def clean(self):
        data_cleaned = super(FormAttestationStage, self).clean()
        
        if data_cleaned:
            return data_cleaned
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
                Div('nom_AtSta', css_class='col-4'), Div('stage', css_class='col-4'), Div('attestation_stage', css_class='col-4'),
                css_class='row')
            )
        
        

class FormAttestationAutre(forms.ModelForm):
    
    class Meta:
        model = AttestationAutre
        fields = '__all__'
        widgets = {
            'nom_AtAu': forms.TextInput(attrs={'placeholder': "Intitulé de l'attestation"}),
            }
        
    #def __init__(self, *args, **kwargs):
        #super(FormAttestationAutre, self).__init__(*args, kwargs)
        #self.fields['emploi'].queryset = Professionnel.objects.filter(employe=self.instance.emploi.employe)
        
    def clean(self):
        data_cleaned = super(FormAttestationAutre, self).clean()
        
        if data_cleaned:
            return data_cleaned
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
                Div('nom_AtAu', css_class='col-4'), Div('emploi', css_class='col-4'), Div('attestation_autre', css_class='col-4'),
                css_class='row')
            )