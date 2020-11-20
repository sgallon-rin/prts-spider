#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: get_agent_info.py
# Author: sgallon
# Date: 2020-10-27
# Description: 根据get_agent_list.py爬取的json干员一览表，
# 更改已有字段名称，并爬取干员对应的页面上的信息，
# 包括干员头像、半身像、档案资料、台词（含语音）等信息

import json
import os, os.path
import requests
import random
from collections import defaultdict
from tqdm import tqdm
from utils import PRTSSpider, HEADERS

LOAD_JSON_PATH = "./data/arknights_agent_list.json"
SAVE_JSON_PATH = "./data/arknights_agent_description.json"
IMG_DIR = "./img/"
VOICE_DIR = "./voice/"

#爬取的json字段与实际意义的转换字典，忽略了初始
KEYS_DICT = {
    "data-cn":"name",
    "data-position":"position",
    "data-en":"name-en",
    "data-sex":"sex",
    "data-tag":"tag",
    "data-race":"race",
    "data-rarity":"rarity",
    "data-class":"class",
    "data-approach":"approach",
    "data-camp":"camp",
    "data-team":"team",
    "data-des":"des",
    "data-feature":"feature",
    "data-str":"str",
    "data-flex":"flex",
    "data-tolerance":"tolerance",
    "data-plan":"plan",
    "data-skill":"skill",
    "data-adapt":"adapt",
    "data-moredes":"more-des",
    "data-icon":"icon",
    "data-half":"half-icon",
    "data-ori-hp":"ori-hp",
    "data-ori-atk":"ori-atk",
    "data-ori-def":"ori-def",
    "data-ori-res":"ori-res",
    "data-ori-dt":"ori-dt",
    "data-ori-dc":"ori-dc",
    "data-ori-block":"ori-block",
    "data-ori-cd":"ori-cd",
    "data-index":"index",
    "data-sort_id":"sort-id",
    "data-jp":"name-jp",
    "data-birthplace":"birthplace"
}

def get_url_type(url: str) -> str:
    return url.split('/')[-1].split('.')[-1]

def save_from_url(url: str, img_name: str, img_dir=IMG_DIR, headers=HEADERS):
    filetype = get_url_type(url)
    save_path = img_dir + img_name + '.' + filetype
    if os.path.exists(save_path):
        print("File {} already exists.".format(save_path))
    else:
        response = requests.get(url, headers)
        if response.status_code == 200:
            with open(save_path, 'wb') as handler:
                handler.write(response.content)
            print("Spider 200 ok. File saved to {}".format(os.path.abspath(save_path)))
        else:
            print("Spider gets status code {}, please check.".format(response.status_code))

def get_agent_file(bs_list, kw="基础档案"):
    """
    html解析用，截取BeautifulSoup中关键字字段之后的内容
    """
    for i, bs in enumerate(bs_list):
        if kw in str(bs):
            result = bs_list[i::]
            break
    return result


class AgentSpider(PRTSSpider):
    """
    Agent information spider for prts wiki
    """
    def __init__(self, agent_dict: dict):
        self.info_dict = defaultdict(str)
        self.transform_agent_dict(agent_dict)
        super().__init__(page_name=self.get_name())

    def transform_agent_dict(self, agent_dict):
        # 转换agent_dict的字典键名称
        for agent_key, info_key in KEYS_DICT.items():
            self.info_dict[info_key] = agent_dict.get(agent_key)

    def get_name(self):
        # 获取干员名字（代号）
        n = self.info_dict.get('name')
        if n:
            return n
        else:
            raise KeyError("Failed to get name!")

    def get_icon(self):
        n = self.get_name()
        icon_link = self.info_dict.get('icon')
        half_link = self.info_dict.get('half-icon')
        if icon_link:
            save_from_url(icon_link, n+'_icon')
        else:
            print("No icon for {}.".format(n))
        if half_link:
            save_from_url(half_link, n+'_half')
        else:
            print("No half icon for {}.".format(n))

    def analyze_html(self, save_icon=False, save_voice=False):
        self.get_html()
        self.make_soup()
        if save_icon:
            self.get_icon()
        #self.get_charimg()
        self.get_cv_il()
        #self.get_battle_data()
        self.get_token()
        #self.get_potential()
        self.get_file()
        self.get_lines(save_voice=save_voice)

    def get_charimg(self):
        # TODO: 保存角色立绘，不同精英化阶段、皮肤
        raise NotImplementedError
        try:
            charimg_soup_lst = self.soup.select('div[class="charimg-wrapper anicss"]')
        except:
            print("Error in getting char img for {}.", self.info_dict['name'])

    def get_cv_il(self):
        # 获取声优、画师
        try:
            cv_soup = self.soup.select('div[class="charleft"]')[0]
            cv = cv_soup.select('div[class="cv-content"]')[0].string
            il = cv_soup.select('div[class="painter-content"]')[0].string
            self.info_dict['cv'] = cv
            self.info_dict['painter'] = il
        except:
            print("Error in getting cv/illust info for {}.", self.info_dict['name'])

    def get_battle_data(self):
        # TODO: 获取战斗数值，天赋等
        # wikitable logo还包含基建技能等，故不同干员长度不同
        raise NotImplementedError
        try:
            battle_soup = self.soup.select('table[class="wikitable logo"]')[1]
            talent_soup = self.soup.select('table[class="wikitable logo"]')[2]
        except:
            print("Error in getting battle data for {}.", self.info_dict['name'])

    def get_token(self):
        # 获取干员简历和信物描述（四句话）
        try:
            token_soup_lst = self.soup.select('table[class="wikitable logo"]')[-1].find_all('p')
            token_description = list(p.string for p in token_soup_lst)
            self.info_dict['token-description'] = '\t'.join(token_description)
        except:
            print("Error in getting token description info for {}.", self.info_dict['name'])

    def get_potential(self):
        # TODO: 获取潜能提升信息？潜能和技能升级材料混在一起，暂时不处理
        raise NotImplementedError
        try:
            potential_soup = self.soup.select('table[class="wikitable nomobile logo"]')[0]
        except:
            print("Error in getting potential info for {}.", self.info_dict['name'])

    def get_file(self):
        # 获取干员档案
        try:
            file_soup_lst = self.soup.select('div[class="poem"]')
            file_soup_lst = get_agent_file(file_soup_lst, kw="基础档案")
            file_text_lst = [t.p.text for t in file_soup_lst]
            self.info_dict['file'] = '\t'.join(file_text_lst)
        except:
            print("Error in getting agent file for {}.", self.info_dict['name'])

    def get_lines(self, save_voice=False):
        # 获取干员台词
        try:
            line_soup = self.soup.select('table[class="wikitable mw-collapsible mw-collapsed nomobile"]')[0]
            line_key_list = line_soup.select('th[style="width:120px;"]')
            line_value_list = line_soup.select('p')
            line_key_list = [item.b.text for item in line_key_list]
            tmp = []
            for item in line_value_list:
                if item.string:
                    tmp.append(item.string)
                else:
                    item.b.clear()
                    tmp.append(item.text)
            line_value_list = tmp
            self.info_dict['lines'] = dict(zip(line_key_list, line_value_list))
            if save_voice:
                line_source_list = line_soup.select('source')
                line_source_list = [item['src'] for item in line_source_list]
                assert len(line_key_list) == len(line_value_list) == len(line_source_list), "line list length not equal"
                n = self.get_name()
                vo_dir = VOICE_DIR + n + '/'
                if not os.path.exists(vo_dir):
                    os.makedirs(vo_dir)
                for i in range(len(line_key_list)):
                    vo_name = line_key_list[i]
                    vo_url = line_source_list[i]
                    save_from_url(url=vo_url, img_name=vo_name, img_dir=vo_dir)
        except:
            print(len(line_key_list) == len(line_value_list))
            print("Error in getting agent lines for {}.", self.info_dict['name'])


def get_agent_info_single(agent_dict, save_icon=False, save_voice=False):
    agent_spider = AgentSpider(agent_dict=agent_dict)
    agent_spider.analyze_html(save_icon=save_icon, save_voice=save_voice)
    print("Spider done for agent {}".format(agent_spider.get_name()))
    return agent_spider.info_dict

def main(save_icon=False, save_voice=False):
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    with open(LOAD_JSON_PATH, 'r') as handler:
        agent_list = json.load(handler)
    result = []
    for agent_dict in tqdm(agent_list):
        try:
            agent_info_dict = get_agent_info_single(agent_dict, save_icon=save_icon, save_voice=save_voice)
            result.append(agent_info_dict)
        except:
            print("Something went wrong! Skip and continue.")
            print(agent_dict)
    result = json.dumps(result, indent=4, separators=[',',':'], ensure_ascii=False)
    with open(SAVE_JSON_PATH, 'w') as handler:
        handler.write(result)
        print("Done! Result file saved to {}".format(os.path.abspath(SAVE_JSON_PATH)))
    """
    with open(SAVE_JSON_PATH, 'w') as handler:
        handler.write('[\n')
        L = len(agent_list)
        for i, agent_dict in enumerate(agent_list):
            agent_info_dict = get_agent_info_single(agent_dict)
            result = json.dumps(agent_info_dict, indent=4, separators=[',',':'], ensure_ascii=False)
            handler.write(result)
            if i != L-1:
                handler.write(',\n')
            else:
                handler.write('\n]')
        print("Done! Result file saved to {}".format(os.path.abspath(SAVE_JSON_PATH)))
    """
   
def test(k=5, save_icon=False, save_voice=False):
    if not os.path.exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    if not os.path.exists(VOICE_DIR):
        os.makedirs(VOICE_DIR)
    with open(LOAD_JSON_PATH, 'r') as handler:
        agent_list = json.load(handler)
    result = []
    agent_list = random.choices(agent_list, k=k)
    for agent_dict in tqdm(agent_list):
        try:
            agent_info_dict = get_agent_info_single(agent_dict, save_icon=save_icon, save_voice=save_voice)
            result.append(agent_info_dict)
        except:
            print("Something went wrong! Skip and continue.")
            #print(agent_dict)
    result = json.dumps(result, indent=4, separators=[',',':'], ensure_ascii=False)
    #print(result)
    with open('./data/test.json', 'w') as handler:
        handler.write(result)
        print("Done! Result file saved to {}".format(os.path.abspath('./data/test.json')))
    """
    with open('./data/test.json', 'w') as handler:
        handler.write('[\n')
        agent_list = random.choices(agent_list, k=5)
        L = len(agent_list)
        for i, agent_dict in enumerate(agent_list):
            agent_info_dict = get_agent_info_single(agent_dict)
            result = json.dumps(agent_info_dict, indent=4, separators=[',',':'], ensure_ascii=False)
            handler.write(result)
            if i != L-1:
                handler.write(',\n')
            else:
                handler.write('\n]')
        print("Done! Result file saved to {}".format(os.path.abspath('./data/test.json')))
    """


if __name__ == "__main__":
    main(save_icon=True, save_voice=True)
    #test(k=5, save_icon=False, save_voice=False)