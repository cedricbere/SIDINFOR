from django.shortcuts import render, redirect
from Stage.views import user_form

# Create your views here.

def depot_doss(request):
    """
    """
    
    logged_user = user_form(request)
    if logged_user:
        return render(request, 'rens_depot.html', {'user': logged_user})
    return redirect('/login')