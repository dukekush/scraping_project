from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd

limit = True

url = 'https://www.otomoto.pl/osobowe/seg-cabrio' 
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

n_pages = bs.find_all('li', {"data-testid":"pagination-list-item"})[-1].span.text
n_pages = int(n_pages)
print(n_pages)

offers_links = []
for i in range(n_pages):
    print(i+1)
    url = f'https://www.otomoto.pl/osobowe/seg-cabrio?page={i+1}'
    print(url)

    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser') 
    pages = bs.find_all('article', {"data-variant":"regular"})

    pages = [page.a["href"] for page in pages]
    offers_links.append(pages)
    print(len(offers_links))
    if limit and (len(offers_links) > 100):
        break

print(offers_links)
print(len(offers_links))