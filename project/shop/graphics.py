from bs4 import BeautifulSoup
import requests
import re
import time

# Set this flag to True if you want to run the scraping
RUN_SCRAPE = False

# Regular expression pattern to match graphics card names
pattern = r'(AMD[\s\®\™]*Radeon[\s\®\™RX\dMSTVega]*\w*)|(Intel[\s\®\®\R]*[Iris\s\(\)R\®Xe\®UHD\s\(\)R]*[\s\wG\d\®]*)|(NVIDIA[\s\®]*[GeForce\s\®Quadro\s\®RTX\s\®MX\s\®]*[\w\d\s\-Max\-QTIADA]*)|(Qualcomm[\s\®]*Adreno[\s\®]*\d*)'

def scrapinfo():
    if not RUN_SCRAPE:
        print("Scraping is disabled. To enable scraping, set RUN_SCRAPE to True.")
        return

    base_url = "https://www.infotechsnepal.com/laptops-nepal/"
    page_number = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    while True:
        url = f"{base_url}page/{page_number}/"
        try:
            webpage = requests.get(url, headers=headers)
            print(webpage.content)


            webpage.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch page {page_number}. Error: {e}. Exiting...")
            break

        soup = BeautifulSoup(webpage.content, "html.parser")
        websites = soup.find_all("div", class_="product-items")

        if not websites:
            print(f"No more products found on page {page_number}. Exiting...")
            break

        for website in websites:
            link = website.a['href']

            # Navigate to the product page
            product_page = requests.get(link, headers=headers)
            product_soup = BeautifulSoup(product_page.content, "html.parser")

            # Find the div containing the graphics card information
            figure_div = product_soup.find("div", class_="woocommerce-Tabs-panel woocommerce-Tabs-panel--attrib_desc_tab panel entry-content wc-tab")

            if figure_div:
                figure = figure_div.find("figure", class_="wp-block-table")
                if figure:
                    table = figure.find("table")
                    if table:
                        rows = table.find_all("tr")
                        for row in rows:
                            if "Graphics" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    graphics = columns[1].get_text(strip=True)
                                    matches = re.findall(pattern, graphics)
                                    for match in matches:
                                        print(match)
        
        page_number += 1
        time.sleep(1)  # Sleep for a second to be polite to the server

if __name__ == '__main__':
    scrapinfo()
