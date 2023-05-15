import pandas as pd
filename = r"X:\Fund Management\Fund Management Team Files\FM Personal " \
           r"Folders\Richard\PycharmProjects\Rebalancing\assets\Horizon Positions.xlsm"
class GetPositions:
    def __init__(self):
        self.positions_df = self._def_fund_positions_df()
        self.fund_trend_df = self._def_fund_trend_df()
        self.dilution_df = self._def_dilution_df()

    @staticmethod
    def _def_fund_positions_df():
        df = pd.read_excel(filename, sheet_name="Horizon Positions", skiprows=2, engine='openpyxl')
        df = df[["Designation", "pID", "PortfolioName", "ISIN", "SecurityNameShort",
                                          "BaseBidValue", "AssetTypeID"]]
        return df

    @staticmethod
    def _def_fund_trend_df():
        df = pd.read_excel(filename, sheet_name="Fund Trend", skiprows=8, engine='openpyxl')
        df.columns = df.iloc[0]
        df.drop(index=df.index[:1], inplace=True)
        df["Account Number"] = df["Account Number"].astype(int)
        return df

    @staticmethod
    def _def_dilution_df():
        df = pd.read_excel(filename, sheet_name="DilutionAdjustment", skiprows=2, engine='openpyxl',
                           dtype={'Designation': int, 'PortfolioName': str, 'CashFlow': float, 'NetAssetValue': float})
        df = df[["Designation", "PortfolioName", "CashFlow", "NetAssetValue"]]
        return df

    def pid_positions(self, pID):
        return self.positions_df[self.positions_df["pID"] == pID]

    def designation_positions(self, designation):
        return self.positions_df[self.positions_df["Designation"] == designation]

    def designation_trend(self, designation):
        return self.fund_trend_df[self.fund_trend_df["Account Number"] == designation]

    def get_nav(self, designation):
        return self.designation_trend(designation)['Net Assets'].values[0]

    def get_cashflow(self, **kwargs):
        if 'Designation' in kwargs:
            return self.dilution_df[self.dilution_df["Designation"] == kwargs['Designation']]["CashFlow"].values[0]
        elif 'PortfolioName' in kwargs:
            return self.dilution_df[self.dilution_df["PortfolioName"] == kwargs['PortfolioName']]["CashFlow"].values[0]


if __name__ == '__main__':
    positions = GetPositions()
    print(f"Positions using pID: {positions.pid_positions(1).to_string()}")
    print(f"Positions using Designation: {positions.designation_positions(392125).to_string()}")
    print(f"Fund Trend using Designation: {positions.designation_trend('392125').to_string()}")
    print(f"Cashflow using Designation: {positions.get_cashflow(Designation=392125)}")
    print(f"Cashflow using PortfolioName: {positions.get_cashflow(PortfolioName='Providence Strategy')}")
