# New Coin Listings: A cryptocurrency trading bot based on exchanges' new listing announcements

Cryptocurrencies, like stocks, are nearly impossible to consistently trade successfully without a disciplined strategy. This project is a fully automated cryptocurrency trading bot based on a simple hypothesis that,

>When major cryptocurrency exchanges such as Binance and Coinbase announce they are going to list a new cryptocurrency coin or token on their platform, the price of that coin or token will likely increase significantly in few minutes.

## An Example
An example of this event occurred on December 27th, 2021 around midnight. In the evening, [$JOE](https://coinmarketcap.com/currencies/joe/) was trading around $2.20. At 11:58pm, [Binance tweeted](https://twitter.com/binance/status/1475692661822705666) that they would list $JOE and within 10 minutes, $JOE was trading at $2.50, about 14% higher. This trading strategy attempts to capitalize on the sudden upwards movement immediately after these types of announcements.

<p align="center">
<img src="https://github.com/raytighe/new_coin_listings/blob/main/img/binance_will_list_joe.PNG" width="40%" height="40%">
<img src="https://github.com/raytighe/new_coin_listings/blob/main/img/joe_price_12.27.2021.PNG" width="40%" height="40%">
</p>

## How it works
In short, this program scans data sources for announcements of new listings and attempts to trade for that coin as fast as possible. The current data sources are the Twitter accounts for Binance and Coinbase. I use a cron job to run this program every minute on a Linux virtual machine hosted on Azure. Below are the high-level steps:

1. Scan tweets from [@binance](https://twitter.com/binance) using the Twitter API's recent search endpoint to find recent tweets matching the regex pattern "Binance will list".
2. If a recent tweet is found, parse the coin symbol from the tweet and insert the coin symbol, exchange, and tweet text into a PostgreSQL database for record keeping. If no tweet is found, repeat step 1 using the next data source (such as the Coinbase Twitter account).
3. Attempt to trade for that coin on  [Gate.io](https://gate.io)
4. Send an email alert notifying yourself of new coin listing using the SendGrid API. I this set up to email a dedicated Gmail email address with push notifications on my phone.
5. Repeat step 1 using the next data source (such as the Coinbase Twitter account).

One challenge I encountered was finding an exchange that has already listed the coin. Binance and Coinbase announce they _will_ list coins soon, but by time they list them, the sudden price increase has already occurred. I chose to trade on Gate.io, a less popular exchange, because they usually list coins before the more popular exchanges such as Binance and Coinbase do. 

## Requirements
This project requires some accounts and API keys to access data sources, execute trades, and send alerts:

- [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api) - for Twitter data sources
- [Gate.io v4](https://www.gate.io/api2) - to execute trades
- [SendGrid](https://docs.sendgrid.com/for-developers/sending-email/api-getting-started) - to send email alerts

This project also uses a number of open source Python packages to work properly:

- [requests](https://docs.python-requests.org/en/latest/) - to format API requests
- [psycopg2](https://pypi.org/project/psycopg2/) - for interacting with PostgreSQL databases
- [gateapi-python](https://github.com/gateio/gateapi-python) - Gate.io's client library for executing trades
- [sendgrid-python](https://github.com/sendgrid/sendgrid-python) - SendGrid's client library for sending email alerts

Additionally, this project uses Azure cloud services:
- [A Linux Virtual Machine](https://azure.microsoft.com/en-us/services/virtual-machines/linux/) - For running the program 24/7
- [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/services/postgresql/) - A managed PostgreSQL database for storing the history of new coin listings

## Future Development Ideas
- The project is set up to easily add data sources for additional exchanges. Some exchanges announce new coin listings on their website in which case the website could be scraped.
- Gate.io allows for conditional orders to be placed based on price. An enhancement to this program could be to place stop-loss and take-profit orders when positions are established.











