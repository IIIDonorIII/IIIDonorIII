import requests
from bs4 import BeautifulSoup



url = 'https://www.russianfood.com/recipes/bytype/?fid=12'
url2 = ''
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


#for food in soup.find_all('div', class_='foto'):
    #name = food.a.meta['content']