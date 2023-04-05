# This current iteration of the rebalancer puts accuracy over trade quantity.
# This can be developed to reduce the amount of trades. But, in its current standing it will ALWAYS
# trade to requirements and not forego trade quality for trade quantity.
# Import libraries
import operator
import openpyxl as xl

# Import local libraries
from Resources import constants
from Resources import trade_writer
from Resources import file_id_reader

# Variable initialisation
global WRITER_SHEET, READER_SHEET, MODIFIED_FILENAME


# Trade any funds that are over 1% overweight. This function triggers a lot of incorrect trades.
def funds_overweight():
    for fund in (constants.all_funds()):
        # The fund.offset(0, 2) is the trading column. If there is already a trade, this must be taken into account.
        if fund.offset(0, 2).value is not None:
            check_val = fund.value - fund.offset(0, 2).value
        else:
            check_val = fund.value
        # This checks whether the fund DTT is larger than the fund threshold (usually 1%) of the portfolio.
        if abs(check_val) > (constants.total_portfolio_value().value * constants.FUND_MAX_THRESHOLD):
            trade_writer.single_trade_writer(fund, fund.value)


# If a trade is done to generate cash, it requires less processing than other trades.
def cash_exec(fund):
    """
    Takes a fund and pushes the trade through without processing. This saves time, processing power, and
    puts the focus on the cash balance of the fund
    :param fund: Cell
    :return: void
    """
    fund_deal = fund.value
    trade_writer.single_trade_writer(fund, fund_deal)


# This is for all trades not to generate cash, or rebalance an overweight fund.
def trade_execution(fund):
    """
    Takes a fund that requires a trade. Processes this trade and then returns.
    :param fund: Cell
    :return: Void
    """
    # Creating variables from fixed points avoids overwriting existing values which can lead to problems down the road.
    fund_deal_to_target = fund.value
    # Finds the bucket that the requested fund is in.
    bucket = (constants.bucket_identifier(fund))
    # This function returns all funds in the requested bucket, it also returns the deal to target of the bucket.
    bucket_deal_to_target = constants.find_funds_in_bucket(bucket.value)[1]
    # The most overweight this function allows a fund to be, is 30 basis points.
    trade_maximum_addition = constants.total_portfolio_value().value * constants.FUND_TRADING_LIMITS
    # Abs values are used here to avoid negative deal to target making this function work incorrectly.
    if abs(bucket_deal_to_target) > abs(fund_deal_to_target):
        # Various logic gates to determine the ideal trade size. This could be tweaked or elimated if they can be calculated
        # another way. #
        if abs(bucket_deal_to_target) > (abs(fund_deal_to_target) + trade_maximum_addition):
            if fund_deal_to_target > 0:
                trade_value = fund_deal_to_target + trade_maximum_addition
            else:
                trade_value = fund_deal_to_target - trade_maximum_addition
            trade_writer.single_trade_writer(fund, trade_value)
            return
        else:
            trade_writer.single_trade_writer(fund, bucket_deal_to_target)
            return
    else:
        trade_writer.single_trade_writer(fund, bucket_deal_to_target)
        return


def find_fund_to_trade(bucket, bucket_dtt):
    """
    This finds the highest deal to target in the desired direction of the given bucket.
    Takes the bucket name, the bucket DTT and returns the highest value.
    :param bucket: String
    :param bucket_dtt: Integer
    :return: Integer
    """
    return_array = []
    for fund in constants.find_funds(bucket):
        # This takes into account any existing trades.
        existing_trade = fund.offset(0, 2).value
        if existing_trade is not None:
            trade_value = fund.value - existing_trade
        else:
            trade_value = fund.value
        return_array.append([fund, trade_value])
    # Organises the bucket in the desired direction.
    sorted_bucket = (sorted(return_array, key=operator.itemgetter(1), reverse=bucket_dtt > 0))
    return sorted_bucket[0]


def find_value(cell):
    """
    This function takes a cell and returns its value - makes for a cleaner generator/list comprehension function.
    :param cell: Cell
    :return: Value
    """
    return cell.value


def funds_to_trade_by_bucket():
    """ This function executes all trades required to trade a single bucket within tolerance. """
    for bucket in constants.all_buckets():
        bucket_dtt = constants.find_funds_in_bucket(bucket.value)[1]
        if abs(bucket_dtt) > constants.total_portfolio_value().value * constants.BUCKET_TRADE_INITIALISER:
            while abs(bucket_dtt) > constants.total_portfolio_value().value * constants.BUCKET_TRADE_GOAL:
                bucket_dtt = constants.find_funds_in_bucket(bucket.value)[1]
                # print(find_fund_to_trade(bucket, bucket_dtt))
                trade_execution(find_fund_to_trade(bucket, bucket_dtt)[0])
                bucket_dtt = constants.find_funds_in_bucket(bucket.value)[1]
                # The reason bucket_DTT is re-calculated multiple times, is because it is checked at multiple locations
                # Including as an exit clause. If it is not re-calculated constantly, then it will force too few/many
                # trades. #


# The bond and equity sector trade functions could be aggregated easily enough with some level argument trickery.
# The reason that this was not done, was readability. It is more important that the code is easily readable, as it is
# not yet finished, that these extremely small optimisations are not yet worth the trade-off.
def funds_to_trade_by_bond_sector(sector_traded):
    """
    If the sector has been traded, then the target to deal the sector to, changes. The tolerance starts at 50bps.
    If the sector has been traded, then it drops to 20bps.
    :param sector_traded: Bool
    :return: Void
    """
    if sector_traded or abs(
            constants.find_bond_sector_dtt()) > constants.total_portfolio_value().value * constants.BOND_SECTOR_TRADE_INITIALISER:
        while abs(
                constants.find_bond_sector_dtt()) > constants.total_portfolio_value().value * constants.BOND_SECTOR_TRADING_GOAL:
            buckets = []
            for bucket in constants.bonds_sector():
                buckets.append(constants.find_funds_in_bucket(bucket.value))
            # Sorts the array generated above (all buckets and their deal to targets) and selects the first
            # (highest) value.
            bucket_to_trade = (
                sorted(buckets, key=operator.itemgetter(1), reverse=constants.find_bond_sector_dtt() > 0)[0])
            # Finds the fund that requires a trade the most in the given bucket.
            fund_to_trade = (find_fund_to_trade(bucket_to_trade[0][0].offset(0, 4), bucket_to_trade[1]))
            # Exec this trade.
            trade_execution(fund_to_trade[0])


def funds_to_trade_by_equity_sector(sector_traded):
    if sector_traded or abs(
            constants.find_equity_sector_dtt()) > constants.total_portfolio_value().value * constants.EQUITY_SECTOR_TRADE_INITIALISER:
        while abs(
                constants.find_equity_sector_dtt()) > constants.total_portfolio_value().value * constants.EQUITY_SECTOR_TRADING_GOAL:
            buckets = []
            for bucket in constants.equities_sector():
                buckets.append(constants.find_funds_in_bucket(bucket.value))
            bucket_to_trade = (
                sorted(buckets, key=operator.itemgetter(1), reverse=constants.find_equity_sector_dtt() > 0)[0])
            fund_to_trade = (find_fund_to_trade(bucket_to_trade[0][0].offset(0, 4), bucket_to_trade[1]))
            trade_execution(fund_to_trade[0])


# This function calculates whether cash needs to be generated, or whether there is too much cash.
def cash_generation():
    # The cash figure is updated as trades are entered. As such this figure should give a live, accurate cash figure.
    current_cash = (constants.cash_figure().value / constants.total_portfolio_value().value)
    cash_to_deal = current_cash - constants.get_cash_target().value
    if abs(cash_to_deal) > constants.CASH_SECTOR_TRADE_INITIALISER:
        while abs(cash_to_deal) > constants.CASH_SECTOR_TRADING_GOAL:
            all_dtt = (constants.all_bucket_deal_to_target().items())
            all_dtt = (sorted(all_dtt, key=lambda x: x[1], reverse=cash_to_deal > 0))
            trade_execution(find_fund_to_trade(all_dtt[0][0], all_dtt[0][1])[0])
            cash_to_deal = (
                                       constants.cash_figure().value / constants.total_portfolio_value().value) - constants.get_cash_target().value


# This acts as the trade starting point. This is done so functions can be taken out easily and without affecting
# any dependancies etc. #
def rebalancing():
    # The order within this function is somewhat arbitrary. Cash is left until the end to ensure that buckets and sectors
    # Are in line, and then cash is generated if need be. Which should reduce the amount of required trades.
    # Similarly, if funds are significantly out of balance, then trading these could bring their bucket/sector in line. #
    funds_overweight()
    # This trades if a bucket is overweight.
    funds_to_trade_by_bucket()
    # These functions trade by sector. (Bonds and Equities) (the argument passed checks whether the sector has already
    # Been traded.) If so, it will continue to trade it within target.
    funds_to_trade_by_bond_sector(constants.bond_sector_traded())
    funds_to_trade_by_equity_sector(constants.equity_sector_traded())
    # Ensures that cash is within limits.
    cash_generation()


def main():
    # Varible initialisation.
    global WRITER_SHEET, READER_SHEET, MODIFIED_FILENAME
    all_files = file_id_reader.list_all_files(True)
    filename_user = file_id_reader.user_selected_file(all_files)
    filenames = file_id_reader.file_name_generator(filename_user)
    for filename in filenames:
        READER_SHEET = file_id_reader.sheet_reader(filename, True)
        write_to = xl.load_workbook(filename)
        WRITER_SHEET = write_to['Rebalancer']
        trade_writer.WRITER_SHEET, trade_writer.READER_SHEET = WRITER_SHEET, READER_SHEET
        constants.READER_SHEET = READER_SHEET
        # If the cash target isn't approximately 100%, then something has gone wrong. This error stops infinite loops
        # Or worse, unnecessary trades. #
        if round(constants.get_total_target().value, 2) != 1:
            print(f"There has been an error with rebalancer: {filename}\n"
                  f"Check that the target is 100%, the cash target may be off.")
            continue
        while True:
            # This function checks if the amount of trades is the same as after it runs through rebalancing. If it is,
            # Then no trade has been found, meaning everything is in line and the rebalancer is ready to be saved. #
            count_trades = trade_writer.TRADES
            rebalancing()
            if count_trades == trade_writer.TRADES:
                break
        # This is where the trade aggregator should go.
        # Would my life be easier if I didn't write trades from the off and instead read then all from the aggregator
        # then add the trades to the writer sheet.
        trade_writer.final_trade_writer()
        # Could this be written to a more succinct filename? Could it overwrite the existing file?
        MODIFIED_FILENAME = filename[:-5] + " finished.xlsx"
        trade_writer.MODIFIED_FILENAME = MODIFIED_FILENAME
        write_to.save(MODIFIED_FILENAME)
    else:
        print(f'Successfully written: {trade_writer.TRADES} trades')


if __name__ == '__main__':
    main()
