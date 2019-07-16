#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 23:24:55 2019

@author: amykim
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
enddate = dt.date(year=2013, month=7, day=16)

while not enddate == startdate:
    query = u'to%3Abts_twt%20filter%3Averified%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&src=typd'
    url = base_url + query
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    lastHeight = browser.execute_script("return document.body.scrollHeight")

body = browser.find_element_by_tag_name('body')

for _ in range(1):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)

tweets = browser.find_elements_by_class_name('tweet-text')

for tweet in tweets:
    print(str(tweet.text))
