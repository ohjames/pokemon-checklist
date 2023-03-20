from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

from .models import Pokemon, UserPokemon

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'checklist/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('checklist')
    
class CustomRegisterView(CreateView):
    template_name = 'checklist/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('create_user_pokemon')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

class PokedexView(TemplateView):
    template_name = 'checklist/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemon_list = Pokemon.objects.all()
        context['pokemon_list'] = pokemon_list
        return context

# Save for current user
class UserPokemonUpdateView(ListView):
    def get(self, request):
        user_pokemon_list = None
        if request.user.is_authenticated:
            user_pokemon_list = UserPokemon.objects.filter(user=request.user)
        else:
            user_pokemon_list = Pokemon.objects.all()
        return render(request, 'checklist/checklist.html', {'user_pokemon_list': user_pokemon_list})
    
    def post(self, request, *args, **kwargs):
        # Save user's progress
        user_pokemon_list = UserPokemon.objects.filter(user=self.request.user)
        for user_pokemon in user_pokemon_list:
            user_pokemon.completed = request.POST.get(str(user_pokemon.id), False)
            user_pokemon.save()
        # Redirect to checklist page
        return redirect('checklist')

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

        # Redirect to checklist page
        return redirect('checklist')