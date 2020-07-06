import requests
from bs4 import BeautifulSoup

url = 'https://www.drift.com/careers/'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='jobs-container')

jobs = results.find_all('section', class_='card-content')

for job in jobs:
  title = job.find('h2', class_='title')
  company = job.find('div', class_='company')
  location = job.find('div', class_='location')
  if None in (title, company, location):
    continue
  print(title.text.strip())
  print(company.text.strip())
  print(location.text.strip())