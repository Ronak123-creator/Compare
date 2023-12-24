import re
from bs4 import BeautifulSoup
import requests

urls = [
    "https://itti.com.np/laptops-by-brands/dell",
    # Add more URLs here if needed
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

# Define a regular expression pattern to match i3, i5, i7, Ryzen 3, Ryzen 5, Ryzen 7 variations
processor_pattern = re.compile(r'(i[357]|Ryzen [357]|[Rr]yzen [357])', re.IGNORECASE)

for url in urls:
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    websites = soup.find_all("li", class_="item product product-item")

    for website in websites:
        title = website.find("h2", class_="product name product-item-name product-name").text.strip()
        
        # Extracting the processor information using regular expressions
        processor_match = processor_pattern.search(title)
        if processor_match:
            processor_info = processor_match.group()
            print("Processor:", processor_info)
