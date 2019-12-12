from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import pickle 
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
url_link = 'http://nepalstockinfo.com/nepse-index'
browser.get(url_link)
print('Connected to the website')

# '1994-12-08' is the oldest date that can be entered in the sheet
input_form_date = browser.find_elements_by_xpath("//input[@id='from_date']")[0]
input_form_date.send_keys('1994-12-08');

# click submit button
submit_button = browser.find_elements_by_xpath('//*[@id="submitBtn"]')[0]
submit_button.click()

# list all the entries in a single page
browser.find_element_by_xpath("//select[@name='example_datatable_length']/option[text()='-1']").click()

# getting the page
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')

print('Data Scraping Started!!')
# getting the table
script_table = body.find('table')

# getting headers
headers = []
script_table_header = script_table.find('thead')
for header in script_table.findAll('th'):
    headers.append(header.get_text())

# getting data
data_table = []
data_rows = []
for row in script_table.findAll('tr'):
    data_row = []
    for datum in row.findAll('td'):
        val = datum.get_text()
        val = val.replace(',', '')
        if val:
            data_row.append(val)
        else:
            data_row.append('nan')

    data_table.append(data_row)
print('Data Scrapped from website!!')

# Writing data to files
print('Writing data to CSV file!!')
with open('data.csv', 'w') as f:
    # writing headers
    f.write("{0}\n".format(','.join(headers)))

    # writing datapoints
    for data_row in data_table:
        f.write('{0}\n'.format(','.join(data_row)))
print('Writing data completed!!')

