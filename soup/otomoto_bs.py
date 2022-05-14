from urllib import request
from bs4 import BeautifulSoup as BS
import pandas as pd
import numpy as np
import random

limit = True

url = "https://www.otomoto.pl/osobowe/seg-cabrio"
html = request.urlopen(url)
bs = BS(html.read(), "html.parser")

# Get number of pages with offers
n_pages = bs.find_all("li", {"data-testid": "pagination-list-item"})[-1].span.text
n_pages = int(n_pages)

#Create set with offer links (set because we want to get unique offers links)
offers_links = set()
for i in range(n_pages):
    # Open page with offers
    url = f"https://www.otomoto.pl/osobowe/seg-cabrio?page={i+1}"
    html = request.urlopen(url)
    bs = BS(html.read(), "html.parser")

    # Extract links to offers
    offers = bs.find_all("article", {"data-variant": "regular"})
    offers = [offer.a["href"] for offer in offers]
    offers_links.update(offers)

    # If limit mode and offers_links greater than 100, stop searching for next links
    if limit and (len(offers_links) > 100):
        offers_links = random.sample(offers_links, 100)
        break

# Prepare list for offers details
color_list = []  # Color of a car
driven_list = []  # Number of km driven to date
make_list = []  # Name of the maker
model_list = []  # Name of a car model
power_list = []  # Engine's power
price_list = []  # Price
year_list = []  # Year of production
fuel_list = []  # Type of fuel
capacity_list = []  # Engine's cappacity
transmission_list = []  # Transmission type
drive_list = []  # Drive type

for link in offers_links:
    html = request.urlopen(link)
    bs = BS(html.read(), "html.parser")

    # Finding offers details:
    try:
        color = (
            bs.find("span", string="Kolor")
            .find_next_sibling("div")
            .a.get_text(strip=True, separator=" ")
        )
        color_list.append(color)
    except:
        color_list.append(np.nan)

    try:
        driven = (
            bs.find("span", string="Przebieg")
            .find_next_sibling("div")
            .get_text(strip=True, separator=" ")[:-3]
            .replace(" ", "")
        )
        driven_list.append(driven)
    except:
        driven_list.append(np.nan)

    try:
        make = (
            bs.find("span", string="Marka pojazdu")
            .find_next_sibling("div")
            .a.get_text(strip=True, separator=" ")
        )
        make_list.append(make)
    except:
        make_list.append(np.nan)

    try:
        model = (
            bs.find("span", string="Model pojazdu")
            .find_next_sibling("div")
            .a.get_text(strip=True, separator=" ")
        )
        model_list.append(model)
    except:
        model_list.append(np.nan)

    try:
        power = (
            bs.find("span", string="Moc")
            .find_next_sibling("div")
            .get_text(strip=True, separator=" ")
            .replace(" ", "")
        )
        power_list.append(power)
    except:
        power_list.append(np.nan)

    try:
        price = bs.find("div", {"class": "offer-price"})["data-price"].replace(" ", "")
        price_list.append(price)
    except:
        price_list.append(np.nan)

    try:
        year = (
            bs.find("span", string="Rok produkcji")
            .find_next_sibling("div")
            .get_text(strip=True, separator=" ")
        )
        year_list.append(year)
    except:
        year_list.append(np.nan)

    try:
        fuel = (
            bs.find("span", string="Rodzaj paliwa")
            .find_next_sibling("div")
            .a.get_text(strip=True, separator=" ")
        )
        fuel_list.append(fuel)
    except:
        fuel_list.append(np.nan)

    try:
        capacity = (
            bs.find("span", string="Pojemność skokowa")
            .find_next_sibling("div")
            .get_text(strip=True, separator=" ")
            .replace(" ", "")
        )
        capacity_list.append(capacity)
    except:
        capacity_list.append(np.nan)

    try:
        transmission = (
            bs.find("span", string="Skrzynia biegów")
            .find_next_sibling("div")
            .a.get_text(strip=True, separator=" ")
        )
        transmission_list.append(transmission)
    except:
        transmission_list.append(np.nan)

    try:
        drive = (
            bs.find("span", string="Napęd")
            .find_next_sibling("div")
            .a.get_text(strip=True, separator=" ")
        )
        drive_list.append(drive)
    except:
        drive_list.append(np.nan)

# Creating a data frame that contains all the collected data
data = pd.DataFrame(
    {
        "Make": make_list,
        "Model": model_list,
        "Price [PLN]": price_list,
        "Power [hp]": power_list,
        "Driven distance [km]": driven_list,
        "Color": color_list,
        "Year of production": year_list,
        "Fuel": fuel_list,
        "Engine capacity [cm^3]": capacity_list,
        "Transmission type": transmission_list,
        "Drive type": drive_list,
    }
)

# Save data to csv
data.to_csv("dane_otomoto.csv")
