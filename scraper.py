# url = 'https://www.serebii.net/pokemon/gen1pokemon.shtml'

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

import os
import django
from django.core.files.base import ContentFile


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokedex.settings')
django.setup()

from checklist.models import Pokemon

class PokeScraper():
    def __init__(self, url):
        self.url = url

    def get_gen_header_info(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'dextable'})
        headers = []
        for i in table.find_all('tr')[:2]:
            for j in i:
                headers.append(j.text)
        headers = [i.removeprefix('\r\n\t\t') for i in headers]
        headers = [i.removesuffix('\r\n\t\t') for i in headers]
        headers = [i.removesuffix('\t') for i in headers]
        headers = [i.replace('\n', '') for i in headers]
        headers = [i for i in headers if i]
        headers.pop(3)
        headers.pop(4)
        headers.pop(1)
        return headers

    def get_gen_content_info(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'dextable'})
        content = []
        for i in table.find_all('tr')[2:]:
            for j in i:
                content.append(j.text)
        content = [i.removeprefix('\r\n\t\t') for i in content]
        content = [i.removesuffix('\r\n\t\t') for i in content]
        content = [i.replace('\n', '').replace(' ', '').replace('#', '') for i in content]
        content = [i for i in content if i]
        return content

    def get_img_src(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'dextable'})
        src = [i for i in table.find_all('img')]
        images = [("=IMAGE(\"" + "https://www.serebii.net"+element['src']+ "\")") for element in src if '.gif' not in element['src']]
        return images

    def create_gen_df(self):
        poke_df = pd.DataFrame(self.get_gen_content_info())
        poke_df = pd.DataFrame(poke_df[0].values.reshape(-1,9), columns=self.get_gen_header_info())
        poke_df.insert(2, "Pic", self.get_img_src())
        poke_df.insert(loc = 0,column = 'Count',value = '')
        return poke_df

    def get_region_header_info(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'tab'})
        headers = []
        for i in table.find_all('tr')[:2]:
            for j in i:
                headers.append(j.text)
        headers = [i.removeprefix('\r\n\t\t') for i in headers]
        headers = [i.removesuffix('\r\n\t\t') for i in headers]
        headers = [i.removesuffix('\t') for i in headers]
        headers = [i.replace('\n', '') for i in headers]
        headers = [i for i in headers if i]
        headers.pop(1)
        headers.pop(3)
        headers.pop(3)
        return headers

    def get_region_content_info(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'tab'})
        content = []
        for i in table.find_all('tr')[2:]:
            for j in i:
                content.append(j.text)
        content = [i.removeprefix('\r\n\t\t') for i in content]
        content = [i.removesuffix('\r\n\t\t') for i in content]
        content = [i.replace('\n', '').replace(' ', '').replace('#', '') for i in content]
        content = [i for i in content if i]

        # Removes all the Japanese characters
        loweralphabets="abcdefghijklmnopqrstuvwxyz"
        upperalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers="0123456789"
        desired_strings = loweralphabets + upperalphabets + numbers
        contents = []
        for i in content:
            a = ""
            for j in i:
                if j in desired_strings:
                    a += j
            contents.append(a)
        contents = [i for i in contents if i]
        return contents
    
    def get_region_img_src(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table', {'class': 'tab'})
        src = [i for i in table.find_all('img')]
        images = [("=IMAGE(\"" + "https://www.serebii.net"+element['src']+ "\")") for element in src if '.gif' not in element['src']]
        return images

    def create_region_df(self):
        region_df = pd.DataFrame(self.get_region_content_info())
        region_df = pd.DataFrame(region_df[0].values.reshape(-1, 9), columns=self.get_region_header_info())
        region_df.insert(2, "Pic", self.get_region_img_src())
        region_df.insert(loc = 0,column = 'Count',value = '')
        return region_df

df = PokeScraper('https://www.serebii.net/pokemon/gen1pokemon.shtml').create_gen_df()
df.drop(columns=['Count', 'Abilities', 'HP', 'Att', 'Def', 'S.Att', 'S.Def', 'Spd'], inplace=True)

for index, row in df.iterrows():
    number = row['No.']
    name = row['Name']
    image_url = row['Pic']
    response = requests.get(image_url)
    image_file = ContentFile(response.content)
    image_name = f'{number}.png'
    # print(number, name)
    pokemon = Pokemon(number=number, name=name)
    pokemon.image.save(image_name, image_file)
    pokemon.save()