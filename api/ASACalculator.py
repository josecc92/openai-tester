from currency import Currency

# add const variable
MILES_UNIT_PRICE = 0.0275
# rate type enum
SPOT_RATE = '本行即期賣出'
CASH_RATE = '本行現金賣出'

class ASACalculator:
    def __init__(self):
      pass

    def get_bonus_miles(self, bonus_percentage, purchase_miles):
        return purchase_miles * bonus_percentage / 100

    def get_asa_mile_unit_price_cash(self, bonus_percentage, purchase_miles):
        result_msg = ''
        bonus_miles = round(self.get_bonus_miles(bonus_percentage, purchase_miles))
        total_miles = purchase_miles + bonus_miles
        result_msg += f"Purchased Miles: {purchase_miles}, Bonus Miles: {bonus_miles}, Total Miles: {total_miles}\n"
        result_msg += f"Total Price: {purchase_miles * MILES_UNIT_PRICE} USD, Unit Price: {round(purchase_miles * MILES_UNIT_PRICE / total_miles,3)} USD\n"

        return f"{result_msg}"

    def _get_exchange_rate(self, soup, currency_index, rate_type):
        div_elements = soup.find_all('div', {'class': 'visible-phone print_hide'})
        for div_element in div_elements:
            if currency_index in div_element.text:
                rate = div_element.find_next('td', {'data-table': rate_type}).text.strip()
                return rate
        return None

aSACalculator = ASACalculator()
print(aSACalculator.get_asa_mile_unit_price_cash( 50, 1000))

currency_rate = Currency()
print(currency_rate.get_currency('USD'))
print(currency_rate.get_currency_spot('USD'))    