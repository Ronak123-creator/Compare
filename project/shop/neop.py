# here description is added 

from bs4 import BeautifulSoup
import requests
import time
import re
from .models import *

def extract_price(price_range):
    if price_range is None or not isinstance(price_range, str):
        raise ValueError("Invalid input: Not a string or None value")
        
    price_range = price_range.replace(",", "").strip()
    numbers = re.findall(r"\d+\.\d+|\d+", price_range)
    
    if not numbers:
        raise ValueError("Invalid input: No numbers found")
        
    prices = [float(num) for num in numbers]  # Using float to handle decimal points
    
    if len(prices) > 1:
        return min(prices)
    else:
        return prices[0]
    
def clean_title(input_text):
    cleaned_text = re.sub(r'\b5G\b|\d+/\d+GB|\d+GB\b|4G Lte|[|()+]|Inc', '', input_text)
    return cleaned_text

RUN_SCRAPE = False

def scrapNeoPhone():
    if not RUN_SCRAPE:
        print("Scraping is disabled for Neophone. To enable scraping, set RUN_SCRAPE to True.")
        return

    urls = [
        "https://neostore.com.np/product-category/mobile-brands",
    
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    scraped_data = []
    increment_step = 48
    max_pages = 2
    for url in urls:
            for i in range(max_pages):
                page_num = i * increment_step
                current_url = f"{url}/{page_num}" if page_num != 0 else url    
                webpage = requests.get(current_url, headers=headers)
                soup = BeautifulSoup(webpage.content, "html.parser")

                # Find all <h3> elements with the class 'product-title'
                websites = soup.find_all("div", class_="product-item-box")

                for website in websites:
                    
                    link = website.a['href']  # Extract the 'href' attribute from the <a> tag within the <h3> element
                    title_word = website.find("h3").text.strip()
                    title = clean_title(title_word)
                    print (title)
                    image = website.find_next("img")
                    if image:
                        image_url = image['src']
                    else:
                        image_url = ""
                    price = website.find_next("span", class_="price")  # Find the next <span> element with the specified class
                    if price:
                        price_text = price.text
                    else:
                        price_text = "N/A"
                    pprice = extract_price(price_text)

                    product_page = requests.get(link, headers=headers)
                    product_soup = BeautifulSoup(product_page.content, "html.parser")
                                                  
                    description = product_soup.find("div", class_="woocommerce-product-details__short-description")
                    if description:
                        description_text = description.get_text(strip=True)
                    else:
                        description_text = "N/A"           
            
                    # from table
                    model = ""
                    category = ""
                    brand = ""
                    display_size = ""
                    battery = ""
                    ram = ""
                    internal_storage = ""
                    primary_camera = ""
                    secondary_camera = ""
                    chipset = ""
                    operating_system = ""
                    sim_type = ""
                    warranty = ""
                    insurance = ""
                    table = product_soup.find("table")                
                    
                    if table:
                        rows = table.find_all("tr")
                        for row in rows:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                key = columns[0].get_text(strip = True)
                                value = columns[1].get_text(strip =True)
                                
                            if key == "Product":
                                model = value
                            if key == "Category":
                                category = value
                            if key == "Brand":
                                brand = value
                            if key == "Display Size":
                                display_size = value
                            if key == "Battery Power":
                                battery = value
                            if key == "Ram":
                                ram = value
                            if key == "Internal Storage":
                                internal_storage = value
                            if key == "Primary Camera":
                                primary_camera = value
                            if key == "Secondary Camera":
                                secondary_camera = value
                            if key == "Chipset":
                                chipset = value
                            if key == "Operating System":
                                operating_system = value
                            if key == "Sim Type":
                                sim_type = value
                            if key == "Warranty":
                                warranty = value
                            if key == "Insurance":
                                insurance = value


                    scraped_data.append({
                    "category": category,
                    "title": title,
                    "images": image_url,
                    "link": link,
                    "price_range": price_text,
                    "pprice":pprice,
                    "description": description_text,
                    "model": model,
                    "ram": ram,
                    "display_size": display_size,
                    "storage": internal_storage,
                    "chipset":chipset,
                    "warranty":warranty,
                    "insurance":insurance,
                    "battery_power":battery,
                    "operating_system":operating_system,
                    "brand":brand,
                    "primary_camera":primary_camera,
                    "secondary_camera":secondary_camera,
                    "sim_type":sim_type

                })            
                time.sleep(2)        
    

            for data in scraped_data:
            # Check if the product already exists in the database
                existing_product = ProductPhoneNeo.objects.filter(category=data['category'], title=data['title']).first()
                
                if existing_product:
                    if existing_product.price_range != data['price_text']:
                        existing_product.price_range = data['price_text']
                        existing_product.save()
                else:
                    new_product = ProductPhoneNeo(**data)
                    new_product.save()

scrapNeoPhone()

