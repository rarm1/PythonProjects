global READER_SHEET


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

