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
        postulant = FormRensPostulant(data = request.POST or None, instance = logged_user)
        initial = {'ufr': logged_user.formation.ufr, 'dpts': logged_user.formation.dpt, 'niveaux': logged_user.formation.niveau,
                   'formation': logged_user.formation} if logged_user.formation is not None else {}
        formation = FormFormation(data = request.POST or None, initial=initial)
        documentId = FormDocumentId(data = request.POST or None, instance = logged_user.documentId)
        #print(documentId)
        if request.POST:
            if postulant.has_changed() and postulant.is_valid():
                postulant.save()
            elif formation.has_changed() and formation.is_valid():
                f = Formation.objects.get(pk = request.POST['formation'])
                logged_user.formation = f
                logged_user.save()
            elif documentId.has_changed() and documentId.is_valid():
                print('ok')
                documentId.save()
                logged_user.documentId = documentId.instance
                logged_user.save()
            return redirect('/accueil')
        return render(request, 'rens_depot.html', {'user': logged_user, 'postulant': postulant, 'formation': formation, 'document': documentId})
    return redirect('/login')