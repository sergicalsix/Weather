import requests
from bs4 import BeautifulSoup
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
def get_weather(url,area_name = '東京都中央区',today = False):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    day_num = 1
    if today:
        day_num = 0
        
    weather = soup.find_all('p','weather-telop')[day_num].text
    high_temp, low_temp = soup.find_all('dd','high-temp temp')[day_num].find('span').text,soup.find_all('dd','low-temp temp')[day_num].find('span').text
    rain_time = ['0~6時:','6~12時:','12~18時:','18~24時:']
    rain_prob = [ v.text for v in soup.find_all('tr','rain-probability')[day_num].find_all('td')]
    rain_info = [ x[0]+x[1] for x in zip(rain_time,rain_prob)]
    rain_info = ' '.join(rain_info)
    
    message = f'{area_name}の天気:{weather}\n {high_temp}度,{low_temp}度,降水確率:{rain_info}'
    
    print(message)

    return  message
    
# 事前にURLは調べておく
kuri = get_weather('https://tenki.jp/forecast/3/16/4410/13102/',area_name = '東京都中央区')
yusuke = get_weather('https://tenki.jp/forecast/3/17/4610/14109/',area_name = '日吉')
dt_tom = (datetime.datetime.now()+ datetime.timedelta(days = 1)).strftime('%m月%d日(%a)')


import yaml
with open('/Users/shibuya/myGithub/Weather/config.yaml') as file:
    obj = yaml.safe_load(file)
    TOKEN = obj['TOKEN']


#APIのURL
api_url = 'https://notify-api.line.me/api/notify'
#送りたい内容
send_contents = '\n'+ dt_tom + '\n'+ kuri + '\n\n' + yusuke

TOKEN_dic = {'Authorization': 'Bearer' + ' ' + TOKEN} 
send_dic = {'message': send_contents}


requests.post(api_url, headers=TOKEN_dic, data=send_dic)





