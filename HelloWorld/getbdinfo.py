import requests
import re
# 获取百度百科关于关键词的介绍
def getBaiDuInfo(val):
	header={
					'Cookie': 'BAIDUID=412A148368EDF1BFEF71D013600BE91B:FG=1; PSTM=1553324805; BIDUPSID=1E5318C442166F414166451F9305620C; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; delPer=0; PSINO=1; ZD_ENTRY=baidu; BDRCVFR[Cw9oagB5smc]=yiTPYW-i3eTXZFWmv68mvqV; pgv_pvi=7175139328; pgv_si=s8533298176; baikedeclare=showed; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1556682401,1556682415,1556682605,1556682619; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%22%2C%22%E5%A4%A7%E6%95%B0%E6%8D%AE%22%5D%7D; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1556683243',
					'Host': 'baike.baidu.com',
					'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
					'Connection':'keep-alive',
				}
	info = requests.get("https://baike.baidu.com/search/word?word=val".replace("val",val),headers= header)
	info.encoding='utf-8'
	patren_1 = re.compile(r'<div class="para" label-module="para">(.*?)</div>',re.S)#
	info = re.findall(patren_1,str(info.text))
	info = info[0:3]
	text = " ".join(info)
	text  = re.findall("[\u4e00-\u9fa5，、。]+",str(text))
	text = "".join(text)
	return text