import re
from bs4 import BeautifulSoup
import requests

urls = [
    "https://itti.com.np/laptops-by-brands/hp",
    # Add more URLs here if needed
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

for url in urls:
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    websites = soup.find_all("li", class_="item product product-item")

    for website in websites:
        title = website.find("h2", class_="product name product-item-name product-name").text.strip()
        
        # Define keywords and patterns to match
        keywords = ["Ryzen", "2020", "2021", "2022", "2023", "/", "Amd", "i3", "i5", "i7", "I3", "I5", "I7", "I9", "Celeron", "Intel", "INTEL", "intel","Core"]
        pattern = '|'.join(map(re.escape, keywords))
        
        # Use regular expression to extract desired text
        extracted_text = re.split(pattern, title)[0].strip()
        
        print(extracted_text)
