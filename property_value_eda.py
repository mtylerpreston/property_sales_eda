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
import atom_api


# Read in raw data
bv_data = pd.read_csv('bv_property_features.csv')

# Sort by date data was generated then remove records with duplicate addresses
# Keep only the oldest record to give us a better chance at a relevant sale record
bv_data.sort_values('roof_data_date', ascending=True, inplace=True)
bv_data.drop_duplicates(subset='full_address', keep='first', inplace=True)

# Remove rows with bad address data
bv_data.dropna(axis=0, how='any', inplace=True)

# Reset index because OCD
bv_data.reset_index(inplace=True, drop=True)

# Take a small sample for testing, toggle this with to comment for production
bv_data = bv_data.iloc[:100, :]

# Append relevant sales history from API Calls to Atom
bv_data = atom_api.append_portfolio_sales_history(bv_data)

# Write results to a .csv file for safe keeping
bv_data.to_csv(r'/Users/tylerpreston/galvanize/capstone/\
    property_sales_eda/export_df.csv', index=False)
