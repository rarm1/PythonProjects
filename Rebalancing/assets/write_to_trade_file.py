import os
import pandas as pd
# Column headers are: FMDealingCode	TradeIdentifier	TradeFileDate	SchemeIdentifier	SecurityName	SecurityIdentifier	NewSecurity	Direction	DealType	Value	SettlementCurrency	PreviouslyReported	Notes
HEADERS = ["FMDealingCode", "TradeIdentifier", "TradeFileDate", "SchemeIdentifier", "SecurityName", "SecurityIdentifier", "NewSecurity", "Direction", "DealType", "Value", "SettlementCurrency", "PreviouslyReported", "Notes"]
TRADE_FILE_PATH = r"X:\Fund Management\Fund Management Team Files\FM Personal " \
                  r"Folders\Richard\PycharmProjects\Rebalancing\assets\trade_files"

class TradeWriter:
    def __init__(self, all_funds):
        self.all_funds = all_funds
        self._create_trade_file()
        self.identify_trades()
        # Set dealing Code
        self.traded["FMDealingCode"] = "RICHARD"
        # Set Trade Identifier
        # This is reading from a file and incrementing the number
        # For now this can increment from 1 each time
        self.traded["TradeIdentifier"] = 1
        # Set Trade File Date as todays date
        self.traded["TradeFileDate"] = pd.to_datetime("today").strftime("%d/%m/%Y")
        # Set Scheme Identifier
        # This is a lookup in the pID get set function that I've created.
        # Set Security Name
        self.traded["SecurityName"] = self.traded["Description"]
        # Set Security Identifier
        self.traded["SecurityIdentifier"] = self.traded["ISIN"]
        # Set New Security
        self.traded["NewSecurity"] = self.traded["Initial Market Value"].apply(lambda x: "Y" if x == 0 else "N")
        # Set Direction
        self.traded["Direction"] = self.traded["Trade Amount"].apply(lambda x: "Buy" if x > 0 else "Sell")
        # Set Deal Type
        # Integrate units and cash trades. Need live pricing for units.
        self.traded["DealType"] = "CASH"
        # Set Value
        self.traded["Value"] = self.traded["Trade Amount"]  # for now
        # Set Settlement Currency
        self.traded["SettlementCurrency"] = "GBP"
        # Set Previously Reported
        self.traded["PreviouslyReported"] = "N"
        # Set Notes
        self.traded["Notes"] = "Rebalancing"    # for now



    def _create_trade_file(self):
        if not os.path.exists(TRADE_FILE_PATH):
            os.makedirs(TRADE_FILE_PATH)

        path = os.path.join(TRADE_FILE_PATH, "manager_date.csv")
        # if the file doesn't exist then create it and add the headers
        with open(path, "w") as f:
            f.write(",".join(HEADERS) + "\n")

    def identify_trades(self):
        self.traded = self.all_funds[self.all_funds["Traded"] == True]


if __name__ == '__main__':
    df = pd.read_csv(r"X:\Fund Management\Fund Management Team Files\FM Personal "
                     r"Folders\Richard\PycharmProjects\Rebalancing\Clarion\Navigator.csv")
    TradeWriter(df)