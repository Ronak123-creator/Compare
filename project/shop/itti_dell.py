
from bs4 import BeautifulSoup
import requests
import re
from .models import *

RUN_SCRAPE = False

def scrape_and_insert1():
    if not RUN_SCRAPE:
        print("Scraping is disabled Itti. To enable scraping, set RUN_SCRAPE to True.")
        return

    urls = [
        "https://itti.com.np/laptops-by-brands/dell?product_list_limit=36",
        "https://itti.com.np/laptops-by-brands/dell?product_list_limit=36&p=2",  
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    scraped_data = []
    for url in urls:
        # ... (rest of your existing code to scrape data and populate `scraped_data`)
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Find all <h3> elements with the class 'product-title'
        websites = soup.find_all("li", class_="item product product-item")

        for website in websites:
            ram_detail = ""
            gen_detail =""
            display =""
            storage=""
            processor_name=""
            touchscreen=""
            graphics=""
            resolution=""
            color=""
            warranty=""
            insurance=""
            
            
            link = website.a['href']
            
            title = website.find("h2", class_="product name product-item-name product-name").text.strip()
            print("Title:", title)
            
            image = website.find_next("img")
            if image:
                image_url = image['data-src']
            else:
                image_url = ""
            
            price = website.find_next("span", class_="price")  # Find the next <span> element with the specified class
            if price:
                price_text = price.text
            else:
                price_text = "-"
            
            # Visit the individual product URL to get the description
            product_page = requests.get(link, headers=headers)
            product_soup = BeautifulSoup(product_page.content, "html.parser")
            
            description_div = product_soup.find("div", class_="value", itemprop="description")
            if description_div:
                description_text = " ".join([p.get_text(strip=True) for p in description_div.find_all("p")])
            else:
                description_text = ""

            model_element = product_soup.find("div", class_="page-title-wrapper product")
            if model_element:
                model_text = model_element.h1.get_text(strip=True)
            
                # Use regular expression to extract the model name
                model_match = re.search(r'(\w+(?:\s+\w+)*) \d{4}', model_text)
                if model_match:
                    model_text = model_match.group(1)
            else:
                model_text = "N/A"
            # from table

            
            table = product_soup.find("table")
            if table:
                rows = table.find_all("tr")
                for row in rows:
                    if "Memory" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            ram_detail = columns[1].get_text(strip = True)
                            print(ram_detail)

                    if "CPU" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            processor_name = columns[1].get_text(strip = True)                           
                        
            
                    if "Generation" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            gen = columns[1].get_text(strip = True)                                
                            # regular expression
                            generation_match = re.search(r'((?:\S+\s+){2}\S+)', gen, re.IGNORECASE)                            
                            if generation_match:
                                gen_detail = generation_match.group(1)
                                                    
                    

                
                    if "Display" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            display_text = columns[1].get_text(strip=True)
                            display_match = re.search(r'\d+\.\d+-inch [^;]+', display_text)
                            if display_match:
                                display = display_match.group(0)
                                
                            resolution_match = re.search(r'(\d+ x \d+) pixels', display_text)
                            if resolution_match:
                                resolution = resolution_match.group(1)
                            
                            touch_match = re.search(r'(Touch|Non-Touch)', display_text)
                            if touch_match:
                                touchscreen = touch_match.group(0)                                             
                            
                    
                    if "Storage" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            storage = columns[1].get_text(strip=True)
                        
                    if "Graphics" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            graphics = columns[1].get_text(strip=True)    
                    
                    
                    if "Color" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            color = columns[1].get_text(strip=True)
                    else:
                        color = "N/A"
                        
                    if "Warranty" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            warranty = columns[1].get_text(strip=True)
                    else: 
                        warranty = "N/A"
                    
                    if "Insurance" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            insurance = columns[1].get_text(strip=True)
                    else:
                        insurance = "-"


                    if "Battery" in row.text:
                        columns = row.find_all("td")
                        if len(columns) >= 2:
                            battery = columns[1].get_text(strip=True)
                    else:
                        insurance = "-"


            scraped_data.append({
            "category": url,
            "title": title,
            "image": image_url,
            "link": link,
            "price": price_text,
            "description": description_text,
            "model": model_text,
            "ram": ram_detail,
            "generation": gen_detail,
            "display": display,
            "storage": storage,
            "processor":processor_name,
            "touchscreen":touchscreen,
            "graphics":graphics,
            "maximum_display_resulation":resolution,
            "color":color,
            "warrenty":warranty,
            "insurance":insurance,
            "battery":battery,

        }) 

    for data in scraped_data:
        # Check if the product already exists in the database
        existing_product = ProductItti.objects.filter(category=data['category'], title=data['title']).first()
        
        if existing_product:
            if existing_product.price != data['price']:
                existing_product.price = data['price']
                existing_product.save()
        else:
            new_product = ProductItti(**data)
            new_product.save()

scrape_and_insert1()