#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: utils.py
# Author: sgallon
# Date: 2020-10-27
# Description: 工具函数，请求头，爬虫主类


import requests
import json
from bs4 import BeautifulSoup

URL = "http://prts.wiki./w/"
HEADERS = {
    "Host": "prts.wiki",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,de-DE;q=0.8,de;q=0.7,ja-JP;q=0.6,ja;q=0.5,en-GB;q=0.4,en;q=0.3,zh-HK;q=0.2",
    "Cookie": "_ga=GA1.2.1812254634.1603692459; _gid=GA1.2.1505203890.1603692459; __gads=ID=3a7591e8027e2bd9-22d56a5266c40033:T=1603692459:RT=1603692459:S=ALNI_MaVbd-9glerHAF_vY2dK7UDP5CUkw; _gat_gtag_UA_158174062_1=1"
}

class PRTSSpider:
    """
    Spider for prts wiki
    """
    def __init__(self, page_name: str, url=URL):
        self.page_name = page_name
        self.url = url + page_name

    def get_html(self):
        response = requests.get(
            url = self.url,
            headers = HEADERS
        )
        self.response = response
        if response.status_code == 200:
            print("Spider gets 200 ok")
        else:
            print("Spider gets status code {}, please check.".format(response.status_code))

    def make_soup(self):
        self.soup = BeautifulSoup(self.response.text, 'html.parser')


def find_longest_child(bs_node: BeautifulSoup, tag_name="div", layer=1) -> BeautifulSoup:
    """
    获取当前BeautifulSoup节点 bs_node 的第 layer 代名称为 tag_name 的子节点
    """
    if layer == 0 or not bs_node:
        return bs_node
    maxlen = float("-inf")
    maxdiv = None
    for div in bs_node.find_all(tag_name):
        if len(str(div)) > maxlen:
            maxlen = len(str(div))
            maxdiv = div
    return find_longest_child(maxdiv, tag_name, layer-1)

