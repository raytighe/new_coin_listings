from credentials import twitter_creds
import datetime
import re
import requests
from requests.structures import CaseInsensitiveDict


class TwitterFeeds:
    """
    Class to group methods of using Twitter's recent search API endpoint
    """
    def __init__(self):
        self.TWITTER_BEARER_TOKEN = twitter_creds['TWITTER_BEARER_TOKEN']
        # Set the start time at which twitter will return tweets after to minimize processing the same tweet
        # It is currently set for 3 minutes before the current time
        self.start_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).replace(microsecond=0).isoformat()

    def get_binance_news(self):
        # Recent search API call
        url = "https://api.twitter.com/2/tweets/search/recent?query=binance%20will%20list%20" \
              "from:binance&max_results=10&start_time=" + self.start_time + "Z"
        headers = CaseInsensitiveDict()
        headers["Authorization"] = 'Bearer ' + self.TWITTER_BEARER_TOKEN
        resp = requests.get(url, headers=headers)
        # Parse response to get coin symbol
        try:
            latest_tweet_text = resp.json()['data'][0]['text']
            start = latest_tweet_text.find('$') + 1
            end = latest_tweet_text.find('$') + 4
            coin_symbol = latest_tweet_text[start:end].strip()
            exchange = 'binance'

            return {'statusCode': 200,
                    'coin_symbol': coin_symbol,
                    'exchange': exchange,
                    'headline': latest_tweet_text}
        except KeyError:
            return {'statusCode': 201,
                    'message': 'No recent Binance tweets found announcing a new listing'}

    def get_coinbase_news(self):
        # Recent search API cal
        url = "https://api.twitter.com/2/tweets/search/recent?query=inbound%20transfers%20for%20" \
              "from:coinbasepro&max_results=10&start_time="+self.start_time+"Z"
        headers = CaseInsensitiveDict()
        headers["Authorization"] = 'Bearer ' + self.TWITTER_BEARER_TOKEN
        resp = requests.get(url, headers=headers)
        # Parse response to get coin symbol
        try:
            latest_tweet_text = resp.json()['data'][0]['text']
            coin_symbol_list = re.findall(r"(\b(?:[A-Z]+[a-z]?[A-Z]*|[A-Z]*[a-z]?[A-Z]+)\b(?:\s+(?:[A-Z]+[a-z]?[A-Z]*|[A-Z]*[a-z]?[A-Z]+)\b)*)",
                                          latest_tweet_text)
            # This line remove strings of capital words 2 characters or less like "PT" which are probably not coins
            coin_symbol_list_validated = [x for x in coin_symbol_list if len(x) >= 3]
            return {'statusCode': 200,
                    'coin_symbol': coin_symbol_list_validated,
                    'exchange': 'coinbase',
                    'headline': latest_tweet_text}
        except KeyError:
            return {'statusCode': 201,
                    'message': 'No recent Coinbase tweets found announcing a new listing'}
