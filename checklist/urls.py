from django.urls import path
from .views import RegisterPage, PokemonList, PokemonUpdateView, DashboardView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('pokemon/', PokemonList.as_view(), name='pokemon_list'),
    path('pokemon/<int:pk>/update/', PokemonUpdateView.as_view(), name='pokemon_update'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # path('pokemon/', PokemonList.as_view(), name='pokedex'),
]