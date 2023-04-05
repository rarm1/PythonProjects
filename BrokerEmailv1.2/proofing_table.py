import pandas as pd
from isin_to_ticker import ISINToTicker

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)


class ProofingTable:
    def __init__(self, class_input):
        self.tickers = []
        self.tickers_dict = {}
        headers = ['Ticker', '30 day rolling average', 'Shares', '% Traded', 'Price per Share', 'URL']
        self.ProofDataFrame = pd.DataFrame(columns=headers)
        self.broker_df = class_input.instructionoutput
        self.class_input = class_input
        self.set_tickers()
        self.isin_to_ticker = ISINToTicker(tickers=self.tickers)
        self.set_30d_avg()
        self.get_agg_traded()
        self.set_agg_traded()
        self.set_pct_traded()
        self.set_price_per_share()
        self.set_urls()

    def set_tickers(self):
        self.tickers = self.broker_df['Ticker'].unique()
        self.ProofDataFrame['Ticker'] = self.tickers

    def set_30d_avg(self):
        self.ProofDataFrame['30 day rolling average'] = self.isin_to_ticker.thirty_rolling_avg
        self.ProofDataFrame['30 day rolling average'] = self.ProofDataFrame['30 day rolling average'].str.replace(",", "").astype(float)

    def get_agg_traded(self):
        ticker_sums = self.broker_df.groupby('Ticker')['Shares'].sum()
        self.tickers_dict = {ticker: value for ticker, value in ticker_sums.items()}

    def set_agg_traded(self):
        for ticker in self.tickers:
            self.ProofDataFrame.loc[self.ProofDataFrame['Ticker'] == ticker, 'Shares'] = self.tickers_dict[ticker]

    def set_pct_traded(self):
        for ticker in self.tickers:
            self.ProofDataFrame.loc[self.ProofDataFrame['Ticker'] == ticker, '% Traded'] = round(self.tickers_dict[ticker] / self.ProofDataFrame.loc[
                self.ProofDataFrame['Ticker'] == ticker, '30 day rolling average'] * 100, 2)
            self.ProofDataFrame.loc[self.ProofDataFrame['Ticker'] == ticker, '% Traded'] = self.ProofDataFrame.loc[self.ProofDataFrame['Ticker'] == ticker,
            '% Traded'].astype(str) + '%'

    def set_price_per_share(self):
        for ticker in self.tickers:
            self.ProofDataFrame.loc[self.ProofDataFrame['Ticker'] == ticker, 'Price per Share'] = self.class_input.Tickers_Dict[ticker][
                'Directional Price']

    def set_urls(self):
        for ticker, url, _ in self.isin_to_ticker.urls:
            self.ProofDataFrame.loc[self.ProofDataFrame['Ticker'] == ticker, 'URL'] = url

