import requests
import re
from bs4 import BeautifulSoup

class currency:
  def __init__(self):

  def getCurrency(self,currencyIndex)
  url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  # 找到包含英鎊的<div>元素
  div_element = soup.find('div', text=re.compile(currencyIndex))

  # 獲取所需的值
  value = div_element.find_next('td', {'data-table': '本行現金賣出'}).text
  return value
