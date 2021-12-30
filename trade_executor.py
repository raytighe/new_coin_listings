from credentials import gateio_creds
from gate_api import ApiClient, Configuration, Order, SpotApi, SpotPriceTriggeredOrder, SpotPriceTrigger, SpotPricePutOrder
import time


class GateAPIOperations:
    def __init__(self):
        # Initialize API authentication
        self.config = Configuration(key=gateio_creds['apiKey'], secret=gateio_creds['secretKey'])
        self.spot_api = SpotApi(ApiClient(self.config))

    def establish_position(self, base_symbol, quote_symbol, total_order_value):
        """
        Method to establish position on Gate.io
        :param base_symbol: Coin to buy
        :param quote_symbol: Coin to sell (USDT)
        :param total_order_value: Value of USDT to trade for base symbol coin
        :return:
        """
        try:
            # Validate currency pair (this will fair if not valid)
            currency_pair = base_symbol + '_' + quote_symbol
            self.spot_api.get_currency_pair(currency_pair)

            # check balance of USDT
            accounts = self.spot_api.list_spot_accounts(currency=quote_symbol)
            available = accounts[0].available

            # If balance is sufficient then attempt to establish position in coin
            if float(available) > total_order_value:
                self.submit_market_buy_order(currency_pair, total_order_value, slippage=0.02)
            else:
                print("Account balance not sufficient")
        except Exception as e:
            print(e)

    def submit_market_buy_order(self, currency_pair, total_order_value, slippage):
        """
        Method that attempts to complete order up to 5 times, waiting 5 seconds between submitting each order.
        :param currency_pair: currency pair to trade
        :param total_order_value: total order value to trade
        :param slippage: allowable slippage in price
        :return: order details
        """
        for i in range(0, 5):
            while True:
                # get last price and add slippage
                last_price = float(self.spot_api.list_tickers(currency_pair=currency_pair)[0].last) * (1.0+slippage)
                order_amount = total_order_value / last_price
                order = Order(amount=str(order_amount), price=str(last_price),
                              side='buy', currency_pair=currency_pair, type='limit')
                order_created = self.spot_api.create_order(order)
                time.sleep(5)
                order_submitted = self.spot_api.get_order(order_created.id, currency_pair)
                if order_submitted.status == 'closed':
                    print(order_submitted)
                    return order_submitted
                else:
                    self.spot_api.cancel_order(order_submitted.id, currency_pair)
                    print('cancelled order')
                    continue
        return {'status': 'failed to complete order'}
