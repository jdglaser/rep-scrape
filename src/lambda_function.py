import sys
sys.path.append("./app/deps")

import json
import requests
from bs4 import BeautifulSoup

import boto3
from app.config import config
from app.generate_html import generate_html
from app.Item import Item
from app.RepScraper import scrape_rep
from app.TitanScraper import scrape_titan
from botocore.exceptions import ClientError


def send_email(json_str):
    client = boto3.client('ses', region_name='us-east-1')
    html = generate_html(json.loads(json_str))
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
                    }
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
    to_scrape = json.loads(requests.get("https://raw.githubusercontent.com/jdglaser/rep-scrape/master/to_scrape.json").text)
    output = []

    # Scrape rep
    for i in to_scrape["rep"]:
        item = scrape_rep(i)
        output.append(item.to_json())

    # Scrape titan
    for i in to_scrape["titan"]:
        item = scrape_titan(i)
        output.append(item.to_json())

    # Send response
    response = send_email(json.dumps(output))

    output_str = '\n'.join([i["url"] for i in output])
    body = f"email sent successfully. checked following urls: {output_str}"

    if response[0] == 0: 
        return {
            'statusCode': 200,
            'body': body
        }
    else:
        return {
            'statusCode': 201,
            'body': response[1]
        }
