from isin_to_ticker import ISINToTicker
import asyncio
import aiohttp

from bs4 import BeautifulSoup


class Prices:
    _document = None

    def __init__(self, requested_tickers, live_pricing: bool = True):
        self.urls = None
        self.Prices = {}
        self.Tickers = requested_tickers
        if live_pricing:
            self.set_prices(requested_tickers)
        else:
            self.default_prices(requested_tickers)

    @staticmethod
    async def _fetch_price_async(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                sell_price_span = soup.find("span", class_="bid price-divide")
                sell_price = sell_price_span.text.strip() if sell_price_span else None
                buy_price_span = soup.find("span", class_="ask price-divide")
                buy_price = buy_price_span.text.strip() if buy_price_span else None
                return sell_price, buy_price

    async def fetch_price_for_ticker(self, ticker, url, currency):
        sell_price, buy_price = await self._fetch_price_async(url)
        self.Prices[ticker] = {}
        if sell_price:
            self.Prices[ticker]["Sell"] = sell_price
        if buy_price:
            self.Prices[ticker]["Buy"] = buy_price
        self.Prices[ticker]["Currency"] = currency

    async def set_prices_async(self, requested_tickers):
        unique_tickers = set(requested_tickers)
        self.urls = ISINToTicker(tickers=unique_tickers).urls
        tasks = [
            self.fetch_price_for_ticker(ticker, url, currency)
            for ticker, url, currency in self.urls
        ]
        await asyncio.gather(*tasks)

    def set_prices(self, requested_tickers):
        asyncio.run(self.set_prices_async(requested_tickers))

    def default_prices(self, requested_tickers):
        """
        Sets the default prices for the given tickers.

        :param requested_tickers: A list of tickers to set default prices for
        """
        unique_tickers = set(requested_tickers)
        self.urls = ISINToTicker(tickers=unique_tickers).urls
        for ticker, url, currency in self.urls:
            print(f"Ticker: {ticker}")
            self.Prices[ticker] = {}
            self.Prices[ticker]["Sell"] = "1.502"
            self.Prices[ticker]["Buy"] = "1.6"
            self.Prices[ticker]["Currency"] = currency

