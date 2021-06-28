import pandas as pd
def getTpData():
    author_data = pd.read_csv('C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/author_new.csv')
    author_team_tp = []
    for i in range(len(author_data)):
        author_id = author_data['author_id'][i]
        name = author_data['name'][i]
        t = author_data['type'][i]
        d = {'data': {"id": str(author_id), 'name': name, "label": t}}
        author_team_tp.append(d)
    team_data = pd.read_csv('C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/team.csv')
    for i in range(len(team_data)):
        team_id = team_data['team_id'][i]
        name = team_data['team'][i]
        t = team_data['type'][i]
        worktitle = team_data['worktitle'][i]
        d = {'data': {"id": str(team_id), 'name': name, "label": t,'worktitle':worktitle}}
        author_team_tp.append(d)
    co_data = pd.read_csv('C:/Users/bingnoi/Desktop/design/HelloWorld/HelloWorld/other/cooperation.csv')
    co_tp = []
    for i in range(len(co_data)):
        author_id = co_data['author_id'][i]
        team_id = co_data['team_id'][i]
        t = co_data['type'][i]
        worktitle = co_data['relation'][i]
        d = {'data': {"source": str(author_id), 'target': str(team_id), "relationship": t,"worktitle":worktitle}}
        co_tp.append(d)
    return author_team_tp,co_tp