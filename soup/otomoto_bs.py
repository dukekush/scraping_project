from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd

limit = True

url = 'https://www.otomoto.pl/osobowe/seg-cabrio' 
html = request.urlopen(url)
bs = BS(html.read(), 'html.parser')

n_pages = bs.find_all('li', {"data-testid":"pagination-list-item"})[-1].span.text
print(n_pages)