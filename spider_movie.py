#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-10-24 22:07:17
# Project: movie

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.fname = ''
        self.name = ''
        self.year = ''
        self.country = ''
        self.category = ''
        self.language = ''
        self.subtitle = ''
        self.douban = ''
        self.imdb = ''
        self.size = ''
        self.duration = ''
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.dygod.net/html/gndy/dyzz/index.html', callback=self.index_page)

    @config(age=3 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://www.dygod.net/html/gndy/dyzz/\d+/\d+.html', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('div.x').items('a'):
            if each.text() == '下一页':
                self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        self.fname = ''
        self.name = ''
        self.year = ''
        self.country = ''
        self.category = ''
        self.language = ''
        self.subtitle = ''
        self.douban = ''
        self.imdb = ''
        self.size = ''
        self.duration = ''
        for item in response.doc('#Zoom').items('p'):
            if re.match('◎译  名', item.text().replace('\u3000', ' ')):
                self.fname = item.text().replace('\u3000', ' ').replace('◎译  名', '').strip()
            elif re.match('◎片  名', item.text().replace('\u3000', ' ')):
                self.name = item.text().replace('\u3000', ' ').replace('◎片  名', '').strip()
            elif re.match('◎年  代', item.text().replace('\u3000', ' ')):
                self.year = item.text().replace('\u3000', ' ').replace('◎年  代', '').strip()
            elif re.match('◎国  家', item.text().replace('\u3000', ' ')):
                self.country = item.text().replace('\u3000', ' ').replace('◎国  家', '').strip()
            elif re.match('◎类  别', item.text().replace('\u3000', ' ')):
                self.category = item.text().replace('\u3000', ' ').replace('◎类  别', '').strip()
            elif re.match('◎语  言', item.text().replace('\u3000', ' ')):
                self.language = item.text().replace('\u3000', ' ').replace('◎语  言', '').strip()
            elif re.match('◎字  幕', item.text().replace('\u3000', ' ')):
                self.subtitle = item.text().replace('\u3000', ' ').replace('◎字  幕', '').strip()
            elif re.match('◎豆瓣评分', item.text().replace('\u3000', ' ')):
                self.douban = item.text().replace('\u3000', ' ').replace('◎豆瓣评分', '').strip()
            elif re.match('◎IMDb评分', item.text().replace('\u3000', ' ')):
                self.imdb = item.text().replace('\u3000', ' ').replace('◎IMDb评分', '').strip()            
            elif re.match('◎文件大小', item.text().replace('\u3000', ' ')):
                self.size = item.text().replace('\u3000', ' ').replace('◎文件大小', '').strip()
            elif re.match('◎片  长', item.text().replace('\u3000', ' ')):
                self.duration = item.text().replace('\u3000', ' ').replace('◎片  长', '').strip()
            else:
                pass
        return {
            "title": response.doc('title').text(),
            'link': response.doc('#Zoom a').text(),
            'fname': self.fname,
            'name': self.name,
            'year': self.year,
            'country': self.country,
            'category': self.category,
            'language': self.language,
            'subtitle': self.subtitle,
            'douban': self.douban,
            'imdb': self.imdb,
            'size': self.size,
            'duration': self.duration,
        }
