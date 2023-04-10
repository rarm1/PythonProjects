import csv
import logging
import os
import pathlib
import shutil
import sys
from stat import S_IREAD

from Resources import constants
from Resources import file_id_reader
from Resources import trade_writer


class TradeReader:
    """
    The purpose of this class is to read from a completed rebalancer and generate a document to be passed into Horizon.
    It aims to do this in a user-friendly manner. Without comments, and several of the features that make the program
    pleasant to use, it could be sped up, and made much smaller. However, the target audience for this program is not
    focused entirely on performance, but also ease of use.
    Most functions in the program have detailed documentation, including docstrings for more complex functions, with inputs
    that can accessed by typing
    print(functionname.___doc___)
    """
    def __init__(self):
        self.broker_trades = []
        self.non_broker_trades = []
        self.configure_logging()
        self.path = self.set_path()
        trade_writer.fundmanager_selection()

    @staticmethod
    def write_csv(filename, data):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

    @staticmethod
    def configure_logging():
        logging.basicConfig(filename='Resources/Trade_reader.log', format='%(asctime)s - %(message)s',
                            level=logging.INFO)

    @staticmethod
    def write_to_file(filename, data):
        with open(filename, 'w') as file:
            file.write(data)

    @staticmethod
    def set_path():
        directory = f'Rebalancing {trade_writer.FOLDER_DATE}_TRAIL_DONOTPLACE'
        parent_directory = "X:/Fund Management/Dealing and Rebalancing"
        path = os.path.join(parent_directory, directory)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    @staticmethod
    def find_trades():
        all_found_trades = [x for x in constants.all_funds() if x.offset(0, 2).value not in [None, ""]]
        return all_found_trades

    def process(self):
        all_files = file_id_reader.list_all_files(True, '.xlsx')
        if not all_files:
            sys.exit("Please ensure that there are files ending in .xlsx within the project folder.")

        filename_user = file_id_reader.user_selected_file(all_files)
        filenames = file_id_reader.file_name_generator(filename_user)
        counters = self.process_files(filenames)

        self.copy_non_broker_trades(counters)
        self.copy_broker_trades(counters)

        # exec(open('dealing_notification.py').read())
        print(f"Written a total of {counters['total_trades']} trade{'s' if counters['total_trades'] > 1 else ''}")
        sys.exit(
            "I hope you enjoyed this program! Please direct any queries or issues to richard.armstrong@margetts.com")

    def process_files(self, filenames):
        tradeless = []
        counters = {"total_trades": 0, "funds_without_trades": 0, "total_non_broker_trades": 0,
                    "total_broker_trades": 0}

        for i, filename in enumerate(filenames):
            if len(filenames) > 1:
                print(f'\r{i + 1} rebalancers read.', end='')

            reader_sheet = file_id_reader.sheet_reader(filename, True)
            self.set_reader_sheets(filename, reader_sheet)
            all_trades = self.find_trades()
            counters["total_trades"] += len(all_trades)

            counters = self.process_trades(counters, all_trades)

            if (i + 1) == len(filenames):
                self.print_summary(filenames, tradeless, counters)

            self.copy_file_to_path(filename)

        return counters

    @staticmethod
    def set_reader_sheets(filename, reader_sheet):
        """
        Sets the reader sheet for the trade writer and the constants file.
        :param filename:
        :param reader_sheet:
        """
        trade_writer.READER_DOC = filename
        trade_writer.READER_SHEET = reader_sheet
        constants.READER_SHEET = reader_sheet

    def process_trades(self, counters, all_trades):
        print(f"Counters: {counters}. All trades: {all_trades}")
        if counters["total_trades"]:
            non_broker_trades, broker_trades = trade_writer.automated_trading_array_generator(all_trades)
            counters["total_non_broker_trades"] += len(self.non_broker_trades)
            counters["total_broker_trades"] += len(self.broker_trades)
            if not len(non_broker_trades) == 0:
                self.non_broker_trades.extend(non_broker_trades)
            if not len(broker_trades) == 0:
                self.broker_trades.extend(broker_trades)
        return counters

    @staticmethod
    def print_summary(filenames, tradeless, counters):
        print(f"\nFinished reading {len(filenames)} file{'s' if len(filenames) > 1 else ''}."
              f"\nThere were {len(tradeless)} portfolios without trades."
              f"\n")
        print(f"Written a total of {counters['total_trades']} trade{'s' if counters['total_trades'] > 1 else ''}")

    def copy_file_to_path(self, filename):
        file_path = (pathlib.Path(filename).resolve())
        try:
            shutil.copy2(file_path, self.path)
        except (shutil.SameFileError, PermissionError, Exception) as e:
            logging.error("Error occured" + str(e))
            print(f"{e}: Error occured while copying file.")

    def copy_non_broker_trades(self, counters):
        try:
            if counters['total_non_broker_trades'] != 0:
                print("#############################")
                print(self.non_broker_trades)
                non_broker_filename = trade_writer.main_writer(self.non_broker_trades)
                non_broker_csv = pathlib.Path(non_broker_filename).resolve()
                os.chmod(non_broker_csv, S_IREAD)
                shutil.copy2(non_broker_csv, self.path)

                with open(non_broker_csv, 'r') as file:
                    reader = csv.reader(file)
                    non_broker_trades = list(reader)

                self.write_csv('non_broker_trades.csv', non_broker_trades)

        except AttributeError as e:
            logging.error("Error occured" + str(e))
            print(
                f"{e}\nNo non-broker trades were found, so there is no sheet to copy."
                f"If this is unexpected behaviour, please report it.")

    def copy_broker_trades(self, counters):
        """
        :param self:
        :param counters:
        """
        try:
            if counters['total_broker_trades'] != 0:
                print("#############################")
                print(self.broker_trades)
                broker_filename = trade_writer.broker_trade_writer(self.broker_trades)
                broker_csv = (pathlib.Path(broker_filename).resolve())
                os.chmod(broker_csv, S_IREAD)
                shutil.copy2(broker_csv, self.path)

                with open(broker_csv, 'r') as file:
                    reader = csv.reader(file)
                    broker_trades = list(reader)
                self.write_csv('broker_trades.csv', broker_trades)

        except AttributeError as e:
            logging.error("Error occured" + str(e))
            print(f"{e}\nNo broker trades were found, so there is no sheet to copy."
                  f"If this is unexpected behaviour, please report it.")


if __name__ == "__main__":
    trade_processor = TradeReader()
    trade_processor.process()
