import pandas as pd
pd.options.display.float_format = '{:.2f}'.format
class DilutionAdjustment:
    def __init__(self):
        use_cols = ['Designation', 'PortfolioName', 'CashFlow', 'NetAssetValue']
        self.df = pd.read_excel(r"X:\Fund Management\Fund Management Team Files\FM Personal "
                           r"Folders\Richard\PycharmProjects\Rebalancing\assets\Horizon Positions.xlsm",
                           sheet_name="DilutionAdjustment", engine='openpyxl', skiprows=2, usecols=use_cols,
                           dtype={'Designation': str, 'PortfolioName': str, 'CashFlow': float, 'NetAssetValue': float})

    def get_cashflow(self, **kwargs):
        if 'Designation' in kwargs:
            return self.df[self.df["Designation"] == kwargs['Designation']]["CashFlow"].values[0]
        elif 'PortfolioName' in kwargs:
            return self.df[self.df["PortfolioName"] == kwargs['PortfolioName']]["CashFlow"].values[0]


    def get_nav(self, **kwargs):
        if 'Designation' in kwargs:
            return self.df[self.df["Designation"] == kwargs['Designation']]["NetAssetValue"].values[0]
        elif 'PortfolioName' in kwargs:
            return self.df[self.df["PortfolioName"] == kwargs['PortfolioName']]["NetAssetValue"].values[0]


if __name__ == '__main__':
    da = DilutionAdjustment()
    print(da.df.to_string())
    print(f"Cashflow designation lookup: {da.get_cashflow(Designation='392212')}")
    print(f"Cashflow portfolio lookup: {da.get_cashflow(PortfolioName='Opes Growth')}")
    print(f"NAV designation lookup: {da.get_nav(Designation='392212')}")
    print(f"NAV portfolio lookup: {da.get_nav(PortfolioName='Opes Growth')}")
