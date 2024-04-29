# WEB-CRAWLING-CRAIGSLIST-JOB-SCRAPER-II

## About

This project is a web scraper built in Python using the Selenium library to extract job postings from Craigslist. The scraper fetches job listings posted today from various cities across the United States and filters out unwanted job titles based on user-defined criteria. It then saves the filtered job postings to a CSV file for further analysis or processing.

### Features

- Scrapes Craigslist job postings from multiple cities.
- Filters job titles based on user-defined criteria to remove unwanted postings.
- Saves the filtered job postings to a CSV file for easy access and analysis.

### How it Works

1. The web scraper fetches job postings from Craigslist using Selenium WebDriver.
2. Job titles are filtered based on a predefined list of undesirable keywords.
3. Filtered job postings are saved to a CSV file for further use.

### Usage

1. Ensure you have the necessary dependencies installed, including Python, Selenium, and the Chrome WebDriver.
2. Run the `scrape_craigslist.py` script to scrape job postings and save them to a CSV file.
3. Customize the list of undesirable keywords in the script to filter job titles according to your preferences.

Feel free to contribute, report issues, or suggest enhancements to this project!
