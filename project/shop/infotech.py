from bs4 import BeautifulSoup
import requests
import csv
import re
import time
from .models import *

# Set this flag to True if you want to run the scraping
RUN_SCRAPE = False

def scrapinfo():
    if not RUN_SCRAPE:
        print("Scraping is disabled for Info. To enable scraping, set RUN_SCRAPE to True.")
        return

    # List of URLs for different product categories
    urls = [
        "https://www.infotechsnepal.com/laptops-nepal/",
    ]

    base_url = "https://www.infotechsnepal.com/laptops-nepal/"
    page_number = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    scraped_data = []

    while True:
        url = f"{base_url}page/{page_number}/"
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")

        websites = soup.find_all("div", class_="product-items")
        if not websites:  # Termination condition: If no products are found on the page, stop the loop
            break
        for website in websites:
            # Initialize default values for all variables
            brand = ""
            processor = ""
            graphics = ""
            storage = ""
            ram_details = ""
            display = ""
            touchscreen = ""
            color = ""
            warranty = ""
            port = ""
            operating_system = ""
            battery = ""

            link = website.a['href']
            title_element = website.find("h3")
            title = title_element.text.strip()
            print(title)

            model = title.split("|")[0].strip()
            image = website.find("img")
            image_url = image['src'] if image else ""

            price = website.find("span", class_="price")
            price_text = price.text.strip() if price else "N/A"

            # Specification from table
            product_page = requests.get(link, headers=headers)
            product_soup = BeautifulSoup(product_page.content, "html.parser")
            figure_div = product_soup.find("div", class_= "woocommerce-Tabs-panel woocommerce-Tabs-panel--attrib_desc_tab panel entry-content wc-tab")
            if figure_div:
                figure = figure_div.find("figure", class_="wp-block-table")
                if figure:
                    table = figure.find("table")
                    if table:
                        rows = table.find_all("tr")
                        brand = ""
                        processor = ""
                        graphics = ""
                        storage = ""
                        ram_details = ""
                        display = ""
                        touchscreen = ""
                        color = ""
                        warranty = ""
                        port = ""
                        operating_system=""
                        battery=""
                        
                        for row in rows:
                            if "Brand" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    brand = columns[1].get_text(strip = True)
                            
                            if "Processor" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    processor = columns[1].get_text(strip = True)
                                    
                            
                            if "Graphics" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    graphics = columns[1].get_text(strip = True)
                                
                            
                            if "Memory" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    ram_details = columns[1].get_text(strip = True)
                                
                            
                            if "Storage" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    storage = columns[1].get_text(strip = True)
                                
                            
                            if "Display" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    display = columns[1].get_text(strip = True)
                                
                            
                            if "Touchscreen" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    touchscreen = columns[1].get_text(strip = True)
                                
                            
                            if "Case Color" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    color = columns[1].get_text(strip = True)
                                                    

                            if "Base Warranty" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    warranty = columns[1].get_text(strip = True)
                                
                            
                            if "Standard Ports" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    port = columns[1].get_text(strip = True)
                                

                            if "Operating System" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    operating_system = columns[1].get_text(strip=True)

                            if "Battery" in row.text:
                                columns = row.find_all("td")
                                if len(columns) >= 2:
                                    battery = columns[1].get_text(strip=True)

                scraped_data.append({
                "category": url,
                "title": title,
                "image": image_url,
                "link": link,
                "price": price_text,
                "model": model,
                "ram": ram_details,
                "display": display,
                "storage": storage,
                "processor": processor,
                "touchscreen": touchscreen,
                "graphics": graphics,
                "color": color,
                "warrenty": warranty,
                "battery": battery,
                "operating_system": operating_system,
                "ports_and_connectivity": port,
                "brand": brand,
            })
        page_number += 1

        # A sleep between page requests to be polite to the website
        time.sleep(3)

    for data in scraped_data:
        existing_product = Product.objects.filter(category=data['category'], title=data['title']).first()
        if existing_product:
            if existing_product.price != data['price']:
                existing_product.price = data['price']
                existing_product.save()
                print(f"Updated price for {existing_product.title} to {existing_product.price}")
        else:
            new_product = Product(**data)
            new_product.save()
            print(f"Added new product: {new_product.title}")

scrapinfo() 
                    
                    
                        
                    
    