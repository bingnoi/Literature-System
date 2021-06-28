import pandas as pd
def getAuthor(path):
    print(path)
    author_school_data = pd.read_csv(path)
    author_school_list = author_school_data.values.tolist()
    columns = ["name","label", "author_id","type"]
    index_id = []
    index_id = [i for i in range(1,len(author_school_list)+1)]
    result_list = []
    for i in range(len(author_school_list)):
        author_school_list[i].append(index_id[i])
        author_school_list[i].append('person')
    dt = pd.DataFrame(author_school_list, columns=columns)
    ####生成处理过程中文件，作者及其对应单位
    dt.to_csv("C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/author_new.csv", index=0)
    print('author ok')