from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

import os
import sys
sys.path.append(os.path.abspath('../'))
from scraper import PokeScraper

from .models import Pokemon

# Create your views here.
def scraper(request):
    df = PokeScraper('https://www.serebii.net/pokemon/gen1pokemon.shtml').create_gen_df()
    df.drop(columns=['Count', 'Abilities', 'HP', 'Att', 'Def', 'S.Att', 'S.Def', 'Spd'], inplace=True)
    new_pokemon = []
    for index, row in df.iterrows():
        number = row['No.']
        name = row['Name']
        image_url = row['Pic']
        image_name = f'{number}.png'
        p = Pokemon(number=number, name=name, image=image_name, user=None,)
        new_pokemon.append(p)
        # pokemon.image.save(image_name, image_file)
        # pokemon.save()
    Pokemon.objects.bulk_create(new_pokemon)

class CustomLoginView(LoginView):
    template_name = 'checklist/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class RegisterPage(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request,'checklist/register.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_pokemon = Pokemon.objects.filter(user=None)
            for pokemon in user_pokemon:
                pokemon.user = user
            Pokemon.objects.bulk_create(user_pokemon)
            login(request, user)
            return redirect('dashboard')
        return render(request, 'checklist/register.html', {'form': form})

class PokemonList(ListView):
    model = Pokemon
    template_name = 'checklist/pokemon_list.html'
    context_object_name = 'pokemon'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'checklist/dashboard.html'
