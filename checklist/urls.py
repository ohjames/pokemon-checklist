from django.urls import path
# from .views import RegisterPage, PokemonList, DashboardView, CustomLoginView, PokemonDetailView, ToggleCompletionView
from .views import CustomLoginView, CustomRegisterView, HomeView, PokemonChecklistView, UserPokemonCreateView, AboutView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('checklist/', PokemonChecklistView.as_view(), name='checklist'),
    path('about/', AboutView.as_view(), name='about'),
    path('checklist/create/', UserPokemonCreateView.as_view(), name='create_user_pokemon'),
    
]