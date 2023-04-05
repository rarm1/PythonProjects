
class Intro:
    def __init__(self):
        self.client_name = None
        self.margetts_portfolio_identifier = None
        self.date_provided = None
        self.performance_end_date = None
        self.new_paragraph = None
        self.intro_text = None
        self.def_vars()
        self.write_introduction()

    # These need to be dynamic variables retrieved from the Excel file.
    def def_vars(self):
        self.client_name = 'client_name'
        self.margetts_portfolio_identifier = 'margetts_portfolio_identifier'
        self.date_provided = 'date_provided'
        self.performance_end_date = 'performance_end_date'
        self.new_paragraph = 'new_paragraph'

    def write_introduction(self):
        self.intro_text = f"""
        Introduction\tVariables List
        In the below report, {self.client_name}
        {self.client_name}\t{self.margetts_portfolio_identifier}
        's portfolio is compared to the Margetts Risk Rated {self.new_paragraph}
        {self.margetts_portfolio_identifier}\t{self.date_provided}
         model portfolio. Performance of {self.performance_end_date}
        {self.client_name}
        's portfolio has been back tested using the latest portfolio positioning provided. To compare the client’s portfolio to the Margetts Risk Rated 
        {self.margetts_portfolio_identifier}
         strategy, we have assessed their geographical and asset class allocations. The asset allocation for the Margetts portfolio referenced in the following report refers to the long-term strategic asset allocation.
        {self.new_paragraph}
        Margetts have compared the back tested performance of the client’s portfolio using holdings and weightings provided to us on 
        {self.date_provided}
        . This analysis does not reflect the performance achieved by the client’s account and only provides an indication of the current client portfolio’s expected risk and return characteristics. All performance data has been sourced from Morningstar. All performance figures have been run to 
        {self.performance_end_date}
        .
        """
