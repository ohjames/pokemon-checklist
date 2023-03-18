from django import forms
from .models import UserPokemon

class UserPokemonForm(forms.ModelForm):
    class Meta:
        model = UserPokemon
        fields = ['user', 'pokemon', 'completed']
        widgets = {'user': forms.HiddenInput(),
                   'pokemon': forms.HiddenInput(),
                   'completed': forms.CheckboxInput(attrs={'class': 'completed-checkbox'})}
