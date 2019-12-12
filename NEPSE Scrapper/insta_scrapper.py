from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import pickle 


username='nepaltourism'
# browser = webdriver.Chrome('/usr/local/bin/chromedriver')
browser = webdriver.Firefox()
browser.get('https://www.instagram.com/'+username+'/?hl=en')
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


links=[]
# source = browser.page_source
# data=bs(source, 'html.parser')
# body = data.find('body')
# script = body.find('span')
# for link in script.findAll('a'):
#      if re.match("/p", link.get('href')):
#         links.append('https://www.instagram.com'+link.get('href'))


# print('Links')
# print(links)

i = 0

#sleep time is required. If you don't use this Instagram may interrupt the script and doesn't scroll through pages
while len(np.unique(links)) <= 1310 and i <= 200:
    # time.sleep(5) 
    # Pagelength = browser.execute_script("window.scrollTo(document.body.scrollHeight/1.5, document.body.scrollHeight/3.0);")
    source = browser.page_source
    data=bs(source, 'html.parser')
    body = data.find('body')
    script = body.find('span')
    for link in script.findAll('a'):
        if re.match("/p", link.get('href')):
            links.append('https://www.instagram.com'+link.get('href'))

    print('Total links collected: ', len(np.unique(links)) , ' Loop number:', i)
    scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
    browser.execute_script(scroll_down)
    time.sleep(10)
    i += 1


links = list(set(links))

# Writing the file
with open('link_list.txt', 'w') as f:
    for item in links:
        f.write("%s\n" % item)


print('File written')

# compiling links to dataframe
result = pd.DataFrame()
for i in range(len(links)):
    try:
        page = urlopen(links[i]).read()
        data=bs(page, 'html.parser')
        body = data.find('body')
        script = body.find('script')
        raw = script.text.strip().replace('window._sharedData =', '').replace(';', '')
        json_data=json.loads(raw)
        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts= json.dumps(posts)
        posts = json.loads(posts)
        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns') 
        x.columns =  x.columns.str.replace("shortcode_media.", "")
        result=result.append(x)
       
    except:
        np.nan
# Just check for the duplicates
result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))



import os
import requests
result.index = range(len(result.index))
directory="photos/"
for i in range(len(result)):
    r = requests.get(result['display_url'][i])
    with open(directory+result['shortcode'][i]+".jpg", 'wb') as f:
        f.write(r.content)
