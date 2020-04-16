import requests
from bs4 import BeautifulSoup

url = 'https://jatim.suara.com/read/2020/04/09/063701/peta-sebaran-virus-corona-di-surabaya-9-april-2020-odp-dan-pdp-bertambah'
suaracovid = requests.get(url)

soup = BeautifulSoup(suaracovid.content, 'html.parser')

#print(soup)

results = soup.find_all('article', class_='content-article')

#print(results.prettify())
for i in results:
    print(i.text, end='\n'*2)