# Real Estate Scraper

## Overview
Real Estate Scraper is a web scraping project built using Scrapy. The purpose of this project is to scrape real estate data from a website, process it, and convert it into an XML format.

## Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/real-estate-scraper.git
```
### Installing dependencies
```bash
cd real-estate-scraper
!pip install -r requirements.txt
```
## To run the project
Set up the environment variables after creating .env file.
```bash
scrapy crawl homespider
```

## Project Structure
* homespider.py: Scrapes data from the website and sends it to pipelines.py for further processing.
* pipelines.py: Converts the scraped data into a desirable Python object structure and then converts the object to XML data.
* items.py: Contains the required Python classes for the project.
* .env: Contains a list of environment variables and their values.

