from bs4 import BeautifulSoup
import requests

url = 'https://id.wikipedia.org/wiki/Daftar_kabupaten_dan_kota_di_Indonesia'
response = requests.get(url, timeout = 5)
content = BeautifulSoup(response.content, 'html.parser')

processed = content.findAll('span', attrs = {'class':'mw-headline'})

print(processed);
