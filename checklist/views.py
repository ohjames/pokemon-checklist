from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

import uuid
import requests
from django.core.files.base import ContentFile

import os
import sys
sys.path.append(os.path.abspath('../'))
from .scraper import PokeScraper

from .models import Pokemon

from django.http import HttpResponse

# Create your views here.
def scraper(user):
    df = PokeScraper('https://www.serebii.net/pokemon/gen1pokemon.shtml').create_gen_df()
    df.drop(columns=['Count', 'Abilities', 'HP', 'Att', 'Def', 'S.Att', 'S.Def', 'Spd'], inplace=True)
    new_pokemon = []
    for index, row in df.iterrows():
        number = row['No.']
        name = row['Name']
        image_url = row['Pic']
        p = Pokemon.objects.filter(number=number, name=name, user=user).first()
        if p:
            # updating existing pokemon with new image
            if not p.image:
                image_name = f'{number}.png'
                image_file = get_image_from_url(image_url)
                p.image.save(image_name, image_file)
                p.save()
        else:
            # Create new pokemon with new image
            image_name = f'{number}.png'
            image_file = get_image_from_url(image_url)
            p = Pokemon(number=number, name=name, user=user, identifier=uuid.uuid4())
            p.image.save(image_name, image_file)
            p.save()
        new_pokemon.append(p)
    # Save new Pokemon objects to database
    Pokemon.objects.bulk_create(new_pokemon)
    # return render(request, 'scraper.html', {'new_pokemon': new_pokemon})

def get_image_from_url(url):
    response = requests.get(url)
    return ContentFile(response.content)

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
            user = form.save(commit=False)
            user.save()
            # scraper(user)
            user_pokemon = Pokemon.objects.filter(user=None)
            for pokemon in user_pokemon:
                pokemon.user = user
                pokemon.identifier = str(uuid.uuid4())
            Pokemon.objects.bulk_create(user_pokemon)
            # Authenticate and login user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        return render(request, 'checklist/register.html', {'form': form})
            # for pokemon in user_pokemon:
            #     pokemon.user = user
            #     pokemon.identifier = str(uuid.uuid4())
            # Pokemon.objects.bulk_create(user_pokemon)

class PokemonList(ListView):
    model = Pokemon
    template_name = 'checklist/pokemon_list.html'
    context_object_name = 'pokemon'

    def get_queryset(self):
        # queryset = super().get_queryset()
        # return queryset.filter(user=self.request.user)
        return Pokemon.objects.filter(user=self.request.user)
        # print(pokemon)
        # return pokemon

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'checklist/dashboard.html'

class MarkPokemonView(View):
    def post(self, request):
        pokemon_ids = request.POST.getlist('pokemon')
        for pokemon_id in pokemon_ids:
            pokemon = Pokemon.objects.get(pk=pokemon_id)
            pokemon.completed = True
            pokemon.save()
        return redirect('pokemon_list')