from django.shortcuts import render

from .models import Pokemon

# Create your views here.
def pokemon_list(request):
    if request.method == 'POST':
        user_pokemon = Pokemon.objects.filter(user=request.user)
        for pokemon in user_pokemon:
            pokemon.user = None
            pokemon.save()
        for pokemon_id in request.POST.getlist('pokemon[]'):
            try:
                pokemon = Pokemon.objects.get(id=int(pokemon_id))
                pokemon.user = request.user
                pokemon.save()
            except Pokemon.DoesNotExist:
                pass
    pokemon = Pokemon.objects.all()
    return render(request, 'checklist/pokemon_list.html', {'pokemon': pokemon})