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
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                image TEXT,
                price REAL,
                link TEXT
            )
        ''')
        self.db_connection.commit()

    def insert_product(self, name, image, price, link):
        # Insert a product into the database
        self.db_cursor.execute('''
            INSERT INTO products (name, image, price, link)
            VALUES (?, ?, ?, ?)
        ''', (name, image, price, link))
        self.db_connection.commit()


    def search(self):
        """
        Makes an API request to the Zappos API and retrieves the search results for the specified product name.

        Returns:
        - json_data (dict): The JSON response from the API containing the search results.
        - None: If there was an error in the API request.
        """

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
            json_data = json_data["results"]
            return json_data
        else:
            print("Error in API request:", response.status_code)
            return None


    def extract_product_names(self, data):
        """
        Extracts the names of the products from the Data DataFrame.

        Args:
        - json_data (dict): The DataFrame response from the Zappos API.

        Returns:
        - product_names (dict): A dictionary where the keys are the positions and the values are the product names.
        - None: If the input JSON data is None.
        """
        if data is None:
            return None

        product_names = {}
        for x in range(len(data)):
            product_names[x] = data[x]["productName"]
        return product_names


    def extract_product_images(self, data):
        """
        Extracts the images of the products from the JSON data.

        Args:
        - json_data (dict): The JSON response from the Zappos API.

        Returns:
        - product_images (dict): A dictionary where the keys are the positions and the values are the product images.
        - None: If the input JSON data is None.
        """
        if data is None:
            return None

        
        product_images = {}
        for x in range(len(data)):
            product_images[x] = data[x]["thumbnailImageUrl"]

        return product_images


    def extract_product_prices(self, data):
        """
        Extracts the prices of the products from the JSON data.

        Args:
        - json_data (dict): The JSON response from the Zappos API.

        Returns:
        - product_prices (dict): A dictionary where the keys are the positions and the values are the product prices.
        - None: If the input JSON data is None.
        """
        if data is None:
            return None

        product_prices = {}

        for x in range(len(data)):
            product_prices[x] = data[x]["price"]

        return product_prices


    def extract_product_links(self, data):
        """
        Extracts the product links from the JSON data.

        Args:
        - json_data (dict): The JSON response from the Zappos API.

        Returns:
        - product_links (dict): A dict of the links of the first 10 products.
        - None: If the input JSON data is None.
        """
        if data is None:
            return None

        product_links = {}

        for x in range(len(data)):
            product_links[x] = data[x]["productUrl"]

        return product_links

    def save_products_to_database(self):
        json_data = self.search()

        product_names = self.extract_product_names(json_data)
        product_images = self.extract_product_images(json_data)
        product_prices = self.extract_product_prices(json_data)
        product_links = self.extract_product_links(json_data)

        for position in product_names:
            name = product_names[position]
            image = product_images.get(position, '')
            price = product_prices.get(position, 0.0)
            link = product_links.get(position, '')

            self.insert_product(name, image, price, link)
        

    def close_database(self):
        self.db_cursor.close()
        self.db_connection.close()

    def returnDatabase(self):
        self.save_products_to_database()
        conn = sqlite3.connect('zappos_data.db')
        # Execute a query to retrieve data
        qry = "SELECT * FROM products;"
        with conn as connection:
            query_result = connection.execute(qry).fetchall()
            zappos_db = pd.DataFrame(query_result, columns=["index", "name", "image", "price", "link"])
            table = pd.DataFrame.to_html(zappos_db)
        conn.close()
        return table


    

