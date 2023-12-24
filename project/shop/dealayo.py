# here description is added 

from bs4 import BeautifulSoup
import requests
import re
import time
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
    

def clean_title(text):
    pattern = r"(Ram|Storage|3G|4G|5G|core|1GB|2GB|3GB|4GB|5GB|6GB|7GB|8GB|9GB|10GB|12GB|16GB|24GB|32GB|1GM|2GM|3GM|4GM|5GM|6GM|7GM|8GM|9GM|10GM|12GM|16GM|24GM|32GM|The|Mobile|1 GB|2 GB|3 GB|4 GB|5 GB|6 GB|7 GB|8 GB|9 GB|10 GB|12 GB|16 GB|24 GB|\||,|-|/|\().*"

    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text

def extractband(text):
    first_word = text.split()[0]
    return first_word


RUN_SCRAPE = False

def scrapPhone():
    if not RUN_SCRAPE:
        print("Scraping is disabled for deal. To enable scraping, set RUN_SCRAPE to True.")
        return

    base_url = "https://www.dealayo.com/mobile.html?p="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    scraped_data = []
    for page_number in range(1,18):
        url = base_url + str(page_number)
        webpage = requests.get(url, headers=headers)        
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Find all product elements
        websites = soup.find_all("li", class_="item product-item col-desktop-4 col-tablet-l-3 col-tablet-p-2 col-mobile-2")   
        for website in websites:
            # Extract product information
            link = website.find("a", class_="product-image no-alt-img")['href']
            title_text = website.find("h2", class_="product-name").a.text.strip()
            title = clean_title(title_text)
            print(title)
            
            image = website.find_next("img", class_="img-responsive")
            if image:
                image_url = image['src']
            else:
                image_url = ""

            price_text = website.find("span", class_="price")
            if price_text:
                pprice = price_text.text.strip()
            else:
                pprice = "N/A" 
            price = extract_price(pprice)  
            brand = extractband(title)
            
            # Visit the individual product URL to get the description
            product_page = requests.get(link, headers=headers)
            product_soup = BeautifulSoup(product_page.content, "html.parser")
            
            brand = ""
            model = ""
            color = ""
            sim_type = ""
            sound = ""
            date = ""
            dimensions =""
            weight =""
            display =""
            type = ""
            touchscreen = ""
            resolution = ""
            density = ""
            protection = ""
            rear_camera = ""
            rear_camera_extra = ""
            camera_features = ""
            front_camera = ""
            front_camera_extra = ""
            video = ""
            processor = ""
            cpu = ""
            gpu = ""
            ram = ""
            storage = ""
            expandablememory = ""
            memorycardslot = ""
            operatingsystem = ""
            technology = ""
            wlan = ""
            nfc = ""
            usb = ""
            battery = ""
            charger = ""
            sensors = ""
            warranty = ""
            tables = product_soup.find_all("table", class_="data-table")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    columns = row.find_all(["th", "td"])
                    if len(columns) >= 2:
                        key = columns[0].get_text(strip = True)
                        value = columns[1].get_text(strip =True)  
                        if key == "Brand":
                            brand = value
                        if key == "Model":
                            model = value
                        if key == "Color":
                            color = value
                        if key == "SIM":
                            sim_type = value
                        if key == "Sound":
                            sound = value
                        if key == "Date":
                            date = value
                        if key == "Product Dimensions":
                            dimensions = value
                        if key == "Weight":
                            weight = value
                        if key == "Screen size(Inches)":
                            display = value
                        if key == "Type":
                            type = value
                        if key == "Touchscreen":
                            touchscreen = value
                        if key == "Resolution(Pixel)":
                            resolution = value
                        if key == "Pixel Density":
                            density = value
                        if key == "Protection":
                            protection = value
                        if key == "Rear Camera(MegPixel)":
                            rear_camera = value
                        if key == "Rear Camera Extra":
                            rear_camera_extra = value
                        if key == "Camera Features":
                            camera_features = value
                        if key == "Front Camera(MegPixel)":
                            front_camera = value
                        if key == "Front Camera Extra":
                            front_camera_extra = value
                        if key == "Video":
                            video = value
                        if key == "Processor(Chipset)":
                            processor = value
                        if key == "Processor(CPU)":
                            cpu = value
                        if key == "Processor(GPU)":
                            gpu = value
                        if key == "RAM":
                            ram = value
                        if key == "Internal Memory":
                            storage = value
                        if key == "Expandable Memory":
                            expandablememory = value
                        if key == "Memory Card Slot":
                            memorycardslot = value
                        if key == "Operating System":
                            operatingsystem = value
                        if key == "Technology":
                            technology = value
                        if key == "Wlan":
                            wlan = value
                        if key == "NFC":
                            nfc = value
                        if key == "USB":
                            usb = value
                        if key == "Battery Info":
                            battery = value
                        if key == "Battery Features":
                            charger = value
                        if key == "Sensors":
                            sensors = value
                        if key == "Warranty Period":
                            warranty = value

            scraped_data.append({
                "link":link,
                "title":title,
                "image_url":image_url,
                "price":price,
                "brand":brand,
                "model":model,
                "color":color,
                "sim_type":sim_type,
                "sound":sound,
                "date":date,
                "dimensions":dimensions,
                "weight":weight,
                "display":display,
                "type":type,
                "touchscreen":touchscreen,
                "resolution":resolution,
                "density":density,
                "protection":protection,
                "rear_camera":rear_camera,
                "rear_camera_extra":rear_camera_extra,
                "camera_features":camera_features,
                "front_camera":front_camera,
                "front_camera_extra": front_camera_extra,
                "video":video,
                "processor":processor,
                "cpu":cpu,
                "gpu":gpu,
                "ram":ram,
                "storage":storage,
                "expandablememory":expandablememory,
                "memorycardslot":memorycardslot,
                "operatingsystem":operatingsystem,
                "technology":technology,
                "wlan":wlan,
                "nfc":nfc,
                "usb":usb,
                "battery":battery,
                "charger":charger,
                "sensors":sensors,
                "warranty":warranty,
            })

        for data in scraped_data:
            existing_product = ProductPhoneDeal.objects.filter(title=data['title']).first()
            if existing_product:
                if existing_product.price != data['price']:
                    existing_product.price = data['price']
                    existing_product.save()
            else:
                new_product = ProductPhoneDeal(**data)
                new_product.save()
                print(f"Added new product: {new_product.title}")
scrapPhone()
