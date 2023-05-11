# TODO: Best way to link fund group to specific strategies. Dictionary with fund group as key and list of strategies as value?
# 1	Providence Strategy
# 2	Select Strategy
# 3	International Strategy
# 4	Venture Strategy
# 25	Opes Growth
# 26	Opes Income
# 65	Future Money Real Growth
# 66	Future Money Real Value
# 67	Future Money Income
# 68	Future Money Dynamic Growth
# 169	Prima Cautious Fund
# 171	Prima Balanced Fund
# 172	Prima Adventurous Fund
# 176	Sample 08:30 VP
# 199	Blenheim Diversified Fixed Income Fund
# 200	Blenheim Overseas Equity Fund
# 201	Blenheim UK Equity Fund
# 202	Blenheim Diversified Property Fund
# 203	Blenheim Diversified Alternatives Fund
# 204	Blenheim Ethical Opportunities Fund
# 212	Progeny Dynamic Equity
# 213	Progeny Dynamic Bond
# 214	Progeny Systematic Equity
# 215	Progeny Systematic Bond
# 229	Progeny ProFolio Model 30-50% Shares
# 230	Progeny ProFolio Model 50-70% Shares
# 231	Progeny ProFolio Model 70-90% Shares
# 232	SIIION Cautious Fund
# 233	SIIION Balanced Fund
# 234	SIIION Adventurous Fund

def main():
    execution = True
    # This variable is to link fund group to the pIDs of specific strategies.
    fund_group = {"Aequitas": ["NA"], "Clarion": [], "IBOSS": [], "Opes": [25, 26], "PRIMA": [169, 171, 172],
                  "Risk Rated": [], "Tempus": []}
    [print(f"{i+1}. {fund_group}") for i, fund_group in enumerate(fund_group)]
    # while execution:
    rebalancing_list = input("Enter the index of the strategy you want to rebalance.\n"
          "This can either be a single number or a comma seperated list, i.e. (1, 2, 4): ")
    rebalancing_list = rebalancing_list.replace(" ", "").split(",")
    rebalancing_list = [int(i) for i in rebalancing_list]

    for i in rebalancing_list:
        print(fund_group[i-1])
        # execution = False


if __name__ == '__main__':
    main()
