import requests
import re
# 获取新浪新闻关于关键词的新闻
def News_Infor(KEY):
	header={
				'Cookie': '_s_tentry=-; Apache=9509286182735.414.1622179099016; SINAGLOBAL=9509286182735.414.1622179099016; ULV=1622179099022:1:1:1:9509286182735.414.1622179099016:; WBtopGlobal_register_version=2021052813; crossidccode=CODE-tc-1LMuXr-1RALN2-0jf9H7GHvXqmcvs20a241; SSOLoginState=1622179381; SUB=_2A25NtA5lDeRhGeNM6VAR9yjMyz-IHXVvVpItrDV8PUJbkNAKLVngkW1NTiPTt2HGMuDvced2Btz10OGdTbQhk1Go; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W57Sn.mJcJ_4y4nojBQlHyv5NHD95QfeozEehMceh50Ws4Dqcj_i--Ri-z7iKnpi--ciK.Ri-8si--Xi-zRi-iWi--fiK.fi-2fi--fiK.pi-2E; wvr=6; WBStorage=8daec78e6a891122|undefined',
				'Host': 's.weibo.com',
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
				'Connection':'keep-alive',
			}
	info = requests.get("https://s.weibo.com/article?q=KEY&Refer=SListRelpage_box".replace("KEY",KEY),headers=header)
	print(info.text)
	#获取文章标题
	patren_1 = re.compile(r'<h3><a.*?target="_blank" title="(.*?)" suda-data.*?>',re.S)
	title = re.findall(patren_1,str(info.text))

	#获取标题的网址
	patren_2 = re.compile(r'<h3><a href="(.*?)" target="_blank" title.*?>',re.S)
	link = re.findall(patren_2,str(info.text))
	return title[:8],link[:8]