#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: get_agent_list.py
# Author: sgallon
# Date: 2020-10-26
# Description: 爬取prts.wiki上的干员一览表，存储为json格式

import json
import os.path
from utils import PRTSSpider, find_longest_child
#from urllib.parse import quote, unquote

SAVE_JSON_PATH = "./data/arknights_agent_list.json"
SAVE_TXT_PATH = "./data/arknights_agent_list.txt"

def get_agent_list() -> list:
    # 干员一览页面需要特殊处理，来获得干员页面列表
    agent_list_spider = PRTSSpider(page_name="干员一览")
    agent_list_spider.get_html()
    agent_list_spider.make_soup()
    # 通过查看html源代码发现干员表格在document的第五代子节点
    # 先获得最长（字符串最长）的第四代子节点
    tmp_soup = find_longest_child(agent_list_spider.soup, tag_name="div", layer=4)
    #agent_list = [child for child in list(tmp_soup.children) if child.get("class") == "smwdata"] #循环体中没法用get
    #agent_list = [child for child in list(tmp_soup.children) if "smwdata" in str(child)]
    agent_list = tmp_soup.select('div[class="smwdata"]')
    return agent_list

   
def save_agent_list(agent_list: list, save_json_path = SAVE_JSON_PATH, save_txt_path = SAVE_TXT_PATH):
    """
    Data example for a in agent_list:
    a = <div class="smwdata" data-adapt="标准" data-approach="公开招募" data-birthplace="东" data-camp="罗德岛" data-class="重装" data-cn="黑角" data-des="罗德岛重装干员黑角，将为队友提供坚实的防御力量。" data-en="Noir Corne" data-feature="能够阻挡三个敌人" data-flex="普通" data-half="http://prts.wiki/images/thumb/6/6c/%E5%8D%8A%E8%BA%AB%E5%83%8F_%E9%BB%91%E8%A7%92_1.png/110px-%E5%8D%8A%E8%BA%AB%E5%83%8F_%E9%BB%91%E8%A7%92_1.png" data-icon="http://prts.wiki/images/f/f1/%E5%A4%B4%E5%83%8F_%E9%BB%91%E8%A7%92.png" data-index="A43" data-jp="ノイルホーン" data-moredes="每天都能看见他仔细擦拭面具的身影。" data-ori-atk="180" data-ori-block="3" data-ori-cd="1.2s" data-ori-dc="14" data-ori-def="220" data-ori-dt="70s" data-ori-hp="1219" data-ori-res="0" data-plan="普通" data-position="近战位" data-race="鬼" data-rarity="1" data-sex="男" data-skill="普通" data-sort_id="4" data-str="标准" data-tag="新手" data-team="行动组A4" data-tolerance="优良"></div>
    a.attrs = {'class': ['smwdata'], 'data-cn': '黑角', 'data-position': '近战位', 'data-en': 'Noir Corne', 'data-sex': '男', 'data-tag': '新手', 'data-race': '鬼', 'data-rarity': '1', 'data-class': '重装', 'data-approach': '公开招募', 'data-camp': '罗德岛', 'data-team': '行动组A4', 'data-des': '罗德岛重装干员黑角，将为队友提供坚实的防御力量。', 'data-feature': '能够阻挡三个敌人', 'data-str': '标准', 'data-flex': '普通', 'data-tolerance': '优良', 'data-plan': '普通', 'data-skill': '普通', 'data-adapt': '标准', 'data-moredes': '每天都能看见他仔细擦拭面具的身影。', 'data-icon': 'http://prts.wiki/images/f/f1/%E5%A4%B4%E5%83%8F_%E9%BB%91%E8%A7%92.png', 'data-half': 'http://prts.wiki/images/thumb/6/6c/%E5%8D%8A%E8%BA%AB%E5%83%8F_%E9%BB%91%E8%A7%92_1.png/110px-%E5%8D%8A%E8%BA%AB%E5%83%8F_%E9%BB%91%E8%A7%92_1.png', 'data-ori-hp': '1219', 'data-ori-atk': '180', 'data-ori-def': '220', 'data-ori-res': '0', 'data-ori-dt': '70s', 'data-ori-dc': '14', 'data-ori-block': '3', 'data-ori-cd': '1.2s', 'data-index': 'A43', 'data-sort_id': '4', 'data-jp': 'ノイルホーン', 'data-birthplace': '东'}
    """
    dict_lst = [a.attrs for a in agent_list] #a.attrs
    json_str = json.dumps(dict_lst, indent=4, separators=[',',':'], ensure_ascii=False)
    with open(save_json_path, 'w') as handler:
        handler.write(json_str)
    with open(save_txt_path, 'w') as handler:
        for agent_dict in dict_lst:
            agent_name = agent_dict.get('data-cn')
            if agent_name:
                handler.write(agent_name)
                handler.write('\n')


if __name__ == "__main__":
    agent_list = get_agent_list()
    save_agent_list(agent_list, SAVE_JSON_PATH)
    print('Done! Result json file saved to {}\nResult txt file saved to {}'.format(
        os.path.abspath(SAVE_JSON_PATH),
        os.path.abspath(SAVE_TXT_PATH)
    ))

