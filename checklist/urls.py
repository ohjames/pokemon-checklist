from django.urls import path
# from .views import RegisterPage, PokemonList, DashboardView, CustomLoginView, PokemonDetailView, ToggleCompletionView
from .views import CustomLoginView, CustomRegisterView, PokedexView# UserPokemonUpdateView, UserPokemonCreateView, ToggleCaughtView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('register/', RegisterPage.as_view(), name='register'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('', PokemonList.as_view(), name='pokemon_list'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('logout/', LogoutView.as_view(next_page='dashboard'), name='logout'),
    # path('<int:pokemon_id>/', PokemonDetailView.as_view(), name='pokemon_detail'),
    # path('<int:pokemon_id>/toggle_completion/', ToggleCompletionView.as_view(), name='toggle_completion'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', PokedexView.as_view(), name='home'),
    # path('checklist/toggle/<int:pk>/', ToggleCaughtView.as_view(), name='toggle_caught'),
    # path('checklist/', UserPokemonUpdateView.as_view(), name='checklist'),
    # path('checklist/create/', UserPokemonCreateView.as_view(), name='create_user_pokemon'),
    # path('checklist/update/<int:pk>/', UserPokemonUpdateView.as_view(), name='update_user_pokemon'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]