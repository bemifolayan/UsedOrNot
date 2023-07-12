from dotenv import load_dotenv
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import os
import sqlite3
import pprint
load_dotenv()
API_KEY = os.getenv('api_key')


class Ebay_21(object):
    def __init__(self, API_KEY, name) -> None:
        self.api_key = API_KEY
        self.name = name
        self.db_connection = sqlite3.connect('ebay_data.db')  # Connect to the database
        self.db_cursor = self.db_connection.cursor()
        self.create_table()

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

    def fetch(self):
        try:
            api = Connection(appid=self.api_key, config_file=None, siteid="EBAY-US")
            response = api.execute('findItemsAdvanced', {'keywords': self.name})
            # pprint.pprint(response.reply)
            # print(response.reply)

            for item in response.reply.searchResult.item:
                item_id = item.itemId
                name = item.title
                image = item.galleryURL
                price = item.sellingStatus.currentPrice.value
                link = item.viewItemURL

                self.insert_product(name, image, price, link)

            return True
        except Exception as e:
            print("Error occurred:", e)
            return False

    def retrieve_data_from_database(self):
        try:
            self.db_cursor.execute("SELECT * FROM {}".format(self.name))
            rows = self.db_cursor.fetchall()

            data_dict = {}
            for row in rows:
                item_id = row[0]
                name = row[1]
                image = row[2]
                price = row[3]
                link = row[4]
                data_dict[item_id] = {
                    'name': name,
                    'image': image,
                    'price': price,
                    'link': link
                }

            return data_dict
        except Exception as e:
            print("Error occurred:", e)
            return None

    def parse(self):
        pass


if __name__ == '__main__':
    e = Ebay_21(API_KEY, 'iphone')
    e.fetch()
    e.parse()