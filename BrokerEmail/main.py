import logging

from BrokerOutput import BrokerOutput
from DealingSheet import DealingSheet
from EmailWriter import Email

logging.basicConfig(level=logging.INFO)


def main():
    """
    The main function to read the dealing sheet, generate the broker output, and send the email.
    """
    try:
        logging.info("Starting PAM Broker Uploader")
        dealing_sheet = DealingSheet()
        broker_output = BrokerOutput(dealing_sheet)
        html_trades = broker_output.output.to_html(index=False)
        mail = Email()
        mail.save_email(html_trades)
        logging.info("PAM Broker Uploader completed successfully")
    except Exception as e:
        logging.error(f"Error in PAM Broker Uploader: {e}")
        raise


if __name__ == '__main__':
    main()
