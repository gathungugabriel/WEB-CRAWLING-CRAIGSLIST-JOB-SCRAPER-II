import re
import csv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nltk.stem import WordNetLemmatizer

def scrape_craigslist_geo(driver_path):
    cities_dict = {}
    url = 'https://geo.craigslist.org/iso/us'
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.binary_location = driver_path  # Set Chrome binary location
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        select_tag = driver.find_element('css selector', '.geo-site-list')
        if select_tag:
            li_tags = select_tag.find_elements('tag name', 'li')
            for li_tag in li_tags:
                a_tag = li_tag.find_element('tag name', 'a')
                city = a_tag.text
                href = a_tag.get_attribute('href')
                cities_dict[city] = href
        driver.quit()
    except WebDriverException as e:
        print(f"An error occurred while fetching {url}: {e}")
    return cities_dict

def fetch_todays_job_urls(cities_dict):
    todays_job_urls = []
    for city, href in cities_dict.items():
        city_url = href + 'search/ggg?postedToday=1#search=1~thumb~0~0'
        todays_job_urls.append(city_url)
    return todays_job_urls

def scrape_job_details(todays_job_urls):
    job_dict = {}
    driver = webdriver.Chrome()
    for url in todays_job_urls:
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol > li[data-pid]")))
            job_list_items = driver.find_elements(By.CSS_SELECTOR, "ol > li[data-pid]")
            for job_item in job_list_items:
                try:
                    data_pid = job_item.get_attribute("data-pid")
                    title_element = job_item.find_element(By.CSS_SELECTOR, ".posting-title > span.label")
                    title = title_element.text if title_element else "Title not found"
                    href_element = job_item.find_element(By.CSS_SELECTOR, ".cl-app-anchor")
                    href = href_element.get_attribute("href") if href_element else "Href not found"
                    job_dict[data_pid] = {"title": title, "href": href}
                except Exception as e:
                    print(f"Error extracting job details: {e}")
        except Exception as e:
            print(f"Error loading job listings for URL {url}: {e}")
    driver.quit()
    return job_dict

def filter_job_dict(job_dict):
    words_to_eradicate = ['till', 'garden', 'repair', 'delivery', 'housekeeping', 'movers', 'cashiers',
                          'door', 'model', 'shopper', 'videographer', 'photographer', 'mechanic',
                          'carpenter', 'cleaner', 'salgate']
    wordnet_lemmatizer = WordNetLemmatizer()
    words_to_eradicate = [wordnet_lemmatizer.lemmatize(word) for word in words_to_eradicate]
    pattern = re.compile(r'\b(?:' + '|'.join(words_to_eradicate) + r')\b', flags=re.IGNORECASE)
    filtered_job_dict = {}
    for data_pid, job_details in job_dict.items():
        if not re.search(pattern, job_details['title']):
            filtered_job_dict[data_pid] = job_details
    return filtered_job_dict

def save_to_csv(job_dict, csv_filename):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Data PID', 'Job Title', 'Href Link']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data_pid, job_details in job_dict.items():
            writer.writerow({'Data PID': data_pid, 'Job Title': job_details['title'], 'Href Link': job_details['href']})
    print(f"Job postings saved to {csv_filename}")

if __name__ == "__main__":
    # Specify the Chrome WebDriver path
    driver_path = r'C:\Users\Gabriel\Desktop\apps\chrome-win64\chrome-win64\chrome.exe'
    
    # Scrape cities listed under "choose the site nearest you"
    cities_dict = scrape_craigslist_geo(driver_path)
    
    # Fetch today's job URLs for each city
    todays_job_urls = fetch_todays_job_urls(cities_dict)
    
    # Scrape job details from each URL
    job_dict = scrape_job_details(todays_job_urls)
    
    # Filter job dictionary based on specified words
    filtered_job_dict = filter_job_dict(job_dict)
    
    # Define the filename for the CSV file
    csv_filename = r"C:\Users\Gabriel\Desktop\Coding\WEB-CRAWLING-CRAIGSLIST-JOB-SCRAPER\job_postings.csv"
    
    # Save filtered job postings to CSV
    save_to_csv(filtered_job_dict, csv_filename)
