#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 23:24:55 2019

@author: amykim
@based on https://bit.ly/2Fztdhk

"""

import requests

import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import datetime as dt

browser = webdriver.Chrome()
base_url = u'https://twitter.com/search?q='

startdate = dt.date(year=2013, month=6, day=13)
untildate = dt.date(year=2013, month=6, day=14)
enddate = dt.date(year=2013, month=12, day=31)

totalfreq=[]

while not enddate == startdate:
    # query = u'to%3Abts_twt%20filter%3Averified%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&src=typd'
    query = u'to%3Abts_twt%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&src=typd'
    url = base_url + query
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    lastHeight = browser.execute_script("return document.body.scrollHeight")

    while True:
            dailyfreq={'Date':startdate}
            tweetbundle = {}
            wordfreq=0

            tweets = soup.find_all("p", {"class": "TweetTextSize"})
            # print(type(tweets))
            # handles = soup.find_all("a", {"class": "account-group js-account-group js-action-profile js-user-profile-link js-nav"})
            # print(len(handles))

            wordfreq+=len(tweets)

            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            newHeight = browser.execute_script("return document.body.scrollHeight")
#            print(newHeight)
            if newHeight != lastHeight:
                html = browser.page_source
                soup = BeautifulSoup(html,'html.parser')
                tweets = soup.find_all("p", {"class": "TweetTextSize"})
                # handles = soup.find_all("a", {"class": "account-group js-account-group js-action-profile js-user-profile-link js-nav"})
                wordfreq=len(tweets)
            else:
                dailyfreq['Frequency']=wordfreq

                # for i in range(len(handles)):
                    # tweetbundle[handles[i]] = tweets[i]

                # dailyfreq['Tweets'] = tweetbundle

                wordfreq=0
                totalfreq.append(dailyfreq)
                startdate=untildate
                untildate+=dt.timedelta(days=1)
                dailyfreq={}
                break
    #         i+=1
            lastHeight = newHeight

# printing as a graph

import pandas as pd
df=pd.DataFrame(totalfreq)
# df.to_excel("bts_twt-tweets.xlsx")
df.to_excel("bts_twt-tweets-total.xlsx", sheet_name = '2013')

import matplotlib.pyplot as plt
plt.figure(figsize=(20,10))
plt.xticks(rotation=90)
plt.plot(df.Date, df.Frequency, 'bo')
plt.show()
