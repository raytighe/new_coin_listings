from alerts import EmailAlerts
from credentials import db_connection
import psycopg2
from trade_executor import GateAPIOperations


class Postgres:
    def __init__(self):
        # Construct connection string
        self.conn_string = db_connection['string']
        self.conn = psycopg2.connect(self.conn_string)
        self.cursor = self.conn.cursor()

    def close_connections(self):
        """
        Method to close all database connections
        """
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except Exception:
            pass

    def validate_coin_exchange_exists(self, coin_symbol, exchange):
        """
        Method to check if the coin listed on the exchange is already known
        :param coin_symbol: coin symbol
        :param exchange: exchange on which coin will be availble to trade
        """
        self.cursor.execute("SELECT coin_symbol, exchange "
                            "FROM new_coin_listings "
                            "WHERE coin_symbol = %s AND exchange = %s",
                            (coin_symbol, exchange))
        results = self.cursor.fetchone()
        if results is None:
            return {'statusCode': 200, 'message': 'Coin and exchange combination does not exist already'}
        else:
            return {'statusCode': 400, 'message': 'Coin and exchange combination exists already'}

    def insert_new_coin_listings(self, data):
        """
        Method to insert coin listing into database, establish position via Gate.io, and send an email alert
        """
        try:
            # truncate headline to 300 characters and convert stings to lists
            headline_full = data['headline']
            headline_trunc = (headline_full[:297] + '...') if len(headline_full) > 300 else headline_full
            symbol_list = [data['coin_symbol']] if isinstance(data['coin_symbol'], str) else data['coin_symbol']
            for symbol in symbol_list:
                validation_status_code = self.validate_coin_exchange_exists(symbol, data['exchange'])['statusCode']
                if validation_status_code == 200:

                    # Attempt to take position and set up stop loss and take profit orders
                    if data['exchange'] in ['kucoin', 'coinbase']:
                        GateAPIOperations().establish_position(symbol, 'USDT', total_order_value=10.00)

                    # Write to database
                    self.cursor.execute("INSERT INTO new_coin_listings (coin_symbol, exchange, headline) VALUES (%s, %s, %s);",
                                        (symbol, data['exchange'], headline_trunc))

                    # Send email alert
                    subject = 'New Coin Alert: ' + symbol + ' will be listed on ' + data['exchange']
                    body = headline_full
                    EmailAlerts().send_email(subject=subject, body=body)

        except Exception as e:
            print(e)
        finally:
            self.close_connections()
