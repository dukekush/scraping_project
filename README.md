# Web Scraping and Social Media Scraping Project

## This is an instruction how to run scrapers!

### 1. Selenium Instruction
In command line run:
```
python selenium/scraper.py
```

### 2. Scrapy Instruction
1. In command line go to project directory:
```
cd scrapy/otomoto_spider
```
2. Run spider to get links to pages, if error occurs, try few more times, and check if links.csv is not empty.
```
scrapy crawl links -O 'data/links.csv'
```
3. Run crawler to get cars data. You can change <strong>LIMIT_ITEMS</strong> to False, in spider_final.py (line 8) to scrape all available data.
```
scrapy crawl cars -O 'data/cars.csv'
```

### 3. BeautifoulSoup Instruction
In command line run:
```
python soup/otomoto_bs.py
```
