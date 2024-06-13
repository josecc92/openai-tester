from currency import Currency

# add const variable
MILES_UNIT_PRICE = 0.0275
TAX_RATE = 0.075
# rate type enum

class ASACalculator:
    BOOKING_FEE = 25.00
    AIRPORT_TAX_AND_FEES = 41.00
    def __init__(self):
      pass

    def process_bonus_percentage(self,bonus_percentage_string):
        try:
            # 嘗試將字符串轉換為浮點數
            float_value = float(bonus_percentage_string)
            
            # 如果成功轉換，則返回去除百分比後的浮點數
            return float_value
            
        except ValueError:
            # 如果無法轉換為浮點數，則當作帶有百分比的字符串處理
            return int(bonus_percentage_string.replace("%", ""))

    def get_bonus_miles(self, bonus_percentage, purchase_miles):
        return purchase_miles * bonus_percentage / 100

    def get_asa_mile_unit_price(self, bonus_percentage_string, purchase_miles, rate_type, round_trip_mileage=0):
        result_msg = ''
        bonus_percentage = self.process_bonus_percentage(bonus_percentage_string)
        bonus_miles = round(self.get_bonus_miles(bonus_percentage, purchase_miles))
        total_miles = purchase_miles + bonus_miles
        total_count_usd = purchase_miles * MILES_UNIT_PRICE
        total_count_tax = total_count_usd * (1 + TAX_RATE)
        exchange_rate = self.process_bonus_percentage(Currency()._get_exchange_rate('USD', rate_type))
        result_msg += "==========> Original Purchase\n" 
        result_msg += f"Purchased miles: {purchase_miles}, {round(bonus_percentage)}% bonus: {bonus_miles}, total miles obtained: {total_miles}\n"
        result_msg += f"Exchange rate: {exchange_rate}({rate_type}), Unit price: ${round(MILES_UNIT_PRICE, 5)} USD, {round(MILES_UNIT_PRICE * exchange_rate, 3)} NTD\n"
        result_msg += "==========> Bonus Calculation\n"
        result_msg += f"Total amount: ${total_count_usd} USD, unit price: ${round(total_count_usd / total_miles, 5)} USD\n"
        result_msg += f"Total amount: {total_count_usd * exchange_rate} TWD, unit price: {round(total_count_usd * exchange_rate / total_miles, 3)} TWD\n"
        result_msg += f"==========> Bonus with Tax Recovery Fee Calculation {TAX_RATE * 100}%\n"
        result_msg += f"Total amount with fee: ${total_count_tax} USD, unit price with fee: ${round(total_count_tax / total_miles, 5)} USD\n"
        result_msg += f"Total amount with fee: {round(total_count_tax * exchange_rate)} TWD, unit price with fee: {round(total_count_tax * exchange_rate / total_miles, 3)} TWD\n"
        if(round_trip_mileage > 0):
            result_msg += "==========> Round-trip Ticket Bonus with Fee and Tax\n"
            result_msg += f"Round-trip mileage used: {round_trip_mileage}\n"
            result_msg += f"Round-trip ticket amount: ${round(round_trip_mileage * total_count_tax / total_miles, 2)} USD\n"
            result_msg += f"Booking Fee: ${self.BOOKING_FEE} USD, Airport Taxes: ${self.AIRPORT_TAX_AND_FEES} USD\n"
            total_amount = round(round_trip_mileage * total_count_tax / total_miles + self.BOOKING_FEE + self.AIRPORT_TAX_AND_FEES, 2)
            result_msg += f"Total amount: ${round(total_amount,2)} USD\n"
            result_msg += f"Total amount: {round(total_amount*exchange_rate)} TWD\n"
        return f"{result_msg}"

    def _get_exchange_rate(self, soup, currency_index, rate_type):
        div_elements = soup.find_all('div', {'class': 'visible-phone print_hide'})
        for div_element in div_elements:
            if currency_index in div_element.text:
                rate = div_element.find_next('td', {'data-table': rate_type}).text.strip()
                return rate
        return None
if __name__ == "__main__":
    aSACalculator = ASACalculator()
    #print(aSACalculator.get_asa_mile_unit_price_cash( "50%", 10000,Currency.CASH_RATE))
    #print(aSACalculator.get_asa_mile_unit_price_cash( 50, 10000,Currency.CASH_RATE))
    print(aSACalculator.get_asa_mile_unit_price_cash( 70, 30000,Currency.CASH_RATE, 15000))
    currency_rate = Currency()
    #print(currency_rate.get_currency('USD'))
    #print(currency_rate.get_currency_spot('USD'))    
