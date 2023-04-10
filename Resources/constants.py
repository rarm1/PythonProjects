# TODO: Move all resources into this folder multi-use files as well as
# TODO: Remove single use values
# TODO: Refactor to be OO
global READER_SHEET

# Variable initialisation for rebalancing limits.
FUND_MAX_THRESHOLD = 0.01
FUND_TRADING_LIMITS = 0.005
BUCKET_TRADE_INITIALISER = 0.005
BUCKET_TRADE_GOAL = 0.003
BOND_SECTOR_TRADE_INITIALISER = 0.005
BOND_SECTOR_TRADING_GOAL = 0.003
EQUITY_SECTOR_TRADE_INITIALISER = 0.005
EQUITY_SECTOR_TRADING_GOAL = 0.003
CASH_SECTOR_TRADE_INITIALISER = 0.005
CASH_SECTOR_TRADING_GOAL = 0.003
TRADE_SHEET_HEADERS = ['Transaction Date', 'Share_Class_Name_Long', 'AccInc', 'DealRef', 'TradeType', 'InvestorCode',
                       'InvestorSalutation', 'Designation', 'UniqueKey', 'PortfolioNumber', 'ProductCode',
                       'WrapperType',
                       'Units', 'Price Per Unit', 'Cost To Holder']


def adjustment_cash_cell_finder():
    for a in range(1, READER_SHEET.max_row):
        cell = READER_SHEET.cell(a, 2)
        if cell.value == "Adjustment Cash":
            return cell


def cash_figure():
    return adjustment_cash_cell_finder().offset(1, 4)


def total_portfolio_value():
    """
    Finds the cell that lists the total portfolio value.
    :return: Cell
    """
    return adjustment_cash_cell_finder().offset(3, 4)


def get_total_target():
    for a in range(1, READER_SHEET.max_row):
        cell = READER_SHEET.cell(a, 11)
        if cell.value == "Total Deals":
            return cell.offset(-2, 0)


def get_cash_target():
    return get_total_target().offset(-2, 0)


def bond_sector_start_point():
    for a in range(1, READER_SHEET.max_row):
        cell = READER_SHEET.cell(a, 5)
        if cell.value == "Bonds":
            return cell


def bond_sector_end_point():
    for a in range(bond_sector_start_point().row, READER_SHEET.max_row):
        cell = READER_SHEET.cell(a, 5)
        if cell.value == "Total Bonds + Property":
            return cell


def equity_sector_start_point():
    for a in range(bond_sector_end_point().row, bond_sector_end_point().row + 5):
        cell = READER_SHEET.cell(a, 5)
        if cell.value == "Equities":
            return cell


def equity_sector_end_point():
    for a in range(equity_sector_start_point().row, READER_SHEET.max_row):
        cell = READER_SHEET.cell(a, 5)
        if cell.value == "Total Equities":
            return cell


def bonds_sector():
    all_stable_sector_return = []
    for a in range(bond_sector_start_point().row + 1, bond_sector_end_point().row):
        cell = READER_SHEET.cell(a, 5)
        all_stable_sector_return.append(cell)
    else:
        return all_stable_sector_return


def equities_sector():
    all_equities = []
    for a in range(equity_sector_start_point().row + 1, equity_sector_end_point().row):
        cell = READER_SHEET.cell(a, 5)
        all_equities.append(cell)
    return all_equities


def all_buckets():
    to_write = []
    for x in bonds_sector():
        to_write.append(x)
    for x in equities_sector():
        to_write.append(x)
    to_write.append(money_markets_bucket())
    return to_write


def all_buckets_no_mm():
    to_write = []
    for x in bonds_sector():
        to_write.append(x)
    for x in equities_sector():
        to_write.append(x)
    return to_write


def money_markets_bucket():
    for x in range(equity_sector_end_point().row, equity_sector_end_point().row + 5):
        cell = (READER_SHEET.cell(x, 5))
        if cell.value == "CASH/MONEY MARKETS":
            return cell


def money_market_funds_finder():
    all_money_markets = []
    for x in all_funds():
        if x.offset(0, 4).value == "CASH/MONEY MARKETS":
            all_money_markets.append(x.offset(0, -6))
    return all_money_markets


def all_funds():
    last_fund = None
    for a in range(adjustment_cash_cell_finder().row, 1, -1):
        cell_check = READER_SHEET.cell(a, 5)
        if cell_check.value is not None:
            last_fund = READER_SHEET.cell(a + 1, 5)
            break
    fund_arr = []
    for a in range(7, last_fund.row):
        if READER_SHEET.cell(a, 12).value is not None:
            fund_arr.append(READER_SHEET.cell(a, 12))
    return fund_arr


def find_funds(bucket_to_trade):
    """
    Find funds that are within a specific bucket.
    :param bucket_to_trade: Bucket, as a cell.
    :return: All funds within bucket.
    """
    to_return = []
    for x in all_funds():
        if x.offset(0, 4).value is not None:
            if isinstance(bucket_to_trade, str):
                if x.offset(0, 4).value.lower() == bucket_to_trade.lower():
                    to_return.append(x)
            else:
                if x.offset(0, 4).value.lower() == bucket_to_trade.value.lower():
                    to_return.append(x)
    return to_return


def bucket_identifier(fund):
    """
    This takes a fund, and finds the bucket it is part of. Used for rebalancer.
    :param fund:
    :return:
    """
    sector_to_find = (fund.offset(0, 4))
    for x in all_buckets():
        if x.value.lower() == sector_to_find.value.lower():
            return x


def find_bond_sector_dtt():
    sector_dtt: int = 0
    for bucket in bonds_sector():
        funds_in_bucket = find_funds_in_bucket(bucket.value)[0]
        if len(funds_in_bucket) != 0:
            bucket_dtt = 0
            for fund in funds_in_bucket:
                existing_trade = fund.offset(0, 2).value
                if existing_trade is not None:
                    trade_write = fund.value - existing_trade
                else:
                    trade_write = fund.value
                bucket_dtt += trade_write
            else:
                sector_dtt += bucket_dtt
    else:
        return sector_dtt


def bond_sector_traded():
    for bucket in bonds_sector():
        funds_in_bucket = find_funds_in_bucket(bucket.value)[0]
        if len(funds_in_bucket) != 0:
            for fund in funds_in_bucket:
                if fund.offset(0, 2).value is not None:
                    return True
    else:
        return False


def equity_sector_traded():
    for bucket in equities_sector():
        funds_in_bucket = find_funds_in_bucket(bucket.value)[0]
        if len(funds_in_bucket) != 0:
            for fund in funds_in_bucket:
                if fund.offset(0, 2).value is not None:
                    return True
    else:
        return False


def mm_sector_traded():
    funds_in_bucket = find_funds_in_bucket(money_markets_bucket().value)[0]
    if len(funds_in_bucket) != 0:
        for fund in funds_in_bucket:
            if fund.offset(0, 2).value is not None:
                return True
    return False


def find_equity_sector_dtt():
    sector_dtt = 0
    for bucket in equities_sector():
        funds_in_bucket = find_funds_in_bucket(bucket.value)[0]
        if len(funds_in_bucket) != 0:
            bucket_dtt = 0
            for fund in funds_in_bucket:
                existing_trade = fund.offset(0, 2).value
                if existing_trade is not None:
                    trade_write = fund.value - existing_trade
                else:
                    trade_write = fund.value
                bucket_dtt += trade_write
            else:
                sector_dtt += bucket_dtt
    else:
        return sector_dtt


def find_mm_dtt():
    sector_dtt = 0
    funds_in_bucket = find_funds_in_bucket(money_markets_bucket().value)[0]
    if len(funds_in_bucket) != 0:
        bucket_dtt = 0
        for fund in funds_in_bucket:
            existing_trade = fund.offset(0, 2).value
            if existing_trade is not None:
                trade_write = fund.value - existing_trade
            else:
                trade_write = fund.value
            if trade_write is not None:
                bucket_dtt += trade_write
        else:
            sector_dtt += bucket_dtt
        return sector_dtt


def find_funds_in_bucket(bucket):
    """
    :param bucket: String
    :return: Array, int
    """
    funds_in_bucket, found_trades, dtt_bucket = [], [], 0
    for fund_deal_to_target in all_funds():
        if fund_deal_to_target.offset(0, 4).value.lower() == bucket.lower():
            existing_trade = fund_deal_to_target.offset(0, 2).value
            if existing_trade is not None:
                write_value = fund_deal_to_target.value - existing_trade
                found_trades.append([fund_deal_to_target, existing_trade])
            else:
                write_value = fund_deal_to_target.value
            funds_in_bucket.append(fund_deal_to_target)
            dtt_bucket += write_value
    else:
        return funds_in_bucket, dtt_bucket


def all_bucket_deal_to_target(buckets=all_buckets):
    """
    Get aggregate deal to target.
    :param buckets: String
    :return: Dictionary
    """
    funds_dict = {}
    for bucket in buckets():
        funds_dict[bucket.value] = 0
        for fund in all_funds():
            if bucket.value.lower() == fund.offset(0, 4).value.lower():
                if fund.offset(0, 2).value is not None:
                    funds_dict[bucket.value] += (fund.value - fund.offset(0, 2).value)
                else:
                    funds_dict[bucket.value] += fund.value
    else:
        keys = [k for k, v in funds_dict.items() if v == 0]
        for x in keys:
            del (funds_dict[x])
        else:
            return funds_dict


def sector_deal_to_target(bucket_to_id):
    if bucket_to_id in equities_sector():
        return find_equity_sector_dtt()
    if bucket_to_id in bonds_sector():
        return find_bond_sector_dtt()
    if bucket_to_id == money_markets_bucket():
        return find_mm_dtt()
