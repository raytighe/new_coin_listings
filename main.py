from database_interactions import Postgres
from datetime import datetime
from twitter_feeds import TwitterFeeds


if __name__ == '__main__':
    print('Starting program...\nThe current time is', datetime.now())

    # Binance
    print('Starting Binance...')
    response = TwitterFeeds().get_binance_news()
    if response['statusCode'] == 200:
        Postgres().insert_new_coin_listings(response)

    # Coinbase
    print('Starting Coinbase...')
    response = TwitterFeeds().get_coinbase_news()
    if response['statusCode'] == 200:
        Postgres().insert_new_coin_listings(response)

print('Ending program...The current time is', datetime.now())
