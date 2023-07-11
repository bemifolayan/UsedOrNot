import requests
import json
import pandas as pd
import os

class Zappos:

    def __init__(self, name,zipcode):
        self.name = name
        self.location = zipcode

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

zappos = Zappos("shoes", 61455)
data = zappos.search()
data_df = pd.DataFrame.from_dict(data)
names = zappos.extract_product_names(data)
images = zappos.extract_product_images(data)
prices = zappos.extract_product_prices(data)
links = zappos.extract_product_links(data)
print(prices)
