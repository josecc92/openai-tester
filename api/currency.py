class Currency:
  def __init__(self):
    pass

  def get_currency(self, currency_index):
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    div_element = soup.find('div', text=re.compile(currency_index))
    if div_element is None:
        return '無匯率' # 或其他預設值，例如 0

    value = div_element.find_next('td', {'data-table': '本行現金賣出'}).text.strip()
    return value
