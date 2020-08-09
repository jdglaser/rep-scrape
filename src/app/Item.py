import sys
sys.path.append("./deps")

from bs4 import BeautifulSoup
import requests
from .config import config
from .generate_html import generate_html
from .SubItem import SubItem

class Item:
    def __init__(self):
        # Initalize information to scrape
        self.name = None
        self.img = None
        self.in_stock = None
        self.url = None
        self.sub_items = []

    def __repr__(self):
        if self.sub_items:
            in_stock_str = '\n'.join([repr(i) for i in self.sub_items])
            in_stock_str = f"{in_stock_str}"
        else:
            in_stock_str = f"In Stock: {self.in_stock}"
        return f"Product: {self.name}\nUrl: {self.url}\n{in_stock_str}\nImage: {self.img}\n"

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "img": self.img,
            "in_stock": self.in_stock,
            "sub_items": [s.to_json() for s in self.sub_items]
        }