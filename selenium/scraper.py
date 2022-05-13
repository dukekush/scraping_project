from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np


# A variable defined in order to limit number of pages to a hundred
limit_pages = True

gecko_path = r"C:\Users\jakub\Desktop\geckodriver.exe"
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(executable_path=gecko_path, options=options)
url = "https://www.otomoto.pl/"
driver.get(url)

# We have to handle the problem of a window that pops out with information about a privacy policy of the website
time.sleep(5)
try:
	button_privacy = driver.find_element(By.ID, "onetrust-accept-btn-handler")
	button_privacy.click()

except:
	pass

# We have to provide arguments for the process of filtartion of car offers
# First, we need to chose car body type
# We may of course provide different type that "Kabriolet" (which is used as an example)
time.sleep(5)
drop_dawn_menu = driver.find_element(By.XPATH, "//input[@id='filter_enum_body_type']")
drop_dawn_menu.click()
drop_dawn_menu.send_keys("Kabriolet")

time.sleep(5)
drop_dawn_menu.send_keys(Keys.ENTER)
time.sleep(5)

# We click the button that should take us to the website with offers
button_submit = driver.find_element(By.XPATH, "//button[@class='ds-button ds-width-full']")
button_submit.click()
time.sleep(5)

# Preparing variables for links to offers
links_list = []

# A loop that is responsible for collecting links to offers from otomoto.pl
while True:
	time.sleep(3)

	try:
		links = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'https://www.otomoto.pl/oferta/')]")
		links_list += [element.get_attribute("href") for element in links] # Collecting links
	except:
		pass

	try:
		button_next_page = driver.find_element(By.XPATH, "//li[@title='Next Page']")
		driver.execute_script("arguments[0].click();", button_next_page) # Clicking button to move to a next page of otomoto.pl
	except:
		pass

	if limit_pages == True and len(links_list) > 100: # The condition to stop the infinite loop
		break

# To remove duplicates and reduce number of pages to scrape:
links_list = list(dict.fromkeys(links_list))
if limit_pages == True:
	links_list = links_list[:100]

# Preparing lists to store data that are going to be collected
color_list = [] # Color of a car
driven_list = [] # Number of km driven to date
make_list = [] # Name of the maker
model_list = [] # Name of a car model
power_list = [] # Engine's power
price_list = [] # Price
year_list = [] # Year of production
fuel_list = [] # Type of fuel
capacity_list = [] # Engine's cappacity
transmission_list = [] # Transmission type
drive_list = [] # Drive type

# A loop that is going to iterate over collected links to car offers and find their parameters, i.e. price, power, model, etc.
for link in links_list:
	# Opening a link
	try:
		driver.get(link)
	except:
		pass

	# Finding offers details:
	try:
		make = driver.find_element(By.XPATH, "//span[text()='Marka pojazdu']/following-sibling::div/a")
		make_list.append(make.text)
	except:
		make_list.append(np.nan)
		pass

	try:
		colour = driver.find_element(By.XPATH, "//span[text()='Kolor']/following-sibling::div/a")
		color_list.append(colour.text)
	except:
		color_list.append(np.nan)
		pass

	try:
		driven = driver.find_element(By.XPATH, "//span[text()='Przebieg']/following-sibling::div")
		driven_list.append(int(driven.text[:-3].replace(" ", "")))
	except:
		driven_list.append(np.nan)
		pass
	
	try:
		modell = driver.find_element(By.XPATH, "//span[text()='Model pojazdu']/following-sibling::div/a")
		model_list.append(modell.text)
	except:
		model_list.append(np.nan)
		pass

	try:
		power = driver.find_element(By.XPATH, "//span[text()='Moc']/following-sibling::div")
		power_list.append(power.text[:-3])
	except:
		power_list.append(np.nan)
		pass

	try:
		price = driver.find_element(By.CLASS_NAME, "offer-price")
		price_list.append(float(price.get_attribute("data-price").replace(" ", "")))
	except:
		price_list.append(np.nan)
		pass

	try:
		year = driver.find_element(By.XPATH, "//span[text()='Rok produkcji']/following-sibling::div")
		year_list.append(year.text)
	except:
		year_list.append(np.nan)
		pass
	
	try:
		fuel = driver.find_element(By.XPATH, "//span[text()='Rodzaj paliwa']/following-sibling::div/a")
		fuel_list.append(fuel.text)
	except:
		fuel_list.append(np.nan)
		pass

	try:
		capacity = driver.find_element(By.XPATH, "//span[text()='Pojemność skokowa']/following-sibling::div")
		capacity_list.append(int(capacity.text[:-4].replace(" ", "")))
	except:
		capacity_list.append(np.nan)
		pass

	try:
		transmission = driver.find_element(By.XPATH, "//span[text()='Skrzynia biegów']/following-sibling::div/a")
		transmission_list.append(transmission.text)
	except:
		transmission_list.append(np.nan)
		pass

	try:
		drive = driver.find_element(By.XPATH, "//span[text()='Napęd']/following-sibling::div/a")
		drive_list.append(drive.text)
	except:
		drive_list.append(np.nan)
		pass

	# A control print which aim is to present details of already scraped offer
	print(make_list[-1], model_list[-1], price_list[-1], power_list[-1], driven_list[-1], color_list[-1], year_list[-1],
	fuel_list[-1], capacity_list[-1], transmission_list[-1], drive_list[-1])

# Creating a data frame that contains all the collected data
data = pd.DataFrame({"Make": make_list, "Model": model_list, "Price [PLN]": price_list, "Power [hp]": power_list,
					"Driven distance [km]": driven_list, "Color": color_list, "Year of production": year_list, "Fuel": fuel_list,
					"Engine capacity [cm^3]": capacity_list, "Transmission type": transmission_list, "Drive type": drive_list})

print(data)