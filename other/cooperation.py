#relation:coopeartion(new)
import pandas as pd
def getCooperation():
    #分别读取三个文件（获取对应唯一的ID）
    author_data = pd.read_csv("C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/author_new.csv")
    author_list=author_data.values.tolist()
    team_data = pd.read_csv("C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/team.csv")
    team_list=team_data.values.tolist()
    #存储结果
    result_list = []
    for author in author_list:
        for team in team_list:
            if author[0] in team[1] and author[1] in team[2]:#如果人名字＆工作单位都匹配上
                result_list.append([author[2],team[0],team[4]," "])
    columns = ["author_id","team_id","relation","type"]
    dt = pd.DataFrame(result_list, columns=columns)
    #####存入csv，relation：author cooperation team#####
    dt.to_csv("C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/cooperation.csv", index=0)
    print('cooperation ok')