from dotenv import load_dotenv
from ebaysdk.finding import Connection
import os
import sqlite3
load_dotenv()
#API_KEY = os.getenv('api_key')


class Ebay_21(object):
    def __init__(self, name) -> None:
        self.api_key = os.getenv('api_key')
        self.name = name
        self.db_connection = sqlite3.connect('ebay_data.db')  # Connect to the database
        self.db_cursor = self.db_connection.cursor()
        self.create_table()

    def __iter__(self):
        return iter(self.retrieve_data_from_database())

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

            for item in response.reply.searchResult.item[:21]:

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
        # try:
        #     conn = sqlite3.connect('ebay_data.db')
        #     qry = self.db_cursor.execute("SELECT * FROM {}".format(self.name))
        #     rows = self.db_cursor.fetchall()
        #
        #     # data_dict = []
        #     # for row in rows:
        #     #     item_id = row[0]
        #     #     name = row[1]
        #     #     image = row[2]
        #     #     price = row[3]
        #     #     link = row[4]
        #     #     data_dict[item_id] = {
        #     #         'name': name,
        #     #         'image': image,
        #     #         'price': price,
        #     #         'link': link
        #     #     }
        #
        #     #return data_dict
        #
        #     #self.save_products_to_database()
        #     #conn = sqlite3.connect('zappos_data.db')
        #     # Execute a query to retrieve data
        #     #qry = "SELECT * FROM products;"
        #     with conn as connection:
        #         rows = self.db_cursor.fetchall()
        #         zappos_db = pd.DataFrame(rows)
        #     conn.close()
        #     return zappos_db
        #
        #
        # except Exception as e:
        #     print("Error occurred:", e)
        #     return None
        self.fetch()

        conn = sqlite3.connect('ebay_data.db')
        qry = "SELECT * FROM {}".format(self.name)
        with conn as connection:
            query_result = connection.execute(qry).fetchall()
            columns = ["index", "name", "image", "price", "link"]
            ebay_db = [dict(zip(columns, row)) for row in query_result]
        conn.close()

        return ebay_db

    def parse(self):
        pass


if __name__ == '__main__':
    ebay = Ebay_21(name='deals')
    ebay_items = ebay.retrieve_data_from_database()[:10]
    for item in ebay_items:
        print(item)