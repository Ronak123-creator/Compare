from bs4 import BeautifulSoup
import requests
import csv
from .models import *  # Adjust the import path according to your project
import re

# Set this flag to True if you want to run the scraping
RUN_SCRAPE = False

def scrape_and_insert():

    if not RUN_SCRAPE:
        print("Scraping is disabled Neo. To enable scraping, set RUN_SCRAPE to True.")
        return
    
    urls = [
        "https://neostore.com.np/product-category/dell-laptops",
        # Add other URLs here
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    scraped_data = []
    increment_step = 32
    max_pages = 3
    for url in urls:
        for i in range(max_pages):
            page_num = i * increment_step
            current_url = f"{url}/{page_num}" if page_num != 0 else url  # Use current_url
            webpage = requests.get(current_url, headers=headers)
            soup = BeautifulSoup(webpage.content, "html.parser")

            logo_img = soup.find("img", class_="img-header-logo")
            if logo_img:
                logo_url = logo_img["src"]
                
            else:
                print("Logo not found.") 

            websites = soup.find_all("h3", class_="product-title")
            

            for website in websites:
                link = website.a['href']
                title = website.text.strip()
                brand_match = re.search(r'^([^ ]+)', title)
                if brand_match:
                    brand = brand_match.group(1)
                else:
                    print("Brand not found in title")
                image = website.find_next("img")
                if image:
                    image_url = image['src']
                else:
                    image_url = ""
                price = website.find_next("span", class_="price")
                if price:
                    price_text = price.text
                else:
                    price_text = "N/A"

                product_page = requests.get(link, headers=headers)
                product_soup = BeautifulSoup(product_page.content, "html.parser")
                other_image = product_soup.find("div", class_="gallery")
                image_tags = other_image.find_all("img")

                image_urls = [img_tag["src"] for img_tag in image_tags]
                img1 = image_urls[0] if len(image_urls) > 0 else ""
                img2 = image_urls[1] if len(image_urls) > 1 else ""
                img3 = image_urls[2] if len(image_urls) > 2 else ""

                description = product_soup.find("div", class_="woocommerce-product-details__short-description")
                if description:
                    description_text = description.get_text(strip=True)
                else:
                    description_text = "N/A"
                    
                model = product_soup.find("div", class_="electro-description clearfix")
                model_name = model.h1
                if model_name:
                    model_text = model_name.get_text(strip=True)
                else:
                    model_text = "N/A"              
                
                ram_detail = ""
                gen_detail = ""
                display = ""
                storage = ""
                processor_name=""
                processor_speed=""
                touchscreen=""
                graphics=""
                resolution=""
                color=""
                warranty=""
                insurance=""
                battery = ""
                operating_system=""
                ports_and_connectivity=""
                table = product_soup.find("table")
                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        if "Ram" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                ram_detail = columns[1].get_text(strip=True)

                        if "Generation" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                gen_detail = columns[1].get_text(strip=True)

                        if "Display Size" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                display = columns[1].get_text(strip=True)

                        if "Storage" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                storage = columns[1].get_text(strip=True)

                        if "Processor" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                processor_name = columns[1].get_text(strip=True) 

                        if "Processor Speed" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                processor_speed = columns[1].get_text(strip=True)
                        
                        if "Touch Screen" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                touchscreen = columns[1].get_text(strip=True)
                                
                        if "Graphics" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                graphics = columns[1].get_text(strip=True)     

                        if "Maximum Display Resolution" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >=2:
                                resolution = columns[1].get_text(strip=True)
                                
                        if "Color" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                color = columns[1].get_text(strip=True)
                        
                        if "Warranty" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                warranty = columns[1].get_text(strip=True)
                        
                        if "Insurance" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                insurance = columns[1].get_text(strip=True)
                        
                        if "Battery" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                battery = columns[1].get_text(strip=True)

                        if "Operation System" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                operating_system = columns[1].get_text(strip=True)

                        if "Ports and Connectivity" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                p_tag = columns[1].find("p")
                                if p_tag:
                                    ports_and_connectivity = p_tag.get_text(strip=True)
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
                    "p_speed":processor_speed,
                    "touchscreen":touchscreen,
                    "graphics":graphics,
                    "maximum_display_resulation":resolution,
                    "color":color,
                    "warrenty":warranty,
                    "insurance":insurance,
                    "battery":battery,
                    "operating_system":operating_system,
                    "ports_and_connectivity":ports_and_connectivity,
                    "brand":brand,
                    "img1":img1,
                    "img2":img2,
                    "img3":img3,
                    "logo_url":logo_url,

                })

        with open("scraped.csv", "w", newline="\n", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Category", "Title", "Image", "Link", "Price", "Description", "Model", "RAM", "Generation", "Display", "Storage","processor","touchscreen","graphics","maximum display resulation","color","warrenty","insurance","Battery","operating_system","ports_and_connectivity"])
            for data in scraped_data:
                csvwriter.writerow(data.values())

        for data in scraped_data:
        # Check if the product already exists in the database
            existing_product = ProductNeo.objects.filter(category=data['category'], title=data['title']).first()
            
            if existing_product:
                if existing_product.price != data['price']:
                    existing_product.price = data['price']
                    existing_product.save()
            else:
                new_product = ProductNeo(**data)
                new_product.save()

# Call the function to start the scraping process
scrape_and_insert()
