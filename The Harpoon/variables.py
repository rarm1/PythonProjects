# I might be over complicating this. Do I need to have seperate classes with inheritence or could I just have a
# single class with various methods and sub methods for definitions?
class Variables:
    def __init__(self, holdings_df, portfolio_df, performance_df):
        self.client_name = None
        self.margetts_portfolio_identifier = None
        self.date_provided = None
        self.performance_end_date = None
        self.new_paragraph = None
        self.intro_text = None
        self.def_vars(portfolio_df)

    def def_vars(self, df):
        self.client_name = df.iloc[2, 0]
        self.margetts_portfolio_identifier = df.iloc[1, 0]
        self.margetts_portfolio_identifier = self.margetts_portfolio_identifier[12:]
        self.date_provided = df.iloc[18, 7].strftime('%d/%m/%Y')
        self.performance_end_date = df.iloc[19, 7].strftime('%d/%m/%Y')
        self.new_paragraph = '\n\n'

class Intro(Variables):
    def __init__(self, holdings_df, portfolio_df, performance_df):
        super().__init__(holdings_df, portfolio_df, performance_df)
        self.intro_text = None
        self.write_introduction()

    def write_introduction(self):
        self.intro_text = f"In the below report, {self.client_name}'s portfolio is compared to the Margetts Risk Rated " \
                          f"{self.margetts_portfolio_identifier} model portfolio. Performance of {self.client_name}" \
                          f"'s portfolio has been back tested using the latest portfolio positioning provided. " \
                          f"To compare the client’s portfolio to the Margetts Risk Rated" \
                          f"{self.margetts_portfolio_identifier}" \
                          f"strategy, we have assessed their geographical and asset class allocations. " \
                          f"The asset allocation for the Margetts portfolio referenced in the following" \
                          f"report refers to the long-term strategic asset allocation." \
                          f"{self.new_paragraph}" \
                          f"Margetts have compared the back tested performance of the client’s portfolio " \
                          f"using holdings and weightings provided to us on {self.date_provided}" \
                          f". This analysis does not reflect the performance achieved by the client’s account " \
                          f"and only provides an indication of the current client portfolio’s expected risk " \
                          f"and return characteristics. All performance data has been sourced from Morningstar. " \
                          f"All performance figures have been run to " \
                          f"{self.performance_end_date}."
