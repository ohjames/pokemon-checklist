from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

import os
import sys
sys.path.append(os.path.abspath('../'))
from scraper import PokeScraper

from .models import Pokemon

# Create your views here.
class RegisterPage(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request,'checklist/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            os.system('python scraper.py')
            return redirect('checklist:pokemon_list')
        return render(request, 'checklist/register.html', {'form': form})

class PokemonList(ListView):
    model = Pokemon
    template_name = 'checklist/pokemon_list.html'
    context_object_name = 'pokemon'

class PokemonUpdateView(UpdateView):
    model = Pokemon
    fields = ['checked']
    success_url = reverse_lazy('checklist:pokemon_list')
    template_name = 'checklist/pokemon_update.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'checklist/dashboard.html'