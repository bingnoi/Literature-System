#!/usr/bin/python3
# 匹配 作者-单位 （比较准确的作者-单位匹配）
import pymysql
import pandas as pd
import re

def getAuthor_School(data):
    # 存储作者-单位
    author_school = []
    # print(data[3][:])
    # ('王常武,孔令富,韩佩富,赵立强', '燕山大学信息科学与工程学院!秦皇岛   066004,河北农业技术师院基础部!河北昌黎 066600')
    for j in range(len(data)):
        author = data[j][0].split(',')
        if ',' in data[j][1]:
            # 处理单位数不唯一情况
            school = data[j][1].split(',')
            if len(author) > len(school):
                # 作者数大于学校数
                for i in range(len(author)):
                    if '!' in school[0]:
                        author_school.append([author[i], re.findall(r'(.+?)!', school[0])[0]])
                    else:
                        author_school.append([author[i], school[0]])
            else:
                # 作者数小于等于学校数
                for i in range(len(author)):
                    if '!' in school[i]:
                        # 有的单位名称中不存在！
                        author_school.append([author[i], re.findall(r'(.+?)!', school[i])[0]])
                    else:
                        author_school.append([author[i], school[i]])
        else:
            # 处理多个作者一个单位情况
            school = data[j][1]
            for i in range(len(author)):
                if '!' in school:
                    author_school.append([author[i], re.findall(r'(.+?)!', school)[0]])
                else:
                    author_school.append([author[i], school])
    columns = ["author", "school"]
    index_id = []
    # 存储重复元素下标
    remove_list = []
    # 判断是否重复
    for i in range(0, len(author_school)):
        for j in range((i + 1), len(author_school)):
            if author_school[i] == author_school[j]:
                remove_list.append(j)
    # 去除重复元素（重名作者在这里去除，重名不重单位）
    author_school = [author_school[i] for i in range(len(author_school)) if (i not in remove_list)]
    index_id = [i for i in range(1, len(author_school) + 1)]
    dt = pd.DataFrame(author_school, columns=columns)
    ####生成处理过程中文件，作者及其对应单位
    path = "C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/author_school_possess.csv"
    dt.to_csv(path, index=0)
    return path

