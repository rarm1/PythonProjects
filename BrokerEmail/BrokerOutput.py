import pandas as pd

from ISINToTicker import ISINToTicker
from PIDLookup import PIDLookup
from PriceFinder import Prices

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)


class BrokerOutput:
    """Generates a broker output DataFrame from a given dealing_sheet."""

    def __init__(self, dealing_sheet):
        self.Tickers_Dict = None
        self.share_quantities = None
        self.price_per_share = None
        self.document = dealing_sheet.document
        self.Filetype = dealing_sheet.filetype

        column_mapping = {
            "xlsx": {"Security": "SecurityNameLong", "ISIN": "ISIN", "Shares": "Units", "Allocation": "PortfolioName",
                     "TradeID": "TradesTempID"},
            "csv": {"Security": "SecurityName", "ISIN": "SecurityIdentifier", "Shares": "Value",
                    "Allocation": "SchemeIdentifier", "TradeID": "TradeIdentifier"}
        }

        self.column_map = column_mapping[self.Filetype]
        # TODO: Create two DataFrames. One of which is the actual instruction, another of which is the checking table.
        headers = ['Action', 'Security', 'ISIN', 'Ticker', 'Shares', 'Approx. Notional Value',
                   'Currency', 'Allocation', 'Margetts Trade Reference', 'Price per Share', 'URLs']
        self.output = pd.DataFrame(columns=headers)
        self.tickers = []
        self.define_attributes()

    def define_attributes(self):
        self.set_action()
        self.set_security()
        self.set_isin()
        self.set_ticker()
        self.set_shares()
        self.set_currency()
        self.set_allocation()
        self.set_trade_id()
        self.set_price_per_share()
        self.apply_prices()
        self.apply_urls()

    def set_security(self):
        self.output['Security'] = self.document[self.column_map["Security"]]

    def set_action(self):
        self.output['Action'] = self.document['Direction']

    def set_isin(self):
        self.output['ISIN'] = self.document[self.column_map["ISIN"]]

    def set_ticker(self):
        isin_to_ticker = ISINToTicker(isin=self.output['ISIN'])
        self.output['Ticker'] = isin_to_ticker.tickers
        self.tickers = self.output['Ticker']

    def set_shares(self):
        self.output['Shares'] = self.document[self.column_map["Shares"]]
        self.share_quantities = self.output['Shares']

    def set_price_per_share(self):
        prices = Prices(self.tickers)
        self.Tickers_Dict = prices.Prices

    def set_currency(self):
        currency_template = ['GBP' for _ in range(len(self.output['Approx. Notional Value']))]
        self.output['Currency'] = currency_template

    def set_allocation(self):
        pid_lookup = PIDLookup(self.document['SchemeID'])
        self.output['Allocation'] = pid_lookup.designation_lookup
        # self.output['Allocation'] = self.document[self.column_map["Allocation"]]

    def set_trade_id(self):
        self.output['Margetts Trade Reference'] = self.document[self.column_map["TradeID"]]

    def apply_prices(self):
        for index, row in self.output.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            direction = row['Action']
            buy_price = float(self.Tickers_Dict[ticker][direction][:-1])
            if self.Tickers_Dict[ticker]['Currency'] == 'GBX':
                buy_price /= 100  # Convert pence to GBP
            notional_value = shares * buy_price
            formatted_notional_value = f"£{notional_value:,.2f}"
            self.output.at[index, 'Price per Share'] = buy_price
            self.output.at[index, 'Approx. Notional Value'] = formatted_notional_value

    def apply_urls(self):
        isin_to_ticker = ISINToTicker(isin=self.output['ISIN'], tickers=self.tickers)
        urls = isin_to_ticker.urls
        urls = [_[1] for _ in urls]
        self.output['URLs'] = urls
