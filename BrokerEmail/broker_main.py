import logging

from broker_output import BrokerOutput
from dealing_sheet import DealingSheet
from email_writer import Email
from proofing_table import ProofingTable

logging.basicConfig(level=logging.INFO)


def main():
    """
    The main function to read the dealing sheet, generate the broker output, and send the email.
    """
    try:
        logging.info("Starting PAM Broker Uploader")
        dealing_sheet = DealingSheet()
        broker = BrokerOutput(dealing_sheet)
        proof = ProofingTable(broker)
        html_trades = broker.instructionoutput.to_html(index=False)
        html_proof = proof.ProofDataFrame.to_html(index=False)
        mail = Email()
        mail.save_email(html_trades, html_proof)
        logging.info("PAM Broker Uploader completed successfully")
    except Exception as e:
        logging.error(f"Error in PAM Broker Uploader: {e}")
        raise


if __name__ == '__main__':
    main()
