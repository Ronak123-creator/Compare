import re
from bs4 import BeautifulSoup
import requests

urls = [
    "https://neostore.com.np/product-category/dell-laptops",
    # Add more URLs here if needed
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

# Regular expression pattern to match processor types
processor_pattern = re.compile(r'(i3|i5|i7|i9|I3|I5|I9|AMD Ryzen\s(?:3|5|7|9)\s\d+|Ryzen\s(?:3|5|7)\s\d+(?:[UH])?|[iI]\d-\d{4}[UH]?)\b')


for url in urls:
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    websites = soup.find_all("h3", class_="product-title")

    for website in websites:
        title = website.text.strip()
        processor_match = processor_pattern.search(title)
        
        if processor_match:
            processor_type = processor_match.group(0)
            print(processor_type + ":", title)
        else:
            print("No processor type found:", title)
