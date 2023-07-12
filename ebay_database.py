import requests
import json
import sqlite3

class Ebay:

    def __init__(self, name, zipcode):
        self.name = name
        self.location = zipcode
        self.db_connection = sqlite3.connect('ebay_data.db')  # Connect to the database
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
        Makes an API request to the eBay API and retrieves the search results for the specified product name.

        Returns:
        - json_data (dict): The JSON response from the API containing the search results.
        - None: If there was an error in the API request.
        """
        params = {
            'api_key': '4628D7F6193C4219B168D3FE361ADB2F',
            'ebay_domain': 'ebay.com',
            'type': 'search',
            'search_term': self.name,
            'customer_location': 'us',
            'customer_zipcode': self.location
        }

        response = requests.get('https://api.countdownapi.com/request', params=params)

        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print("Error in API request:", response.status_code)
            return None

    def extract_product_names(self, json_data):
        """
        Extracts the names of the products from the JSON data.

        Args:
        - json_data (dict): The JSON response from the eBay API.

        Returns:
        - product_names (dict): A dictionary where the keys are the positions and the values are the product names.
        - None: If the input JSON data is None.
        """
        if json_data is None:
            return None

        product_names = {}
        products = json_data['search_results']

        for item in products[:10]:
            product_names[item['position']] = item['title']

        return product_names

    def extract_product_images(self, json_data):
        """
        Extracts the images of the products from the JSON data.

        Args:
        - json_data (dict): The JSON response from the eBay API.

        Returns:
        - product_images (dict): A dictionary where the keys are the positions and the values are the product images.
        - None: If the input JSON data is None.
        """
        if json_data is None:
            return None

        product_images = {}
        products = json_data['search_results']

        for item in products[:10]:
            product_images[item['position']] = item['image']

        return product_images

    def extract_product_prices(self, json_data):
        """
        Extracts the prices of the products from the JSON data.

        Args:
        - json_data (dict): The JSON response from the eBay API.

        Returns:
        - product_prices (dict): A dictionary where the keys are the positions and the values are the product prices.
        - None: If the input JSON data is None.
        """
        if json_data is None:
            return None

        product_prices = {}
        products = json_data['search_results']

        for item in products[:10]:
            price = item['price']['value']
            product_prices[item['position']] = price

        return product_prices

    def extract_product_links(self,json_data):
        """
        Extracts the product links from the JSON data.

        Args:
        - json_data (dict): The JSON response from the eBay API.

        Returns:
        - product_links (dict): A dict of the links of the first 10 products.
        - None: If the input JSON data is None.
        """
        products = json_data['search_results']

        product_links = {}
        for item in products[:10]:  # Extract links from the first 10 products
            link = item["link"]
            product_links[item['position']] = link

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


if __name__ == "__main__":
    ebay = Ebay("iphone", "61455")  # Replace "iphone" with your desired search term and "12345" with the desired ZIP code
    ebay.save_products_to_database()
    ebay.close_database()