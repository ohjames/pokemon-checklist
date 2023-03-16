import requests
from django.core.files.base import ContentFile

import os
import sys
sys.path.append(os.path.abspath('../'))
from checklist.poke_scraper import PokeScraper

from checklist.models import Pokemon

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Scrape the Serebii Pokedex and save to database'

    def handle(self, *args, **options):
        scraper()

def scraper():
    df = PokeScraper('https://www.serebii.net/pokemon/gen1pokemon.shtml').create_gen_df()
    df.drop(columns=['Count', 'Abilities', 'HP', 'Att', 'Def', 'S.Att', 'S.Def', 'Spd'], inplace=True)
    new_pokemon = []
    for index, row in df.iterrows():
        number = row['No.']
        name = row['Name']
        image_url = row['Pic']
        p = Pokemon.objects.filter(number=number, name=name).first()
        if p:
            # updating existing pokemon with new image
            if not p.image:
                image_name = f'{number}.png'
                image_file = get_image_from_url(image_url)
                p.image.save(image_name, image_file)
                p.save()
        else:
            # Create new pokemon with new image
            image_name = f'{number}.png'
            image_file = get_image_from_url(image_url)
            p = Pokemon(number=number, name=name)
            p.image.save(image_name, image_file)
            p.save()
        new_pokemon.append(p)
    # Save new Pokemon objects to database
    Pokemon.objects.bulk_create(new_pokemon)

def get_image_from_url(url):
    response = requests.get(url)
    return ContentFile(response.content)
