# I might be over complicating this. Do I need to have seperate classes with inheritence or could I just have a
# single class with various methods and sub methods for definitions?
class Variables:
    def __init__(self, holdings_df, portfolio_df, performance_df):
        self.port_df = portfolio_df
        self.client_name = None
        self.margetts_portfolio_identifier = None
        self.date_provided = None
        self.performance_end_date = None
        self.new_paragraph = None
        self.intro_text = None
        self.margetts_equity = None
        self.client_equity = None
        self.client_equity_higher_lower = None
        self.client_emerging_markets = None
        self.client_emerging_markets_higher_lower = None
        self.margetts_emerging_markets = None
        self.margetts_developed_markets = None
        self.client_portfolio_risk_rating = None
        self.client_developed_markets = None
        self.margetts_cash_bond = None
        self.client_cash_bond_higher_lower = None
        self.client_cash_bond = None
        self.asset_allocation_text = None
        self.def_vars(portfolio_df)

    def _find_margetts_equity(self):
        for row, value in enumerate(self.port_df.iloc[:, 0]):
            try:
                if 'Equity' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 1]*100)
                    return to_return
            except TypeError:
                pass


    def def_vars(self, df):
        self.client_name = df.iloc[2, 0]
        self.margetts_portfolio_identifier = df.iloc[1, 0]
        self.margetts_portfolio_identifier = self.margetts_portfolio_identifier[12:]
        self.date_provided = df.iloc[18, 7].strftime('%d/%m/%Y')
        self.performance_end_date = df.iloc[19, 7].strftime('%d/%m/%Y')
        self.new_paragraph = '\n\n'
        self.margetts_equity = self._find_margetts_equity()
        self.client_equity = None
        self.client_equity_higher_lower = None
        self.client_emerging_markets = None
        self.client_emerging_markets_higher_lower = None
        self.margetts_emerging_markets = None
        self.margetts_developed_markets = None
        self.client_portfolio_risk_rating = None
        self.client_developed_markets = None
        self.margetts_cash_bond = None
        self.client_cash_bond_higher_lower = None
        self.client_cash_bond = None
        self.asset_allocation_text = None

    @staticmethod
    def _check_if_round_num(num):
        if num % 1 == 0:
            return int(num)
        else:
            return num


class Intro(Variables):
    def __init__(self, holdings_df, portfolio_df, performance_df):
        super().__init__(holdings_df, portfolio_df, performance_df)
        self.write_introduction()

    def write_introduction(self):
        self.intro_text = f"In the below report, {self.client_name}'s portfolio is compared to the Margetts Risk Rated " \
                          f"{self.margetts_portfolio_identifier} model portfolio. Performance of {self.client_name}" \
                          f"'s portfolio has been back tested using the latest portfolio positioning provided. " \
                          f"To compare the client’s portfolio to the Margetts Risk Rated" \
                          f" {self.margetts_portfolio_identifier} " \
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

class AssetAllocation(Variables):
    def __init__(self, holdings_df, portfolio_df, performance_df):
        super().__init__(holdings_df, portfolio_df, performance_df)
        self.write_asset_allocation()

    def write_asset_allocation(self):
        self.asset_allocation_text = f"In this report, {self.client_name}'s portfolio is compared to the Margetts " \
                                     f"Risk " \
                                     f"Rated {self.margetts_portfolio_identifier} model portfolio. Margetts assesses " \
                                     f"the " \
                                     f"risk " \
                                     f"profile of a portfolio by comparing collective cash and fixed interest weightings " \
                                     f"(assumed to be lower risk assets) and equities (assumed to be higher risk assets). " \
                                     f"The client's portfolio has a cash and bond exposure o" \
                                     f"f {self.client_cash_bond}%, " \
                                     f"which is {self.client_cash_bond_higher_lower} than that of the Margetts Risk " \
                                     f"Rated " \
                                     f"{self.margetts_portfolio_identifier} strategy, with a combined allocation of " \
                                     f"{self.margetts_cash_bond}%. Margetts believes that identifying the split " \
                                     f"between " \
                                     f"Western developed equities (UK, North America, and Europe) and developing markets " \
                                     f"/ Asian equities (Asia Pacific, Japan, and Emerging Markets) is useful when examining " \
                                     f"the risk of the equity allocation within a portfolio. {self.client_name}'s " \
                                     f"portfolio has a " \
                                     f"{self.client_developed_markets}% allocation to developed Western economies, " \
                                     f"whereas the " \
                                     f"Margetts {self.margetts_portfolio_identifier} portfolio holds a" \
                                     f" {self.margetts_developed_markets}% " \
                                     f"exposure. The Margetts {self.margetts_portfolio_identifier} portfolio " \
                                     f"allocates" \
                                     f" {self.margetts_emerging_markets}% to developing and Asian economies, " \
                                     f"and the client's " \
                                     f"portfolio has a {self.client_emerging_markets_higher_lower} allocation of" \
                                     f" {self.client_emerging_markets}%. " \
                                     f"Equities within developing regions and Asia tend to be higher risk than those " \
                                     f"within developed Western economies due to the prevalence of corruption, lower " \
                                     f"corporate governance standards, and a relatively less stable political backdrop. " \
                                     f"As a result, Margetts classifies Asian and developing market equities as " \
                                     f"relatively higher risk. Overall, the client's portfolio has a" \
                                     f" {self.client_cash_bond_higher_lower} exposure to cash and bonds (" \
                                     f"approximately " \
                                     f"{self.client_cash_bond}% compared to {self.margetts_cash_bond}%) and a" \
                                     f" {self.client_equity_higher_lower} exposure to equities (approximately " \
                                     f"{self.client_equity}% compared to {self.margetts_equity}%). Due to the asset " \
                                     f"allocation " \
                                     f"of the client's portfolio, Margetts suggests that the client's portfolio has a " \
                                     f"{self.client_portfolio_risk_rating} risk when compared to the Margetts " \
                                     f"portfolio."