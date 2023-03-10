from django.urls import path
from .views import RegisterPage, PokemonList, DashboardView, CustomLoginView, scraper
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('', DashboardView.as_view(), name='dashboard'),
    path('pokemon/', PokemonList.as_view(), name='pokemon_list'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='dashboard'), name='logout'),
    path('scrape/', scraper, name='scraper'),
]