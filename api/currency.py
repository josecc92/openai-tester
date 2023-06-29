import requests
from bs4 import BeautifulSoup

class Currency:
  def __init__(self):
    pass

  def get_currency(self, currency_index):
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    time = soup.find('span',{'class':'time'})
    div_elements = soup.find_all('div', {'class': 'visible-phone print_hide'})
    for div_element in div_elements:
        if currency_index in div_element.text:
            value = f"{time.text} {div_element.text.strip()} 匯率: {div_element.find_next('td', {'data-table': '本行現金賣出'}).text.strip()}"
            return value
    return f"查無{currency_index}匯率"

def get_currency_spot(self, currency_index):
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    time = soup.find('span',{'class':'time'})
    div_elements = soup.find_all('div', {'class': 'visible-phone print_hide'})
    for div_element in div_elements:
        if currency_index in div_element.text:
            value = f"{time.text} {div_element.text.strip()} 即期匯率: {div_element.find_next('td', {'data-table': '本行即期賣出'}).text.strip()}"
            return value
    return f"查無{currency_index}即期匯率"
