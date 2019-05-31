import os
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import numpy as np
import pandas as pd
import random


def set_up_selenium():
    chromedriver = "/Users/tylerpreston/bin/chromedriver"  # path to the chromedriver executable
    chromedriver = os.path.expanduser(chromedriver)
    sys.path.append(chromedriver)
    driver = webdriver.Chrome(chromedriver)
    return driver


# get betterview data from csv file
bv_data = pd.read_csv('bv_property_features.csv')
addresses = bv_data.full_address.unique()
addresses = addresses[:29]
addresses = ['1872 Winchester Trail, Atlanta, GA 30341', '711 Corlett Drive, Huntsville, AL, 35802', '933 Apgar Street, Oakland, CA 94608']

# initializations
driver = set_up_selenium()
property_id = 1
property_list = []
url = 'https://www.realtor.com/'

# loop through all addresses in list to navigate to address page
for address in addresses:
    property_dictionary = {}

    driver.get(url)
    element = driver.find_element_by_id('rdc-main-search-nav-hero-input')
    element.clear()
    time.sleep(np.random.exponential() * .2)

    # use loop to allow for slowly typing the search string to throw off bot detection
    search_string = address.lower()
    for letter in search_string:
        element.send_keys(letter)
        time.sleep(np.random.exponential() * .1)
    time.sleep(np.random.exponential() * .4)
    element.send_keys(Keys.RETURN)

    # wait for realtor to put the necessary info into the page_source data
    x = 0
    while 'avm_trend' not in driver.page_source:
        time.sleep(2)
        x += 1
        if x > 20:
            print('breaking')
            break

    # pull page_source data with Beautiful Soup and save all scripts
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    scripts = soup.find_all("script")
    try:
        scraped_address = soup.find(id='ldp-address').get('content')
    except:
        scraped_address = 'null'

    # Scripts are not organized/structured, so we are manually searching them for
    # the desired data
    for script in scripts:
        script = str(script)
        if 'avm_trend' in script:
            index = script.find('avm_trend')
            script = script[index: len(script)]
            start_index = script.find('{')
            stop_index = script.find('}') + 1
            print(script[start_index:stop_index])
            estimate_history = json.loads(script[start_index:stop_index])['history']
            break
        else:
            estimate_history = 'null'

    property_dictionary['property_id'] = property_id
    property_dictionary['scraped_address'] = scraped_address
    property_dictionary['estimate_history'] = estimate_history
    property_dictionary['bv_address'] = address
    property_list.append(property_dictionary)
    property_id += 1

driver.close()
print(property_list)

# trying to select and copy all with keybboard shortcuts
# actions.key_down(Keys.COMMAND).send_keys('a').send_keys('c').key_up(Keys.COMMAND).perform()

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# search_input = soup.find_all('input', class_='react-autosuggest__input Input-sc-7nzn9k-0 dIKGyt')
# print(search_input)
