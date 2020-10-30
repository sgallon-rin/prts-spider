#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: get_agent_info.py
# Author: sgallon
# Date: 2020-10-29
# Description: 对爬取的json文件干员信息进行重构，得到文本内容。结果文件以\t分隔句子，前两列为编号、姓名。

import json
import os.path

LOAD_JSON_PATH = "./data/0_arknights_agent_description.json"
SAVE_TXT_PATH = "./data/arknights_description_text.txt"

def reform(agent_dict):
    result = []
    na = agent_dict.get('name')
    description = agent_dict.get('token-description')
    file = agent_dict.get('file')
    #lines = agent_dict.get('lines')
    #if not description or not file or not lines:
    if not na or not description or not file:
        print("Missing information for {}. Skip to nest.".format(agent_dict.get('name')))
    else:
        result.append(na)
        description = description.split('\t')
        #print(description)
        if len(description) == 4:
            _ = description.pop(2)
        result.extend(description)
        file = file.split('\t')
        for sent in file:
            s = sent.split('\n')
            for ss in s:
                if "【" not in ss and len(ss)>10:
                    result.append(ss)
        # TODO: 台词（暂不需要）
        #for key, value in lines.items():
    return result

def main():
    with open(LOAD_JSON_PATH, 'r') as handler:
        agent_list = json.load(handler)
    L = len(agent_list)
    with open(SAVE_TXT_PATH, 'w') as handler:
        for i in range(L):
            handler.write("{}\t".format(i+1))
            result = '\t'.join(reform(agent_list[i]))
            handler.write(result)
            handler.write('\n')
    print("Done! Result file saved to {}".format(os.path.abspath(SAVE_TXT_PATH)))
    

if __name__ == "__main__":
    main()


