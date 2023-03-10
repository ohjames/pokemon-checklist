from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pokemon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    image = models.ImageField(upload_to='pokemon_images')

    def __str__(self):
        return self.name