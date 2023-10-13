import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

url = 'https://www.russianfood.com/recipes/bytype/?fid=12'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for food in soup.find_all('div', class_='foto'):
    name = food.a.meta['content']
    cursor.execute('INSERT INTO recipes (name) VALUES (?)', (name,))

conn.commit()
conn.close()
