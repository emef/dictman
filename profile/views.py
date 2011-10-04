from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.http import Http404

def register(request):
    if request.method == 'GET':
        f = UserCreationForm()
        return TemplateResponse(request, 'profile/register.djhtml', {'form': f})
    elif request.method == 'POST':
        post = request.POST
        f = UserCreationForm(post)
        if f.is_valid():
            user = f.save()
            user = authenticate(username=post['username'], password=post['password1'])
            if user is not None:
                login(request, user)
            return redirect('/')
    else:
        raise Http404
        
