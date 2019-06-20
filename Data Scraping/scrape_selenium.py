# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 20:04:41 2017

@author: Sanjivani Patil
"""

import time
import pandas as pd
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')

query_tag = "womeninstem"
#base_url = u'https://twitter.com/search?src=typd&q=%23equalpay'
base_url = u'https://twitter.com/search?q=womeninstem&src=typd'
browser.get(base_url)
time.sleep(1)

body = browser.find_element_by_tag_name('body')

#for i in range(0 , 5):
#    body.send_keys(Keys.PAGE_DOWN)
#    time.sleep(0.2)
browser.maximize_window()
Y=1000
df = pd.DataFrame(columns = ["Tweet_text"])

for num in range(1,100):
    browser.execute_script("window.scrollTo(0, " + str(Y) + ")")
    Y=Y+10
    time.sleep(0.5)
    tweets = browser.find_elements_by_class_name('tweet-text')
    for tweet in tweets:
      new_tweet = pd.Series([tweet.text])
      df = df.append(new_tweet, ignore_index=True)
      #print(tweet.text)
browser.quit() 
with open(query_tag+".csv", 'w') as fh:
    df.to_csv(fh)
