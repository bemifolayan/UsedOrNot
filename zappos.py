import requests
import json
import pandas as pd
import os
import sqlite3
import sqlalchemy as db

class Zappos:

    def __init__(self, name):
        self.name = name
        self.db_connection = sqlite3.connect('zappos_data.db')  # Connect to the database
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
            INSERT INTO products (name, image, price, link)
            VALUES (?, ?, ?, ?)
        ''', (name, image, price, link))
        self.db_connection.commit()

    def search(self):

        url = "https://zappos1.p.rapidapi.com/products/list"

        querystring = {"page":"1","limit":"100", "query": self.name, "sort":"relevance/desc"}

        payload = []
        headers = {
	                "content-type": "application/json",
	                "X-RapidAPI-Key": os.environ.get('Zappos_API_Key'),
	                "X-RapidAPI-Host": "zappos1.p.rapidapi.com"
                }   

        response = requests.post(url, json=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            json_data = response.json()
            data = json_data["results"]
            result = []
            for x in range(len(data)):
                index = x
                name = data[x]["productName"]
                image = data[x]["thumbnailImageUrl"]
                price = data[x]["price"]
                link = data[x]["productUrl"]

                result.append([index,name,image,price,link])

            return result
        else:
            print("Error in API request:", response.status_code)
            return None


    def close_database(self):
        self.db_cursor.close()
        self.db_connection.close()

    def returnDatabase(self):
        return self.search()

        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.width', None)

        # conn = sqlite3.connect('zappos_data.db')
        # # Execute a query to retrieve data
        # qry = "SELECT * FROM {}".format(self.name)
        # print(qry)
        # with conn as connection:
        #     query_result = connection.execute(qry).fetchall()
        #     zappos_db = pd.DataFrame(query_result,columns=["index", "name", "image", "price", "link"])
        #     table = pd.DataFrame.to_numpy(zappos_db)
        #     #first_ten_rows = zappos_db.head(10)
        # conn.close()
        # return table


hello = Zappos("iPhone")
print(hello.returnDatabase())    
    
    # def save_products_to_database(self):
    #     json_data = self.search()
    #     product_names = self.extract_product_names(json_data)
    #     product_images = self.extract_product_images(json_data)
    #     product_prices = self.extract_product_prices(json_data)
    #     product_links = self.extract_product_links(json_data)
    #     products = []
    #     for position in product_names:
    #         name = product_names[position]
    #         image = product_images.get(position, '')
    #         price = product_prices.get(position, 0.0)
    #         link = product_links.get(position, '')
    #         product = {
    #             'name': name,
    #             'image': image,
    #             'price': price,
    #             'link': link,
    #         }
    #         products.append(product)
    #     return products
 
