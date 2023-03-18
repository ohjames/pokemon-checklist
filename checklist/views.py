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

from .models import Pokemon, UserPokemon
from .forms import UserPokemonForm

from django.http import HttpResponse

# Create your views here.

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

# Save for current user
class UserPokemonUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_pokemon_list = UserPokemon.objects.filter(user=request.user)
        return render(request, 'checklist/checklist.html', {'user_pokemon_list': user_pokemon_list})
    # model = UserPokemon
    # form_class = UserPokemonForm
    # template_name = 'checklist/checklist.html'
    # success_url = reverse_lazy('checklist')
    
    # def get_queryset(self):
    #     return UserPokemon.objects.filter(user=self.request.user)
    
    # def post(self, request, *args, **kwargs):
    #     # Save user's progress
    #     user_pokemons = UserPokemon.objects.filter(user=request.user)
    #     for user_pokemon in user_pokemons:
    #         user_pokemon.completed = request.POST.get(str(user_pokemon.id), False)
    #         user_pokemon.save()
    #     return super().post(request, *args, **kwargs)

# Save for new users
class UserPokemonCreateView(LoginRequiredMixin, View):
    def get(self, request):
        # Get all pokemon
        pokemon_list = Pokemon.objects.all()

        # Create UserPokemon objects for each Pokemon
        user = request.user
        for pokemon in pokemon_list:
            user_pokemon = UserPokemon(user=user, pokemon=pokemon, completed=False)
            user_pokemon.save()

        # Redirect to home page
        return redirect('checklist')

    # model = UserPokemon
    # form_class = UserPokemonForm
    # template_name = 'checklist/checklist.html'
    # success_url = reverse_lazy('checklist')

    # def form_valid(self, form):
    #     pokemon_ids = self.request.POST.getlist('pokemon')
    #     pokemon_ids = [int(pokemon_id) for pokemon_id in pokemon_ids]
    #     user = self.request.user
    #     print('Selected Pokemon IDs:', pokemon_ids)
    #     for pokemon_id in pokemon_ids:
    #         try:
    #             pokemon = Pokemon.objects.get(pk=pokemon_id)
    #             user_pokemon = UserPokemon(user=user, pokemon=pokemon, completed=False)
    #             user_pokemon.save()
    #             print('Created UserPokemon:', user_pokemon)
    #         except Pokemon.DoesNotExist:
    #             print('Pokemon with ID', pokemon_id, 'does not exist')
    #     return super().form_valid(form)

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