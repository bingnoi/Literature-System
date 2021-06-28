#!/usr/bin/python3
import pymysql
import pandas as pd
import re
def getTeam(data):
    # 二、存入team节点
    author_label = []
    result_list = []
    columns = ["team_id", "team", "label","worktitle"]
    # 每一篇文章作者作为一组
    author_list = []
    for i in range(0, len(data)):
        author_list.append(list(data[i][0].split(',')))
    index_id = [(100000 + i) for i in range(1, len(data) + 1)]
    for i in range(len(data)):
        author_label.append(data[i][1])
        result_list.append([index_id[i], ','.join(author_list[i]), author_label[i],data[i][2]])
    # print(result_list[2])
    dt = pd.DataFrame(result_list, columns=columns)
    #####存入csv，node：team#####
    dt.to_csv("C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/team.csv", index=0)
    # 四、去除team中重复元素并重新写入列表
    team_data = pd.read_csv("C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/team.csv")
    team_list = team_data.values.tolist()
    team = list(team_data['team'])
    label = list(team_data['label'])
    worktitle = list(team_data['worktitle'])
    re_list = []
    for i in range(len(team)):
        for j in range(i + 1, len(team)):
            if team[i] == team[j]:
                re_list.append(j)
    team = [team[i] for i in range(len(team)) if (i not in re_list)]
    label = [label[i] for i in range(len(label)) if (i not in re_list)]
    worktitle =[worktitle[i] for i in range(len(worktitle)) if (i not in re_list)]
    # 清空列表操作
    index_id.clear()
    author_label.clear()
    result_list.clear()
    columns = ["team_id", "team", "label","type","worktitle"]
    # 每一篇文章作者作为一组
    index_id = [(100000 + i) for i in range(1, len(team) + 1)]
    for i in range(len(team)):
        result_list.append([index_id[i], team[i], label[i],'team',worktitle[i]])
    dt = pd.DataFrame(result_list, columns=columns)
    #####存入csv，node：team#####
    dt.to_csv("C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/team.csv", index=0)

    print('team ok')
