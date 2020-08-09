import sys
sys.path.append("./deps")

from bs4 import BeautifulSoup
import requests
from .Item import Item
from .config import config
from .generate_html import generate_html
from .SubItem import SubItem

def scrape_titan(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    return __scrape(soup, url)

def __scrape(soup, url):
    item = Item()
    item.url = url

    # Name
    name = soup.find_all("span", class_="product-name")[0].text
    item.name = name

    # In stock
    in_stock = soup.find_all("span", class_="availability-msg")[0].find_all("span")[0].text
    if in_stock == "Out of Stock":
        item.in_stock = False
    elif in_stock == "In Stock":
        item.in_stock = True
    else:
        item.in_stock = None
    
    # Image
    img = soup.find_all("img", class_="img-fluid")[0]["src"]
    item.img = img

    return item