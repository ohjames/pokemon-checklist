from django.shortcuts import render

from .models import Pokemon

# Create your views here.
def pokemon_list(request):
    pokemon = Pokemon.objects.all()
    return render(request, 'checklist/pokemon_list.html', {'pokemon': pokemon})