import pandas as pd
import numpy as np
import requests
import zillow


class ZillowAPI:

    def __init__(self):
        pass

    def get_headers():
        # Create headers
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'accept-encoding': 'gzip, deflate, sdch, br',
                   'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                   'cache-control': 'max-age=0',
                   'upgrade-insecure-requests': '1',
                   'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

        return headers

    def build_urls(self, key, street_address, city, state, postal_code=False):
        '''
        Description: Use basic data from BV database to create a url
        that will work for Zillow's API.

        Parameters: 
        - key: 
            - string 
            - zwsid necessary for Zillow API
        - api_type: 
            - string  
            - the type of api call/data that is intended to be gotten
            - Example - "GetChart"
        - street_address:
            - string
            - street number and street name for a property separated by spaces
        -city/state/postal:
            - strings
            - As expected

        Return:
            - string 
            - the functional url that will call appropriate data from the api
        '''
        base_url = 'https://www.zillow.com/webservice/GetDeepSearchResults.htm'

        # concatenate street address as needed
        street_address = '+'.join(street_address.split(' '))

        if not postal_code:
            # if no postal code provided just concatenate on citystate
            citystatezip = city + '%2C+' + state
        else:
            # if postal code is provided, use it
            citystatezip = city + '%2C+' + state + str(postal_code)

        return base_url + '?zws-id=' + key + '&address=' + street_address + '&citystatezip=' + citystatezip

    def build_chart_urls(self, key, property_id):
        '''
        Description: Use basic data from BV database to create a url
        that will work for Zillow's API.

        Parameters: 
        - key: 
            - string 
            - zwsid necessary for Zillow API
        - api_type: 
            - string  
            - the type of api call/data that is intended to be gotten
            - Example - "GetChart"
        - street_address:
            - string
            - street number and street name for a property separated by spaces
        -city/state/postal:
            - strings
            - As expected

        Return:
            - string 
            - the functional url that will call appropriate data from the api
        '''

        # Unit type needed for chart data to get dollar values instead of percents

        example = 'http://www.zillow.com/webservice/GetChart.htm?zws-id=<ZWSID>&unit-type=percent&zpid=48749425&width=300&height=150'

        unit_type = 'dollar'

        base_url = 'http://www.zillow.com/webservice/GetChart.htm'

        # concatenate street address as needed
        street_address = '+'.join(street_address.split(' '))

        if not postal_code:
            # if no postal code provided just concatenate on citystate
            citystatezip = city + '%2C+' + state
        else:
            # if postal code is provided, use it
            citystatezip = city + '%2C+' + state + str(postal_code)

        return base_url + '?zws-id=' + key + '&address=' + street_address + '&citystatezip=' + citystatezip

    def get_deep_search_results(url):
        '''
        Description: 
        Parameters:
        Return:
        '''

        pass


url = "https://www.zillow.com/webservice/GetDeepSearchResults.htm"
address = "2949 Chestnut Street"
city = 'Oakland'
state = 'CA'
postal_code = '94608'


with open("/Users/tylerpreston/bin/config/zillow_key.conf", 'r') as f:
    key = f.readline().strip()

params = {
    'zws-id': key,
    "citystatezip": "Oakland, CA 94608",
    "address": "2949 Chestnut Street"
}

# api = zillow.ValuationApi()

# data = api.GetSearchResults(key, address, postal_code)

# print(data)

api = ZillowAPI()

url = api.build_urls(key, address, city, state, postal_code)
print(url)
try:
    response = requests.get(url, params)

    # If the response was successful, no Exception will be raised
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
    print(f'Other error occurred: {err}')  # Python 3.6

print('Response content:\n{}\n\n'.format(response.content),
      'Response text:\n{}\n\n'.format(response.text),
      'Response encoding:\n{}\n\n'.format(response.encoding),
      'Response json:\n{}\n\n'.format(response.json)
      )
