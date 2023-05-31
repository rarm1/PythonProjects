import pandas as pd
from pathlib import Path
# Define your constants here
FUND_SELL_LIMIT = 0.01
SECTOR_SELL_LIMIT_TRADED = 0.002
BUCKET_SELL_LIMIT = 0.005
ASSET_GROUPS = {
    "Bonds": ["Bond", "Property", "Commodity", "Absolute Return"],
    "Equities": ["UK", "UK EQUITY INCOME", "ASIA PACIFIC", "EUROPE", "USA", "GLOBAL", "EMERGING MARKETS",
                 "IA 20-60%", "IA 0-35%", "JAPAN"],
    "Cash/Money Markets": ["CASH/MONEY MARKETS"],
}
from write_to_trade_file import TradeWriter

class TradingAlgo:
    def __init__(self, df_in, fund_nav, asset_groups=None):
        if asset_groups is None:
            asset_groups = ASSET_GROUPS
        self.asset_groups = asset_groups
        self.nav = fund_nav
        self.df = df_in
        self._prepare_df_for_trades()
        max_iterations = 100  # Set a maximum number of iterations
        iteration = 0  # Initialize the iteration counter
        #
        while not self._is_on_target():
            fund = self._trade("Fund Over/Under", "Fund Over/Under", FUND_SELL_LIMIT)
            if self._is_on_target():
                break
            sector = self._trade("Sector Over/Under", "Sector Over/Under", SECTOR_SELL_LIMIT_TRADED)
            if self._is_on_target():
                break
            bucket = self._trade("Bucket Over/Under", "Bucket Over/Under", BUCKET_SELL_LIMIT)
            if self._is_on_target():
                break
            iteration += 1  # Increment the iteration counter
            if iteration >= max_iterations:  # If maximum iterations reached, break out of the loop
                print("Maximum iterations reached. Exiting the loop.")
                print(self.df.to_string())
                break

    def _is_on_target(self):
        condition_fund = (self.df["Fund Over/Under"] != "On Target").any()
        condition_sector = (self.df["Sector Over/Under"] != "On Target").any()
        condition_bucket = (self.df["Bucket Over/Under"] != "On Target").any()
        # Return True if all conditions are not met (i.e., on target)
        return not (condition_fund or condition_sector or condition_bucket)

    def _prepare_df_for_trades(self):
        self.df["Tradeable"] = True
        self.df["Traded"] = False
        self.df["Trade Amount"] = 0.00
        self.df["Initial Market Value"] = self.df["Base Market Value"]
        self.df.loc[self.df["% Target"] == 0, "Fund Over/Under"] = "Sell"
        self._recalculate_percentages()
        # Check whether any funds should be sold completed. If so, sell them and recalculate percentages removing
        # this fund from the calculation.
        self.sell_all_fund()

    def _trade(self, entity_col, action_col, threshold):
        entities_to_trade = self.df[(self.df[entity_col] != "On Target") & (self.df['Tradeable'] == True)].copy()
        unique_entities = entities_to_trade[entity_col].unique()
        for idx, unique_entity in enumerate(unique_entities):
            if idx == 0:
                entity_to_trade = entities_to_trade[entities_to_trade[entity_col] == unique_entity].copy()
                action = entity_to_trade[action_col].iloc[0]
                ascending_order = True if action == "Buy" else False
                fund_to_trade = entity_to_trade.sort_values(by="% Fund Difference", ascending=ascending_order)
                fund_to_trade = fund_to_trade.iloc[[0]]
                difference = fund_to_trade["% Fund Difference"].iloc[0] - fund_to_trade["% Sector Difference"].iloc[0]
                trade_amount = self._calculate_trade_amount(action, fund_to_trade, difference, threshold)
                fund_to_trade["Trade Amount"] = trade_amount
                self.df = self._apply_trades(self.df, fund_to_trade)
                self._recalculate_percentages()
                return True
        return False

    def _calculate_trade_amount(self, action, fund_to_trade, difference, threshold):
        multiplier = -1 if action == "Sell" else 1
        if abs(difference) < threshold:
            trade_amount = fund_to_trade["% Fund Difference"] * self.nav * multiplier
        else:
            trade_amount = fund_to_trade["% Sector Difference"] * self.nav * multiplier
        return trade_amount

    @staticmethod
    def _apply_trades(df, funds_to_trade):
        funds_to_trade["Traded"] = True
        funds_to_trade["Base Market Value"] += round(funds_to_trade["Trade Amount"], 2)
        df.update(funds_to_trade)
        df['Designation'] = df['Designation'].astype(int)
        return df

    def _recalculate_percentages(self):
        self.df["Designation"] = self.df["Designation"].astype(int)
        self.df["% Holding"] = self.df["Base Market Value"] / self.nav
        self.df["% Fund Difference"] = self.df["% Holding"] - self.df["% Target"]

        self.df['% Sector Target'] = self.df.groupby('Investment Area')['% Target'].transform('sum')
        self.df['% Sector Holding'] = self.df.groupby('Investment Area')['% Holding'].transform('sum')
        self.df['% Sector Difference'] = self.df['% Sector Holding'] - self.df['% Sector Target']
        self.df['Sector Traded'] = self.df.groupby('Investment Area')['Traded'].transform('any')

        self.df['Bucket'] = self.df['Investment Area'].str.lower().map(
            lambda x: next((k for k, v in self.asset_groups.items() if x in [item.lower() for item in v]), None))
        self.df['% Bucket Target'] = self.df.groupby('Bucket')['% Target'].transform('sum')
        self.df['% Bucket Holding'] = self.df.groupby('Bucket')['% Holding'].transform('sum')
        self.df['% Bucket Difference'] = self.df['% Bucket Holding'] - self.df['% Bucket Target']

        # Now use 'Sector Traded' instead of 'Traded' in the sector_over_under function
        def sector_over_under(row):
            limit = 0.002 if row['Sector Traded'] else 0.005
            return "Sell" if row['% Sector Difference'] > limit \
                else "Buy" if row['% Sector Difference'] < -limit \
                else "On Target"
        self.df['Fund Over/Under'] = self.df['% Fund Difference'].map(
            lambda x: "Sell" if x > 0.01 else "Buy" if x < -0.01 else "On Target"
        )
        self.df['Sector Over/Under'] = self.df.apply(sector_over_under, axis=1)
        self.df['Bucket Over/Under'] = self.df['% Bucket Difference'].map(
            lambda x: "Sell" if x > 0.005 else "Buy" if x < -0.005 else "On Target"
        )

    def sell_all_fund(self):
        if self.df["Fund Over/Under"].any():
            # Create a dataframe of funds to sell
            funds_to_sell = self.df[self.df["% Target"] == 0].copy()
            funds_to_sell["Trade Amount"] = funds_to_sell["Base Market Value"] * -1
            funds_to_sell["Tradeable"] = False
            self.df = self._apply_trades(self.df, funds_to_sell)
            self._recalculate_percentages()


if __name__ == '__main__':
    asset_groups = {
        "Bonds": ["Bond", "Property", "Commodity", "Absolute Return"],
        "Equities": ["UK", "UK EQUITY INCOME", "ASIA PACIFIC", "EUROPE", "USA", "GLOBAL", "EMERGING MARKETS",
                     "IA 20-60%", "IA 0-35%", "JAPAN"],
        "Cash/Money Markets": ["CASH/MONEY MARKETS"],
    }
    print("Explorer")
    input_df = pd.read_csv(r"X:\Fund Management\Fund Management Team Files\FM Personal "
                     r"Folders\Richard\PycharmProjects\Rebalancing\Clarion\Navigator.csv")
    ta = TradingAlgo(input_df, 41550166.01)
    print(ta.df.to_string())
    TradeWriter(ta.df)

