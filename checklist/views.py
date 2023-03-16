from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django import forms
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, get_user_model

import uuid
import requests
from django.core.files.base import ContentFile

import os
import sys
sys.path.append(os.path.abspath('../'))
from .scraper import PokeScraper

from .models import Pokemon, UserPokemon

from django.http import HttpResponse

# Create your views here.
# def scraper(user):
#     df = PokeScraper('https://www.serebii.net/pokemon/gen1pokemon.shtml').create_gen_df()
#     df.drop(columns=['Count', 'Abilities', 'HP', 'Att', 'Def', 'S.Att', 'S.Def', 'Spd'], inplace=True)
#     new_pokemon = []
#     for index, row in df.iterrows():
#         number = row['No.']
#         name = row['Name']
#         image_url = row['Pic']
#         p = Pokemon.objects.filter(number=number, name=name, userpokemon=None).first()
#         if p:
#             # updating existing pokemon with new image
#             if not p.image:
#                 image_name = f'{number}.png'
#                 image_file = get_image_from_url(image_url)
#                 p.image.save(image_name, image_file)
#                 p.save()
#         else:
#             # Create new pokemon with new image
#             image_name = f'{number}.png'
#             image_file = get_image_from_url(image_url)
#             p = Pokemon(number=number, name=name, identifier=uuid.uuid4())
#             p.image.save(image_name, image_file)
#             p.save()
#         new_pokemon.append(p)
#     # Save new Pokemon objects to database
#     Pokemon.objects.bulk_create(new_pokemon)
#     # return render(request, 'scraper.html', {'new_pokemon': new_pokemon})

# def get_image_from_url(url):
#     response = requests.get(url)
#     return ContentFile(response.content)

# User = get_user_model()

# class PokemonList(LoginRequiredMixin, View):
#     template_name = 'checklist/pokemon_list.html'
#     def get(self, request):
#         user_pokemon = UserPokemon.objects.filter(user=request.user)
#         return render(request, self.template_name, {'user_pokemon': user_pokemon})

# class PokemonDetailView(LoginRequiredMixin, View):
#     template_name = 'checklist/pokemon_detail.html'
#     def get(self, request, pokemon_id):
#         pokemon = get_object_or_404(Pokemon, id=pokemon_id)
#         user_pokemon = UserPokemon.objects.filter(user=request.user, pokemon=pokemon).first()
#         return render(request, self.template_name, {'pokemon': pokemon, 'user_pokemon': user_pokemon})
    
# class ToggleCompletionView(LoginRequiredMixin, View):
#     def post(self, request, pokemon_id):
#         user_pokemon = UserPokemon.objects.filter(user=request.user, pokemon_id=pokemon_id).first()
#         if user_pokemon:
#             user_pokemon.completed = not user_pokemon.completed
#             user_pokemon.save()
#         return redirect('pokemon_detail', pokemon_id=pokemon_id)

# class DashboardView(LoginRequiredMixin, View):
#     template_name = 'checklist/dashboard.html'
#     def get(self, request):
#         return render(request, self.template_name)

# class CustomLoginView(LoginView):
#     template_name = 'checklist/login.html'
#     def get(self, request):
#         return render(request, self.template_name)
    
#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         return render(request, self.template_name, {'error_message': 'Invalid login credentials'})

class CustomLoginView(LoginView):
    template_name = 'checklist/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    
class CustomRegisterView(CreateView):
    template_name = 'checklist/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

class PokedexView(ListView):
    model = Pokemon
    context_object_name = 'pokedex'
    template_name = 'checklist/home.html'

    def get_queryset(self):
        return self.model.objects.all()

# class UserPokemonUpdateView(LoginRequiredMixin, UpdateView):
#     model = UserPokemon
#     form_class = UserPokemonForm
#     template_name = 'checklist/checklist.html'
#     success_url = reverse_lazy('checklist')
    
#     def get_queryset(self):
#         return UserPokemon.objects.filter(user=self.request.user)

# class UserPokemonCreateView(LoginRequiredMixin, CreateView):
#     model = UserPokemon
#     form_class = UserPokemonForm
#     template_name = 'checklist/checklist.html'
#     success_url = reverse_lazy('checklist')

#     def form_valid(self, form):
#         pokemon_ids = self.request.POST.getlist('pokemon')
#         pokemon_ids = [int(pokemon_id) for pokemon_id in pokemon_ids]
#         user = self.request.user
#         print('Selected Pokemon IDs:', pokemon_ids)
#         for pokemon_id in pokemon_ids:
#             try:
#                 pokemon = Pokemon.objects.get(pk=pokemon_id)
#                 user_pokemon = UserPokemon(user=user, pokemon=pokemon, completed=False)
#                 user_pokemon.save()
#                 print('Created UserPokemon:', user_pokemon)
#             except Pokemon.DoesNotExist:
#                 print('Pokemon with ID', pokemon_id, 'does not exist')
#         return super().form_valid(form)

# class ToggleCaughtView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         user_pokemon = UserPokemon.objects.get(user=request.user, pokemon__pk=pk)
#         user_pokemon.completed = request.POST.get('completed') == 'true'
#         user_pokemon.save()
#         return JsonResponse({'updated': True})
    
#     def get(self, request, pk):
#         return JsonResponse({'updated': False})

# @login_required
# def checklist(request):
#     user_pokemon_list = UserPokemon.objects.filter(user=request.user)
#     return render(request, 'checklist/checklist.html', {'user_pokemon_list': user_pokemon_list})

# class RegisterPage(View):
#     form_class = UserCreationForm
#     template_name = 'checklist/register.html'
#     # If logged in, redirect
#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})
#     # Once registered, redirect and after finishing registration, redirect
#     def post(self, request):
#         if request.user.is_authenticated:
#             return redirect('home')
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(request, username=username, password=password)
#             login(request, user)
#             return redirect('checklist')
#         return render(request, self.template_name, {'form': form})