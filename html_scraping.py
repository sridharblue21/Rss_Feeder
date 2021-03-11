from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup

URL = 'https://www.financialreporter.co.uk/regulation/fca-admits-fscs-levy-is-unsustainable-and-acknowledges-previous-mistakes.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find('article', class_='wrap-column-1')
paras= results.find_all('p')
for para in paras:
    print(para.get_text())
