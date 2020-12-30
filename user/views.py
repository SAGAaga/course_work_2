from django.shortcuts import render
from django.views.generic import View

from . import forms
# Create your views here.


class CreateUserView(View):
    def get(self, request):
        form = forms.CreationForm()
        return render(request, 'user/create.html', context={'form': form})

    def post(self, request):
        boundForm = forms.CreationForm(request.POST)
        if boundForm.is_valid():
            user = boundForm.save()
            return render(request, 'user/login.html')
        else:
            return render(request, 'user/create.html', context={'form': boundForm})
