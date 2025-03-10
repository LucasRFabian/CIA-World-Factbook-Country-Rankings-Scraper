from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup
from random import randint
import requests
import csv
import time

def links_get():
    #Page Initialization
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.cia.gov/the-world-factbook/countries/');

    #Selenium Tomfoolery
    select = Select(driver.find_element(By.CLASS_NAME, "per-page"))
    s = randint(1, 5)
    time.sleep(s)
    select.select_by_visible_text('All')

    #Soup Initialization
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    #Get Links
    link_list = []
    country_list = soup.find_all('a', class_='inline-link')
    for country in country_list:
        link_list.append(country.attrs['href'])

    #Remove Duplicates
    link_list = list(set(link_list))
    link_list.sort()

    driver.quit()
    return link_list

def ranking_get(url):
    #Page Initialization
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}
    page = requests.get(url, headers=hdr)
    soup = BeautifulSoup(page.text, 'html.parser')

    #List Initialization
    stat_hrefs = ['/the-world-factbook/field/area/country-comparison/', '/the-world-factbook/field/population/country-comparison/', '/the-world-factbook/field/median-age/country-comparison/', '/the-world-factbook/field/infant-mortality-rate/country-comparison/', '/the-world-factbook/field/real-gdp-per-capita/country-comparison/', '/the-world-factbook/field/unemployment-rate/country-comparison/', '/the-world-factbook/field/military-expenditures/country-comparison/']
    ranking_list = []

    #Get Country Name
    country_name = soup.find('h1').text
    ranking_list.append(country_name)

    #Get Rankings
    for link in stat_hrefs:
        try:
            stat = soup.find('a', href=link).text
            if ' ' in stat:
                stat = stat[stat.rfind(' '):].strip(' ')
            stat = int(stat)
            ranking_list.append(stat)
        except:
            ranking_list.append('-')
    
    return ranking_list

#Get URLs
link_list = links_get()

#Initialize CSV
csvfile = open('countryrankings.csv', 'w', newline='', encoding='utf-8')
c = csv.writer(csvfile)
c.writerow(['country','area','population', 'median_age', 'infant_mortality_rate', 'gdp_per_capita', 'unemployment_rate', 'military_expenditures'])

#Get/Write Country Rankings
for link in link_list:
    country_url = 'https://www.cia.gov' + link
    c.writerow(ranking_get(country_url))
csvfile.close()