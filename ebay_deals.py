import requests
from dotenv import load_dotenv
import json
import sqlite3
import os

load_dotenv()


class EbayDeals:

    def __init__(self, name) -> None:
        self.api_key = os.getenv('api_deals')
        self.name = name
        self.db_connection = sqlite3.connect('ebay_data.db')  # Connect to the database
        self.db_cursor = self.db_connection.cursor()
        self.create_table()


    def __iter__(self):
        return iter(self.extract_deal_info(self.search()))

    def create_table(self):
        # Create a table to store the product data
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY,
                name TEXT,
                image TEXT,
                price REAL,
                link TEXT
            )
        '''.format(self.name))
        self.db_connection.commit()

    def insert_product(self, name, image, price, link):
        # Insert a product into the database
        self.db_cursor.execute('''
            INSERT INTO {} (name, image, price, link)
            VALUES (?, ?, ?, ?)
        '''.format(self.name), (name, image, price, link))
        self.db_connection.commit()

    def search(self):
        # Set up the request parameters
        params = {
            'api_key': self.api_key,
            'type': 'deals',
            'url': 'https://www.ebay.com/deals'
        }

        # Make the HTTP GET request to the Countdown API
        api_result = requests.get('https://api.countdownapi.com/request', params=params)

        # Print the JSON response from Countdown API
        json_data = json.dumps(api_result.json())

        return json_data

    def extract_deal_info(self, json_data):
        if json_data is None:
            return None

        data = json.loads(json_data)
        deals_results = data["deals_results"]

        deal_info = []
        for result in deals_results[:10]:
            item_info = {
                "name": result["title"],
                "previous_price": result.get("was_price", {}).get("raw"),
                "current_price": result.get("price", {}).get("raw"),
                "link": result.get("link"),
                "image": result.get("image")
            }
            if item_info["name"] and item_info["current_price"]:
                self.insert_product(item_info["name"], item_info["image"], item_info["current_price"],
                                    item_info["link"])
                deal_info.append(item_info)

        return deal_info


if __name__ == '__main__':
    ebay = EbayDeals(name='deals')
    json_data = ebay.search()
    deal_info = ebay.extract_deal_info(json_data)
    print(deal_info)
