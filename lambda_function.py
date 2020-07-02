import sys
sys.path.append("./deps")

from bs4 import BeautifulSoup
import requests
import boto3
from botocore.exceptions import ClientError
import json
from config import config
from generate_html import generate_html

class Item:
    def __init__(self, url: str):
        self.url = url
        
        # Initalize information to scrape
        self.soup = None
        self.name = None
        self.img = None
        self.in_stock = None
        self.sub_items = []

        # Scrape item
        self.scrape_item()

    def __repr__(self):
        if self.sub_items:
            in_stock_str = '\n'.join([repr(i) for i in self.sub_items])
            in_stock_str = f"{in_stock_str}"
        else:
            in_stock_str = f"In Stock: {self.in_stock}"
        return f"Product: {self.name}\nUrl: {self.url}\n{in_stock_str}\nImage: {self.img}\n"
    
    def scrape_item(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, 'html.parser')

        # Check if single or multi
        single = False if self.soup.find_all("table", class_="grouped-items-table") else True
        if single:
            self.scrape_single()
        else:
            self.scrape_multi()
    
    def scrape_single(self):
        # Name
        try:
            self.name = self.soup.find_all("h1",itemprop="name")[0].text
        except IndexError:
            self.name = "Error: Not Found"
        
        # Img
        try:
            self.img = self.soup.find_all("img", class_="img-responsive")[0]["src"]
        except IndexError:
            self.img = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"
        
        # In Stock
        in_stock_class = self.soup.find_all("p",class_="in-stock")
        out_of_stock_class = self.soup.find_all("p",class_="out-of-stock")
        if out_of_stock_class:
            self.in_stock = False
        elif in_stock_class:
            self.in_stock = True
        else:
            self.in_stock = "Error: Not Found"
    
    def scrape_multi(self):
        # Name
        try:
            self.name = self.soup.find_all("h1",itemprop="name")[0].text
        except IndexError:
            self.name = "Error: Not Found"
        
        # Img
        try:
            self.img = self.soup.find_all("img", class_="img-responsive")[0]["src"]
        except IndexError:
            self.img = "https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg"

        items_table = self.soup.find_all("table", class_="grouped-items-table")[0].find_all("tr")
        for row in items_table:
            tds = row.find_all("td")
            if len(tds) < 3:
                continue
            name = tds[0].text.replace("\n","").strip()
            in_stock = False if tds[-1].text.replace("\n","").strip() else True
            if self.in_stock is None and in_stock == True:
                self.in_stock = True
            self.sub_items.append(SubItem(name, in_stock))
        if self.in_stock is None:
            self.in_stock = False

    def to_json(self):
        return {
            "name": self.name,
            "url": self.url,
            "img": self.img,
            "in_stock": self.in_stock,
            "sub_items": [s.to_json() for s in self.sub_items]
        }

class SubItem:
    def __init__(self, name: str, in_stock: bool):
        self.name = name
        self.in_stock = in_stock
    
    def __repr__(self):
        return f"\tSub-Item: {self.name} - In Stock: {self.in_stock}"
    
    def to_json(self):
        return {
            "name": self.name,
            "in_stock": self.in_stock
        }

def send_email(json_str):
    client = boto3.client('ses', region_name='us-east-1')
    html = generate_html(json.loads(json_str))
    with open("output.html","w",encoding="utf-8") as f:
        f.write(html)
    try:
        response = client.send_email(
            Destination={
                "ToAddresses": config.reciever_emails,
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": "UTF-8",
                        "Data": html,
                    },
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": html,
                    },
                },
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": "Auto Rep Fitness In-Stock Update"
                }
            },
            Source=config.sender_email
        )
    except ClientError as e:
        return (1, e.__traceback__)
    else:
        return (0, response["MessageId"])

# AWS Lambda
def lambda_handler(event, context):
    to_scrape = requests.get("https://raw.githubusercontent.com/jdglaser/rep-scrape/master/to_scrape.txt").text.split("\n")
    output = []
    for i in to_scrape:
        output.append(Item(i).to_json())
    response = send_email(json.dumps(output))
    if response[0] == 0: 
        return {
            'statusCode': 200,
            'body': "email sent successfully"
        }
    else:
        return {
            'statusCode': 201,
            'body': response[1]
        }