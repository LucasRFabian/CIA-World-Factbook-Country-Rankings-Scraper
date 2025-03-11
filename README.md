# CIA World Factbook Country Rankings Scraper
This script uses Selenium and Beautiful Soup to scrape the [CIA World Factbook](https://www.cia.gov/the-world-factbook/) for certain ranking information. Specifically, this script collects seven unique ranking metrics:
1. Area
2. Population
3. Median Age
4. Infant Mortality Rate
5. GDP per Capita
6. Unemployment Rate
7. Military Expenditures

The goal is to create a database that allows users to easily compare/contrast different countries' performance in these areas to make isolating factors for success easier.

## How it Works
In order to get the links to able to scrape ranking data from every country, Selenium is used to open a chrome tab for the CIA World Factbook [Countries Page](https://www.cia.gov/the-world-factbook/countries/) and selects the "All" button in the dropdown so that all the partial links can be scraped by Beautiful Soup. This is all handled by the links_get() function.

Since every country's page is structured similarly, a simple for loop runs the ranking_get() function for every country's link, which scrapes all the relevant data using Beautiful Soup. The data is then written to a csv file.

## Changes and Issues
There are a few countries on the CIA World Factbook [Countries Page](https://www.cia.gov/the-world-factbook/countries/) that just redirect to the page for the [United States Pacific Island Wildlife Refuges](https://www.cia.gov/the-world-factbook/countries/united-states-pacific-island-wildlife-refuges/). This is typically because these countries are islands within the USPIWR. In the code, this is addressed by removing duplicate links, which results in there being 254 countries listed on the datasheet, as opposed to the website's claimed 261.
