import requests
import json
import pandas as pd

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
	                "X-RapidAPI-Key": "3abf378184msh3907cc74d161a65p11d50djsn4feb42e142fc",
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
        if data_df is None:
            return None

        product_names = {}
        for x in range(len(data)):
            product_names[x] = data[x]["productName"]
        return product_names


    # def extract_product_images(self, json_data):
    #     """
    #     Extracts the images of the products from the JSON data.

    #     Args:
    #     - json_data (dict): The JSON response from the eBay API.

    #     Returns:
    #     - product_images (dict): A dictionary where the keys are the positions and the values are the product images.
    #     - None: If the input JSON data is None.
    #     """
    #     if json_data is None:
    #         return None

    #     product_images = json_data[]
        

    #     return product_images

zappos = Zappos("shoes", 61455)
data = zappos.search()
data_df = pd.DataFrame.from_dict(data)
names = zappos.extract_product_names(data)
print(names)

    # def extract_product_prices(self, json_data):
    #     """
    #     Extracts the prices of the products from the JSON data.

    #     Args:
    #     - json_data (dict): The JSON response from the eBay API.

    #     Returns:
    #     - product_prices (dict): A dictionary where the keys are the positions and the values are the product prices.
    #     - None: If the input JSON data is None.
    #     """
    #     if json_data is None:
    #         return None

    #     product_prices = {}
    #     products = json_data['search_results']

    #     for item in products[:10]:
    #         price = item['price']['value']
    #         product_prices[item['position']] = price

    #     return product_prices

    # def extract_product_links(self,json_data):
    #     """
    #     Extracts the product links from the JSON data.

    #     Args:
    #     - json_data (dict): The JSON response from the eBay API.

    #     Returns:
    #     - product_links (dict): A dict of the links of the first 10 products.
    #     - None: If the input JSON data is None.
    #     """
    #     products = json_data['search_results']

    #     product_links = {}
    #     for item in products[:10]:  # Extract links from the first 10 products
    #         link = item["link"]
    #         product_links[item['position']] = link

    #     return product_links


# class ebay_deals:

#     def search(self):
#         # set up the request parameters
#         params = {
#             'api_key': '4628D7F6193C4219B168D3FE361ADB2F',
#             'type': 'deals',
#             'url': 'https://www.ebay.com/deals'
#         }

#         # make the http GET request to Countdown API
#         api_result = requests.get('https://api.countdownapi.com/request', params)

#         # print the JSON response from Countdown API
#         json_data = json.dumps(api_result.json())

#         return json_data

#     def extract_deal_info(self, json_data):
#         """
#         Extracts information about the first 10 items from the 'deals_results' in the JSON data.

#         Args:
#         - json_data (dict): The JSON response from the eBay API.

#         Returns:
#         - deal_info (list): A list of dictionaries containing the extracted information for each item.
#         """
#         if json_data is None:
#             return None

#         data = json.loads(json_data)
#         deals_results = data["deals_results"]

#         deal_info = []
#         for result in deals_results[:10]:
#             item_info = {
#                 "name": result["title"],
#                 "previous_price": result["was_price"]["raw"],
#                 "current_price": result["price"]["raw"],
#                 "link": result["link"],
#                 "image": result["image"]
#             }
#             deal_info.append(item_info)

#         return deal_info


# ebay = Ebay("iphone","61455")
# json_data = ebay.search()

# product_prices = ebay.extract_product_prices(json_data)
# product_names = ebay.extract_product_names(json_data)
# product_images = ebay.extract_product_images(json_data)


# print("Product Names:", product_names)
# print("Product Prices:", product_prices)
# print("Product Images:", product_images)