import sys
sys.path.append("./deps")

from bs4 import BeautifulSoup
import requests
from .Item import Item
from .config import config
from .generate_html import generate_html
from .SubItem import SubItem

def scrape_rep(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Check if single or multi
    single = False if soup.find_all("table", class_="grouped-items-table") else True
    if single:
        return __scrape_single(soup, url)
    else:
        return __scrape_multi(soup, url)

def __scrape_single(soup, url):
    item = Item()
    item.url = url

    # Name
    try:
        item.name = soup.find_all("h1",itemprop="name")[0].text
    except IndexError:
        item.name = "Error: Not Found"
    
    # Img
    try:
        item.img = soup.find_all("img", class_="img-responsive")[0]["src"]
    except IndexError:
        item.img = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"
    
    # In Stock
    in_stock_class = soup.find_all("p",class_="in-stock")
    out_of_stock_class = soup.find_all("p",class_="out-of-stock")
    
    if out_of_stock_class:
        item.in_stock = False
    elif in_stock_class:
        item.in_stock = True
    else:
        item.in_stock = "Error: Not Found"

    return item

def __scrape_multi(soup, url):
    item = Item()
    item.url = url

    # Name
    try:
        item.name = soup.find_all("h1",itemprop="name")[0].text
    except IndexError:
        item.name = "Error: Not Found"
    
    # Img
    try:
        item.img = soup.find_all("img", class_="img-responsive")[0]["src"]
    except IndexError:
        item.img = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"

    items_table = soup.find_all("table", class_="grouped-items-table")[0].find_all("tr")
    for row in items_table:
        tds = row.find_all("td")
        if len(tds) < 3:
            continue
        name = tds[0].text.replace("\n","").strip()
        in_stock = False if tds[-1].text.replace("\n","").strip() else True
        if item.in_stock is None and in_stock == True:
            item.in_stock = True
        item.sub_items.append(SubItem(name, in_stock))
    if item.in_stock is None:
        item.in_stock = False

    return item
