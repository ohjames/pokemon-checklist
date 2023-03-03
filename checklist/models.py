from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    image = models.ImageField(upload_to='pokemon_images/')

    def __str__(self):
        return self.name