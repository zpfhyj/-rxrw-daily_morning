from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
#user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  #url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  url = "http://api.yytianqi.com/observe?city=CH090101&key=cjjhfggthaue8ilm"
  res = requests.get(url).json()
  #weather = res['data']['list'][0]
  weather = res['data']
  #return weather['weather'], weather['humidity'],math.floor(weather['temp'])
  return weather['tq'], weather['sd']+"%",math.floor(float(weather['qw']))

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, humidity, temperature = get_weather()
data = {"weather":{"value":wea, "color": get_random_color()},"humidity":{"value":humidity, "color": get_random_color()},"temperature":{"value":temperature, "color": get_random_color()},"love_days":{"value":get_count(), "color": get_random_color()},"birthday_left":{"value":get_birthday(), "color": get_random_color()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
#user_id = user_id2
#res = wm.send_template(user_id, template_id, data)
#print(res)
