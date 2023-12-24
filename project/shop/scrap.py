# here description is added 

from bs4 import BeautifulSoup
import requests
import csv

# List of URLs for different product categories
urls = [
    "https://neostore.com.np/product-category/dell-laptops",
    # "https://neostore.com.np/product-category/lenovo-laptops",
    # "https://neostore.com.np/product-category/asus-laptops",
    # "https://neostore.com.np/product-category/msi-laptops",
    # "https://neostore.com.np/product-category/avita",
    # "https://neostore.com.np/product-category/macbook",
    # "https://neostore.com.np/product-category/hp",
    # "https://neostore.com.np/product-category/acer-laptops",    
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

# Create a CSV file and write headers
with open("scraped.csv", "w", newline= "\n", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Category", "Title", "Image", "Link", "Price", "Description", "Model", "RAM", "Generation", "Display", "Storage", "Processor", "Touch Screen", "Graphics", "Resolution", "Color", "Warranty", "Insurance"])  # Updated header row

    for url in urls:
        max_page = 3
        for page in range(1, max_page +1):
            webpage = requests.get(url, headers=headers)
            soup = BeautifulSoup(webpage.content, "html.parser")

            # Find all <h3> elements with the class 'product-title'
            websites = soup.find_all("h3", class_="product-title")

            for website in websites:
                link = website.a['href']  # Extract the 'href' attribute from the <a> tag within the <h3> element
                title = website.text.strip()  # Extract the text from the <h3> element
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

                # Visit the individual product URL to get the description
                product_page = requests.get(link, headers=headers)
                product_soup = BeautifulSoup(product_page.content, "html.parser")

                description = product_soup.find("div", class_="woocommerce-product-details__short-description")
                if description:
                    description_text = description.get_text(strip=True)
                else:
                    description_text = "N/A"
                
                model = product_soup.find("div", class_ = "electro-description clearfix" )
                model_name = model.h1
                if model_name:
                    model_text = model_name.get_text(strip=True)
                else:
                    model_text = "N/A"             
          
                # from table
                ram_detail = ""
                gen_detail =""
                display =""
                storage=""
                processor=""
                touchscreen=""
                graphics=""
                resolution=""
                color=""
                warranty=""
                insurance=""
                table = product_soup.find("table")
                if table:
                    rows = table.find_all("tr")
                    for row in rows:
                        if "Ram" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                ram_detail = columns[1].get_text(strip = True)                           
                            
                
                        if "Generation" in row.text:
                            columns = row.find_all("td")
                            if len(columns) >= 2:
                                gen_detail = columns[1].get_text(strip = True)
                                
                        
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
                                processor = columns[1].get_text(strip=True)  
                        
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
                                        
                # Write the data to the CSV file
                
                data = f"URL: {url}\nTitle: {title}\nImage URL: {image_url}\nLink: {link}\nPrice: {price_text}\nDescription: {description_text}\nModel: {model_text}\nRam: {ram_detail}\nGeneration: {gen_detail}\nDisplay: {display}\nStorage: {storage}\nProcessor: {processor}\nTouch Screen: {touchscreen}\nGraphics: {graphics}\nResolution: {resolution}\nColor: {color}\nWarranty: {warranty}\nInsurance: {insurance}\n "
                csvwriter.writerow([data])
               

        


