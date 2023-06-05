import sys

class Report:
    def __init__(self, holdings_df, portfolio_df, performance_df):
        self.client_equity = None
        self.client_cash_bond = None
        self.annualised_performance_calc = None
        self.top_five_strategies = None
        self.margetts_cash_bond = None
        self.client_cash_bond_higher_lower = None
        self.three_y_performance_margetts = None
        self.three_y_performance_client = None
        self.three_y_margetts_relative_performance = None
        self.one_y_performance_margetts = None
        self.one_y_performance_client = None
        self.one_y_margetts_relative_performance = None
        self.ytd_performance_margetts = None
        self.ytd_performance_client = None
        self.ytd_margetts_relative_performance = None
        self.client_developed_markets = None
        self.margetts_developed_markets = None
        self.client_portfolio_risk_rating = None
        self.asset_allocation_text = None
        self.five_y_performance_margetts = None
        self.five_y_performance_client = None
        self.five_y_margetts_relative_performance = None
        self.margetts_equity = None
        self.client_equity_higher_lower = None
        self.client_emerging_markets = None
        self.margetts_emerging_markets = None
        self.client_emerging_markets_higher_lower = None
        self.ytd_margetts_relative_performance = None
        self.client_cash_bond = None
        self.new_paragraph = None
        self.performance_end_date = None
        self.date_provided = None
        self.margetts_portfolio_identifier = None
        self.client_name = None
        self.ongoing_charges_text = None
        self.performance_text = None
        self.asset_allocation_text = None
        self.intro_text = None
        self.port_df = portfolio_df
        self._initialize_variables()
        self.perf_df = performance_df
        self.def_vars(holdings_df, portfolio_df, performance_df)
        self.write_introduction()
        self.write_asset_allocation()
        self.write_performance()
        self.write_ongoing_charges()


    def write_introduction(self):
        self.intro_text = f"In the below report, {self.client_name}'s portfolio is compared to the Margetts Risk Rated " \
                          f"{self.margetts_portfolio_identifier} model portfolio. Performance of {self.client_name}" \
                          f"'s portfolio has been back tested using the latest portfolio positioning provided. " \
                          f"To compare the client’s portfolio to the Margetts Risk Rated" \
                          f" {self.margetts_portfolio_identifier} strategy, we have assessed their geographical " \
                          f"and asset class allocations. The asset allocation for the Margetts portfolio referenced " \
                          f"in the following report refers to the long-term strategic asset allocation." \
                            f"{self.new_paragraph}" \
                          f"Margetts have compared the back tested performance of the client’s portfolio " \
                          f"using holdings and weightings provided to us on {self.date_provided}" \
                          f". This analysis does not reflect the performance achieved by the client’s account " \
                          f"and only provides an indication of the current client portfolio’s expected risk " \
                          f"and return characteristics. All performance data has been sourced from Morningstar. " \
                          f"All performance figures have been run to {self.performance_end_date}." \
                            f"{self.new_paragraph}"

    def write_asset_allocation(self):
        self.asset_allocation_text = f"In this report, {self.client_name}'s portfolio is compared to the Margetts " \
                             f"Risk Rated {self.margetts_portfolio_identifier} model portfolio. Margetts assess " \
                             f"the risk profile of a portfolio by comparing collective cash and fixed interest " \
                             f"weightings (assumed to be lower risk assets) and equities (assumed to be higher risk " \
                             f"assets). The client's portfolio has a cash and bond exposure of {self.client_cash_bond}%," \
                             f" which is {self.client_cash_bond_higher_lower} that of the Margetts Risk " \
                             f"Rated {self.margetts_portfolio_identifier} strategy, which has a combined allocation " \
                             f"of {self.margetts_cash_bond}%. " \
                                     f"{self.new_paragraph}" \
                             f"Margetts believe that identifying the split between Western developed equities " \
                             f"(UK, North America, and Europe) and developing markets / Asian equities " \
                             f"(Asia Pacific, Japan, and Emerging Markets) is useful when examining  the risk of the " \
                             f"equity allocation within a portfolio. {self.client_name}'s portfolio has a " \
                             f"{self.client_developed_markets}% allocation to developed Western economies, " \
                             f"whereas the Margetts {self.margetts_portfolio_identifier} portfolio holds a" \
                             f" {self.margetts_developed_markets}% exposure. " \
                                     f"{self.new_paragraph}" \
                             f"The Margetts {self.margetts_portfolio_identifier} portfolio allocates " \
                             f"{self.margetts_emerging_markets}% to developing and Asian economies, " \
                             f"and the client's portfolio has a {self.client_emerging_markets_higher_lower} allocation " \
                             f"of {self.client_emerging_markets}%. Equities within developing regions and Asia tend to " \
                             f"be higher risk than those within developed Western economies due to the prevalence of " \
                             f"corruption, lower corporate governance standards, and a relatively less stable " \
                             f"political backdrop. As a result, Margetts classifies Asian and developing market equities" \
                             f" as relatively higher risk. " \
                                     f"{self.new_paragraph}" \
                             f"Overall, the client's exposure to cash and bonds is {self.client_cash_bond_higher_lower} " \
                             f"(approximately {self.client_cash_bond}% compared to {self.margetts_cash_bond}%). " \
                             f"The client's exposure to equities is {self.client_equity_higher_lower} the Margetts " \
                             f"{self.margetts_portfolio_identifier} (approximately {self.client_equity}% compared to " \
                             f"{self.margetts_equity}%). Due to the asset allocation of the client's portfolio, Margetts" \
                             f" suggest that the client's portfolio has a {self.client_portfolio_risk_rating} risk when" \
                             f" compared to the Margetts Risk Rated {self.margetts_portfolio_identifier} portfolio." \
                                     f"{self.new_paragraph}"

    def write_performance(self):
        self.performance_text = (f"Over 5 years, an investment into Margetts Risk Rated "
                                 f"{self.margetts_portfolio_identifier} would have returned c."
                                 f"{self.five_y_performance_margetts}%, "
                                 f"{self.five_y_margetts_relative_performance} the back tested performance "
                                 f"of the portfolio held by {self.client_name} at c."
                                 f"{self.five_y_performance_client}%, as shown on the chart below."
                                    f"{self.new_paragraph}"
                                 f"Over 3 years, an investment into Margetts Risk Rated "
                                 f"{self.margetts_portfolio_identifier} would have returned c."
                                 f"{self.three_y_performance_margetts}%, which is "
                                 f"{self.three_y_margetts_relative_performance} "
                                 f"{self.client_name}'s portfolio which would have returned c."
                                 f"{self.three_y_performance_client}% over the same period, as shown on the chart below."
                                    f"{self.new_paragraph}"
                                 f"Over 1 year, the Margetts RR {self.margetts_portfolio_identifier} "
                                 f"strategy performed {self.one_y_margetts_relative_performance} "
                                 f"the client's portfolio. This is shown on the chart below, with Margetts RR "
                                 f"{self.margetts_portfolio_identifier} returning c."
                                 f"{self.one_y_performance_margetts}% and {self.client_name}"
                                 f"'s portfolio returning c.{self.one_y_performance_client}%."
                                    f"{self.new_paragraph}"
                                 f"Over the year to date ({self.performance_end_date}), the Margetts RR "
                                 f"{self.margetts_portfolio_identifier} strategy performed "
                                 f"{self.ytd_margetts_relative_performance} the client's portfolio. "
                                 f"This is demonstrated on the chart below, with Margetts "
                                 f"{self.margetts_portfolio_identifier} returning c.{self.ytd_performance_margetts}% "
                                 f"and the client's portfolio returning c.{self.ytd_performance_client}%."
                                    f"{self.new_paragraph}"
                                 f"{self.annualised_performance_calc}"
                                    f"{self.new_paragraph}"
                                 f"While {self.client_name}'s portfolio is reasonably well diversified geographically, "
                                 f"it is relatively highly concentrated. The top 5 strategies in {self.client_name}'s portfolio "
                                 f"account for c.{self.top_five_strategies}% of the overall portfolio. Each Margetts fund "
                                 f"holds between 12-18 strategies at between 4% and 8% weightings, meaning the largest "
                                 f"5 individual holdings could account for a maximum of 40% of the portfolio, although this "
                                 f"level of concentration is typically avoided by Margetts. This level of concentration within "
                                 f"the client's portfolio may add to the perceived idiosyncratic risk of {self.client_name}'s "
                                 f"portfolio. The Margetts Risk Rated strategies attempt to reduce this risk by implementing "
                                 f"the above diversification strategies."
                                    f"{self.new_paragraph}")

    def annualised_calc(self):
        start = False
        margetts_outperform_years = []
        client_outperform_years = []
        equal_years = []

        for row, value in enumerate(self.perf_df.iloc[:, 0]):
            performance_period = str(self.perf_df.iloc[row, 0])

            if performance_period == "YTD":
                performance_period = "the year to date (" + self.performance_end_date + ")"

            if start:
                difference = self.perf_df.iloc[row, 1] - self.perf_df.iloc[row, 2]
                if difference > 0.01:
                    margetts_outperform_years.append(performance_period)
                elif difference < -0.01:
                    client_outperform_years.append(performance_period)
                else:
                    equal_years.append(performance_period)
            if value == "Annualised":
                start = True
        if len(margetts_outperform_years) >= 2:
            margetts_outperform_years[-1] = "and " + margetts_outperform_years[-1]
        margetts_outperform_years_str = ", ".join(margetts_outperform_years)
        if len(client_outperform_years) >= 2:
            client_outperform_years[-1] = "and " + client_outperform_years[-1]
        client_outperform_years_str = ", ".join(client_outperform_years)

        if len(equal_years) >= 2:
            equal_years[-1] = "and " + equal_years[-1]
        equal_years_str = ", ".join(equal_years)

        to_return = ["The below chart shows discrete annual performance for the last 5 years."]
        if len(margetts_outperform_years) > 0:
            rr_outperform = (f"The Margetts Risk Rated {self.margetts_portfolio_identifier} model, "
                                 f"performed ahead of {self.client_name}'s portfolio across "
                                 f"{margetts_outperform_years_str}.")
            to_return.append(rr_outperform)

        if len(client_outperform_years) > 0:
            client_outperform = (f"{self.client_name}'s portfolio outperformed the Margetts strategy in "
                                     f"{client_outperform_years_str}.")
            to_return.append(client_outperform)

        if len(equal_years) > 0:
            in_line = f"The two portfolios performed in line across {equal_years_str}."
            to_return.append(in_line)
        to_return = " ".join(to_return)
        return to_return

    def write_ongoing_charges(self):
        self.ongoing_charges_text = f"{self.client_name}'s portfolio has a {self.client_cash_bond_higher_lower} " \
                                    f"exposure to cash and bonds compared to the Margetts RR " \
                                    f"{self.margetts_portfolio_identifier} strategy. " \
                                    f"{self.client_name}'s portfolio has a {self.client_emerging_markets_higher_lower} " \
                                    f"exposure to emerging markets when compared to the Margetts RR " \
                                    f"{self.margetts_portfolio_identifier} strategy. The greater level of diversification " \
                                    f"within the Margetts strategy may also be a contributory factor towards the risk profile " \
                                    f"of the two portfolios when compared to one another. When summarising the risk levels of " \
                                    f"the two strategies, the Margetts RR {self.margetts_portfolio_identifier} strategy would " \
                                    f"be considered to have marginally less risk appetite when compared to {self.client_name}'s " \
                                    f"portfolio." \
                                        f"{self.new_paragraph}" \
                                    f"The below table details the weighted average of underlying " \
                                    f"ongoing charges of the funds included in {self.client_name}’s portfolio and the weighted " \
                                    f"average ongoing charge of the Margetts funds included in the Margetts Risk Rated " \
                                    f"{self.margetts_portfolio_identifier} strategy." \
                                        f"{self.new_paragraph}"

    def _initialize_variables(self):
        variables_list = ['client_name', 'margetts_portfolio_identifier', 'date_provided', 'performance_end_date',
                          'new_paragraph',
                          'intro_text', 'margetts_equity', 'client_equity', 'client_equity_higher_lower',
                          'client_emerging_markets',
                          'client_emerging_markets_higher_lower', 'margetts_emerging_markets',
                          'margetts_developed_markets',
                          'client_portfolio_risk_rating', 'client_developed_markets', 'margetts_cash_bond',
                          'client_cash_bond_higher_lower',
                          'client_cash_bond', 'asset_allocation_text',
                          'five_y_performance_margetts', 'five_y_margetts_relative_performance',
                          'five_y_performance_client', 'three_y_performance_margetts', 'three_y_margetts_relative_performance',
                          'three_y_performance_client', 'one_y_margetts_relative_performance', 'one_y_performance_margetts',
                          'one_y_performance_client', 'annualised_performance_calc', 'ytd_margetts_relative_performance',
                          'ytd_performance_margetts', 'ytd_performance_client', 'top_five_strategies',
                          'performance_text']
        for var in variables_list:
            setattr(self, var, None)

    def def_vars(self, holdings_df, portfolio_df, performance_df):
        self.client_name = portfolio_df.iloc[26, 7]
        self.margetts_portfolio_identifier = portfolio_df.iloc[1, 0]
        self.margetts_portfolio_identifier = self.margetts_portfolio_identifier[12:]
        self.date_provided = portfolio_df.iloc[18, 7].strftime('%d/%m/%Y')
        self.performance_end_date = portfolio_df.iloc[19, 7].strftime('%d/%m/%Y')
        self.new_paragraph = '\n\n'
        self.client_cash_bond = self._find_client_cash_bond()
        self.margetts_cash_bond = self._find_margetts_cash_bond()
        self.client_cash_bond_higher_lower = self.compare_client_cash_bond(client_equity=self.client_cash_bond,
                                                                          margetts_equity=self.margetts_cash_bond)
        self.client_equity = self._find_client_equity()
        self.margetts_equity = self._find_margetts_equity()
        self.client_equity_higher_lower = self.compare_client_equity(client_equity=self.client_equity,margetts_equity=self.margetts_equity)
        self.client_emerging_markets = self._find_client_em_equity()
        self.margetts_emerging_markets = self._find_margetts_em_equity()
        self.client_emerging_markets_higher_lower = self.compare_client_em_equity(client_equity=self.client_emerging_markets,
                                                                                  margetts_equity=self.margetts_emerging_markets)
        self.client_developed_markets = self._find_client_dm_equity()
        self.margetts_developed_markets = self._find_margetts_dm_equity()
        self.client_portfolio_risk_rating = self.find_client_portfolio_risk_rating()
        self.asset_allocation_text = None
        self.five_y_performance_margetts = self._check_if_round_num(performance_df.iloc[1, 1]*100)
        self.five_y_performance_client = self._check_if_round_num(performance_df.iloc[1, 2]*100)
        self.five_y_margetts_relative_performance = self.perf_check(self.five_y_performance_margetts,
                                                                    self.five_y_performance_client, 2)
        self.three_y_performance_margetts = self._check_if_round_num(performance_df.iloc[2, 1]*100)
        self.three_y_performance_client = self._check_if_round_num(performance_df.iloc[2, 2]*100)
        self.three_y_margetts_relative_performance = self.perf_check(self.three_y_performance_margetts,
                                                                     self.three_y_performance_client, 1)
        self.one_y_performance_margetts = self._check_if_round_num(performance_df.iloc[3, 1]*100)
        self.one_y_performance_client = self._check_if_round_num(performance_df.iloc[3, 2]*100)
        self.one_y_margetts_relative_performance = self.perf_check(self.one_y_performance_margetts,
                                                                   self.one_y_performance_client, 1)
        self.ytd_performance_margetts = self._check_if_round_num(performance_df.iloc[4, 1]*100)
        self.ytd_performance_client = self._check_if_round_num(performance_df.iloc[4, 2]*100)
        self.ytd_margetts_relative_performance = self.perf_check(self.ytd_performance_margetts,
                                                                 self.ytd_performance_client, 1)
        self.annualised_performance_calc = self.annualised_calc()
        self.top_five_strategies = self.client_holdings(holdings_df=holdings_df)
        self.performance_text = None
        self.ongoing_charges_text = None

    def _find_margetts_equity(self):
        for row, value in enumerate(self.port_df.iloc[:, 0]):
            try:
                if 'Equity' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 1] * 100)
                    return to_return
            except TypeError:
                pass

    def _find_client_equity(self):
        for row, value in enumerate(self.port_df.iloc[:, 3]):
            try:
                if 'Equity' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 4] * 100)
                    return to_return
            except TypeError:
                pass

    @staticmethod
    def _check_if_round_num(num):
        try:
            if round(num) == round(num, 1):
                return round(num)
            else:
                return round(num, 1)
        except ValueError:
            sys.exit("Error: Value Error in the performance table. Please check all performance figures are numbers "
                     "and present.")

    @staticmethod
    def compare_client_equity(client_equity, margetts_equity):
        difference = client_equity - margetts_equity
        if difference > 2:
            return "higher"
        elif difference < -2:
            return "lower"
        elif difference == 0.0:
            return "same"
        else:
            return "similar"

    def _find_client_em_equity(self):
        client_col = 3
        for row, value in enumerate(self.port_df.iloc[:, client_col]):
            try:
                if 'Emerging Markets' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, client_col+1] * 100)
                    return to_return
            except TypeError:
                pass

    def _find_margetts_em_equity(self):
        for row, value in enumerate(self.port_df.iloc[:, 0]):
            try:
                if 'Emerging Markets' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 1] * 100)
                    return to_return
            except TypeError:
                pass

    @staticmethod
    def compare_client_em_equity(client_equity, margetts_equity):
        difference = client_equity - margetts_equity
        if difference > 2:
            return "higher"
        elif difference < -2:
            return "lower"
        elif round(difference, 1) == 0.0:
            return "same"
        else:
            return "similar"

    def _find_client_dm_equity(self):
        for row, value in enumerate(self.port_df.iloc[:, 3]):
            try:
                if 'Developed Markets' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 4] * 100)
                    return to_return
            except TypeError:
                pass

    def _find_margetts_dm_equity(self):
        for row, value in enumerate(self.port_df.iloc[:, 0]):
            try:
                if 'Developed Markets' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 1] * 100)
                    return to_return
            except TypeError:
                pass

    def _find_client_cash_bond(self):
        for row, value in enumerate(self.port_df.iloc[:, 3]):
            try:
                if 'Client Cash' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 4] * 100)
                    return to_return
            except TypeError:
                pass

    def _find_margetts_cash_bond(self):
        for row, value in enumerate(self.port_df.iloc[:, 0]):
            try:
                if 'Margetts Cash' in value:
                    to_return = self._check_if_round_num(self.port_df.iloc[row, 1] * 100)
                    return to_return
            except TypeError:
                pass

    @staticmethod
    def compare_client_cash_bond(client_equity, margetts_equity):
        difference = client_equity - margetts_equity
        if difference > 2:
            return "higher than"
        elif difference < -2:
            return "lower than"
        elif difference == 0.0:
            return "the same as"
        else:
            return "similar to"

    def find_client_portfolio_risk_rating(self):
        margetts_risk_rating = 0
        client_risk_rating = 0
        for col, value in enumerate(self.port_df.iloc[0, :]):
            try:
                if 'Risk Score' in value:
                    margetts_risk_rating = self.port_df.iloc[1, col]
                    client_risk_rating = self.port_df.iloc[2, col]
            except TypeError:
                pass
        if margetts_risk_rating == client_risk_rating:
            return f"same"
        elif client_risk_rating > margetts_risk_rating:
            return f"higher"
        elif client_risk_rating < margetts_risk_rating:
            return f"lower"

    @staticmethod
    def perf_check(perf_1, perf_2, tolerance: int = 2):
        diff = perf_1 - perf_2
        if diff > tolerance:
            return "ahead of"
        elif diff < tolerance*-1:
            return "behind"
        else:
            return "in line with"

    @staticmethod
    def client_holdings(holdings_df):
        holdings_df.columns = holdings_df.iloc[0]
        holdings_df = holdings_df.drop(holdings_df.index[0])
        holdings_df = holdings_df.sort_values(by='% Holding', ascending=False)
        top_5_weightings = holdings_df.iloc[:5, 6].sum()
        return round(top_5_weightings, 1)
