from django.shortcuts import render, redirect
from Stage.views import user_form
from DepotDoc.forms import FormRensPostulant, FormFormation, FormDocumentId
from DepotDoc.models import Formation

# Create your views here.

def depot_doss(request):
    """
    """
    
    logged_user = user_form(request)
    if logged_user:
        postulant = FormRensPostulant(data = request.POST if request.POST and(request.POST['type_form'] == 'postulant') else None,
                                      instance = logged_user)
        initial = {'ufr': logged_user.formation.ufr, 'dpts': logged_user.formation.dpt, 'niveaux': logged_user.formation.niveau,
                   'formation': logged_user.formation} if logged_user.formation is not None else {}
        formation = FormFormation(data = request.POST if request.POST and(request.POST['type_form'] == 'formation') else None, initial=initial)
        documentId = FormDocumentId(data = request.POST if request.POST and(request.POST['type_form'] == 'documentId') else None,
                                    instance = logged_user.documentId)
        if request.POST:
            if request.POST['type_form'] == 'postulant':
                if postulant.has_changed() and postulant.is_valid():
                    postulant.save()
                else:
                    pass
            elif request.POST['type_form'] == 'formation':
                if formation.has_changed() and formation.is_valid():
                    f = Formation.objects.get(pk = request.POST['formation'])
                    logged_user.formation = f
                    logged_user.save()
                else:
                    pass
            elif request.POST['type_form'] == 'documentId':
                if documentId.has_changed() and documentId.is_valid():
                    documentId.save()
                    logged_user.documentId = documentId.instance
                    #logged_user.save()
                else:
                    pass
            return redirect('/accueil')
        return render(request, 'rens_depot.html', {'user': logged_user, 'postulant': postulant, 'formation': formation, 'document': documentId})
    return redirect('/login')