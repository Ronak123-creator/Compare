from bs4 import BeautifulSoup
import requests
import csv
import re
import time

# Set this flag to True if you want to run the scraping
RUN_SCRAPE = False

def scrapinfo():
    if not RUN_SCRAPE:
        print("Scraping is disabled. To enable scraping, set RUN_SCRAPE to True.")
        return

    # List of URLs for different product categories
    base_url = "https://www.infotechsnepal.com/laptops-nepal/"
    page_number = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    while True:
        url = f"{base_url}page/{page_number}/"  # Construct the URL for each page
        webpage = requests.get(url, headers=headers)
        if webpage.status_code != 200:
            print(f"Failed to fetch page {page_number}. Exiting...")
            break

        soup = BeautifulSoup(webpage.content, "html.parser")
        websites = soup.find_all("div", class_="product-items")

        if not websites:
            print(f"No more products found on page {page_number}. Exiting...")
            break

        for website in websites:
            link = website.a['href']
            title_element = website.find("h3")
            title = title_element.text.strip()

            product_page = requests.get(link, headers=headers)
            product_soup = BeautifulSoup(product_page.content, "html.parser")
            figure_div = product_soup.find("div", class_="woocommerce-Tabs-panel woocommerce-Tabs-panel--attrib_desc_tab panel entry-content wc-tab")

            processor = ""  # Initialize processor variable

            if figure_div:
                table = figure_div.find("table")
                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        if "Processor" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                processor = columns[1].get_text(strip=True)
                                break 

            combined_info = title + " " + processor
                
                # Search for patterns using regular expressions
            intel_core_match = re.search(r'(i[3579])\s*-?\s*(\d{4,5}[A-Za-z]*)', combined_info)
            intel_celeron_match = re.search(r'Celeron', combined_info)
            amd_match = re.search(r'Ryzen (\d+)\s*-?\s*(\d{4}[A-Za-z]*)?', combined_info)
            
            if intel_core_match:
                generation = intel_core_match.group(1)
                model = intel_core_match.group(2)
                print(f"{generation}-{model}")
            elif intel_celeron_match:
                print("Celeron")
            elif amd_match:
                generation = amd_match.group(1)
                model = amd_match.group(2)
                if model:
                    print(f"Ryzen {generation} {model}")
                else:
                    print(f"Ryzen {generation}")
            else:
                print("Processor information not found")
            
            print("\n")

        page_number += 1
        time.sleep(1)


scrapinfo()
