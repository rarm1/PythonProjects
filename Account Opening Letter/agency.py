from constants import Constants
from input_document import InputDocument


class Agency:
    def __init__(self, row):
        self.Constants = Constants()
        self.Reader_Sheet = InputDocument().Reader_Sheet
        self.Agency_Code = None
        self.Agent_Address = None
        self.Agent_Phone = None
        self.fetch_vars(row)

    def fetch_vars(self, row):
        self.Agency_Code = self.Reader_Sheet.cell(row=row, column=self.Constants.AgentCodeColumn).value
        if self.Agency_Code is not None:
            self.Agency_Code = "Agency Code: " + str(self.Agency_Code)
        self.Agent_Address = self.Reader_Sheet.cell(row=row, column=self.Constants.TAAddressColumn).value
        self.Agent_Phone = self.Reader_Sheet.cell(row=row, column=self.Constants.TAPhoneFaxColumn).value
