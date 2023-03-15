from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid

# Create your models here.
class Pokemon(models.Model): # Represents single Pokemon in checklist
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    image = models.ImageField(upload_to='pokemon_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.number}: {self.name}'

class UserPokemon(models.Model):
    # Represent User's collection of Pokemon
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.pokemon.name}'