import http.client
import time
import pandas as pd
import numpy as np
import json


def get_property_detail(street, city, state, postal, key, conn, headers):
    address1 = ('%20').join(street.split())
    address2 = ('%20').join([city, state, postal])
    end_url = '/propertyapi/v1.0.0/property/detail?address1='\
        + address1 + "&address2=" + address2

    conn.request("GET", end_url, headers=headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode('utf-8'))
    return data


def get_sales_history_by_address(street, city, state, postal, key, conn, headers):
    address1 = ('%20').join(street.split())
    address2 = ('%20').join((city + ' ' + state + ' ' + postal).split())
    end_url = '/propertyapi/v1.0.0/saleshistory/detail?address1='\
        + address1 + "&address2=" + address2

    conn.request("GET", end_url, headers=headers)

    res = conn.getresponse()
    sales_data = json.loads(res.read().decode('utf-8'))

    if sales_data['status']['code'] == 0:
        sales_data = sales_data['property'][0]['salehistory']
    else:
        sales_data = []
    return sales_data


def get_relevant_sale(sales_data, date):
    for sale in sales_data:
        try:
            sale_date = date_to_epoch(sale['amount']['salerecdate'])
        except:
            try:
                sale_date = date_to_epoch(sale['saleTransDate'])
            except:
                continue
        sale_amount = sale['amount']['saleamt']
        if sale_date > date and sale_amount > 0:
            return (sale_date, sale_amount)
    return ('null', 'null')


def date_to_epoch(date):
    if len(date) < 11:
        pattern = '%Y-%m-%d'
    else:
        date = date[0:10]
        pattern = '%Y-%m-%d'
    return int(time.mktime(time.strptime(date, pattern)))


def append_portfolio_sales_history(df):
    # Obtain Attom API key from secure location
    with open("/Users/tylerpreston/bin/config/attom_key.conf", 'r') as f:
        key = f.readline().strip()

    # Set up connection to the Attom API
    conn = http.client.HTTPSConnection("search.onboard-apis.com")
    headers = {
        'accept': "application/json",
        'apikey': key,
    }

    all_sales = []
    relevant_sale_dates = []
    relevant_sale_amounts = []

    for label, row in df.iterrows():
        street, city, state, postal = row.street, row.city, row.state, row.zip
        date = date_to_epoch(row.roof_data_date)
        sales_data = get_sales_history_by_address(street, city, state, postal, key, conn, headers)
        relevant_sale = get_relevant_sale(sales_data, date)
        relevant_sale_dates.append(relevant_sale[0])
        relevant_sale_amounts.append(relevant_sale[1])
        all_sales.append(sales_data)
        time.sleep(.2)

    conn.close()
    df['all_sales'] = pd.Series(all_sales)
    df['relevant_sale_date'] = pd.Series(relevant_sale_dates)
    df['relevant_sale_amount'] = pd.Series(relevant_sale_amounts)
    return df
