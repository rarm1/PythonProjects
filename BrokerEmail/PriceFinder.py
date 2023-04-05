from ISINToTicker import ISINToTicker
import requests
from bs4 import BeautifulSoup


# TODO: Maybe read the tickers below from the ISIN TO Ticker document. All I need to do is add a hargreaves lansdown
#  column and a currency column.
class Prices:

    _document = None

    def __init__(self, requested_tickers):

        self.urls = None
        self.Prices = {}
        # self.default_prices(requested_tickers)
        # self.Tickers = requested_tickers
        self.set_prices(requested_tickers)

    @staticmethod
    def _fetch_price(url):
        """
        Fetches the buy and sell prices from the given URL.

        :param url: The URL to fetch the prices from
        :return: A tuple containing the sell price and the buy price
        """
        response = requests.get(url)
        print(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            sell_price_span = soup.find("span", class_="bid price-divide")
            sell_price = sell_price_span.text.strip() if sell_price_span else None
            buy_price_span = soup.find("span", class_="ask price-divide")
            buy_price = buy_price_span.text.strip() if buy_price_span else None
            print(f"Sell price: {sell_price}. Buy price: {buy_price}")
            return sell_price, buy_price
        return None, None

    def set_prices(self, requested_tickers):
        """
        Sets the prices for the given tickers.

        :param requested_tickers: A list of tickers to fetch prices for
        """
        unique_tickers = set(requested_tickers)
        self.urls = ISINToTicker(tickers=unique_tickers).urls
        for ticker, url, currency in self.urls:
            print(f"Ticker: {ticker}")
            self.Prices[ticker] = {}
            sell_price, buy_price = self._fetch_price(url)
            if sell_price:
                self.Prices[ticker]["Sell"] = sell_price
            if buy_price:
                self.Prices[ticker]["Buy"] = buy_price
            self.Prices[ticker]["Currency"] = currency

    # def default_prices(self, requested_tickers):
    #     ticker_dict = {}
    #     for ticker in requested_tickers:
    #         ticker_dict[ticker] = '_'
    #     unique_tickers = ticker_dict.keys()
    #     ticker_keys = self.Tickers.keys()
    #     for ticker in unique_tickers:
    #         self.Prices[ticker] = {}
    #         if ticker.lower() in ticker_keys:
    #             self.Prices[ticker]["Sell"] = "105.44p"
    #             self.Prices[ticker]["Buy"] = "106.35"
    #             self.Prices[ticker]["Currency"] = self.Tickers[ticker.lower()]['currency']
