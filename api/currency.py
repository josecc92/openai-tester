import requests
from bs4 import BeautifulSoup

class Currency:
    QUERY_TIME = ''
    SPOT_RATE = '本行即期賣出'
    CASH_RATE = '本行現金賣出'
    # Test
    def __init__(self):
      pass

    def get_currency(self, currency_index):
        cash_rate = self._get_exchange_rate(currency_index, self.CASH_RATE)
        if cash_rate is not None:
            return f"{self.QUERY_TIME} {currency_index} 匯率: {cash_rate}"
        return f"查無{currency_index}匯率"

    def get_currency_spot(self, currency_index):
        spot_rate = self._get_exchange_rate( currency_index, self.SPOT_RATE)
        if spot_rate is not None:
            return f"{self.QUERY_TIME} {currency_index} 即期匯率: {spot_rate}"
        return f"查無{currency_index}即期匯率"

    def _get_exchange_rate(self, currency_index, rate_type):
        url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        time = soup.find('span', {'class': 'time'}).text.strip()
        self.QUERY_TIME = time
        div_elements = soup.find_all('div', {'class': 'visible-phone print_hide'})
        for div_element in div_elements:
            if currency_index in div_element.text:
                rate = div_element.find_next('td', {'data-table': rate_type}).text.strip()
                return rate
        return None

if __name__ == "__main__":
    currency_rate = Currency()
    print(currency_rate.get_currency('USD'))
    print(currency_rate.get_currency_spot('USD'))    
