import requests
from bs4 import BeautifulSoup

class Currency:
  def __init__(self):
    pass

  def get_currency(self, currency_index):
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    div_elements = soup.find_all('div', {'class': 'visible-phone print_hide'})
    for div_element in div_elements:
        if currency_index in div_element.text:
            value = f"{div_element.text.strip()}匯率: {div_element.find_next('td', {'data-table': '本行現金賣出'}).text.strip()}"
            return value
    return '無匯率'
