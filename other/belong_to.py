#new relation_write:belong_to
#relation:belong_to
import pandas as pd
#分别读取三个文件（获取对应school的ID）
def getBelong():
    school_data = pd.read_csv("/Users/yutao/Desktop/HelloWorld/other/school.csv")
    school_list=school_data.values.tolist()
    author_school_data = pd.read_csv("/Users/yutao/Desktop/HelloWorld/other/author_new.csv")
    author_school_list = author_school_data.values.tolist()
    result_list = []
    for i in range(len(author_school_list)):
        for school in school_list:
            if author_school_list[i][1] in school:
                result_list.append([(i+1),school[0],"belong_to","belong_to"])
    columns = ["author_id","school_id","relation","type"]
    dt = pd.DataFrame(result_list, columns=columns)
    #####存入csv，relation：author belong to school#####
    dt.to_csv("belong_to.csv", index=0)
    print('ok')