#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-10-29 21:09:48
# Project: IMDB_NowPlaying

from pyspider.libs.base_handler import *
import codecs
import re

base_url = 'http://www.imdb.cn/nowplaying/'
start_page = 1
pages = 20000


class Handler(BaseHandler):
    crawl_config = {
        'headers' : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
    }
    
    def __init__(self):
        self.base_url = base_url
        self.start_page = start_page
        self.pages = pages

    @every(minutes=24 * 60)
    def on_start(self):
        while self.start_page <= pages:
            self.crawl(self.base_url + str(self.start_page), callback=self.extract_list)
            self.start_page += 1

    @config(age=10 * 24 * 60 * 60)
    def extract_list(self, response):
        with codecs.open(r'D:\Daniel World\Life\Personal\Coding\Python3\spider\IMDB.txt', 'a', 'utf-8') as file:
            for movie in response.doc('.ss-3 a').items():
                file.write(movie('.honghe-3 p').text() + '#')
                file.write(movie('span i').text() + '#')
                for detail in movie('.honghe-1 .clear p').items():
                    if not re.match('评分', detail.text()):
                        file.write(detail.text() + '#')
                file.write(movie.attr.href)
                file.write('\r\n')
