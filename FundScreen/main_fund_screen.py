# TODO: Could probably init a .xlsx doc type too which would just change to a pd.read_excel operator on the import
#  processing class.
# TODO: Dataprocessing class should be dynamic. Having this preset means that adding new variables isn't
#  going to be picked
#  up. What I should really be doing in here is having another class of potential calculations that I can run
#  on each dataset and then have them execute in the main function. i.e. Class DataManipulation
#  def UpDownDifference(self) and then be able to run the below function in this class which would append the
#  column to the dataframe object. Or it would return the new object?
# TODO: Probably import the OCF
# TODO: Could I do something cool here like, all the funds that've been rejected just end up in the final page on
#  excel called 'rejects' and it does whatever calculations it can do?
# TODO: Can you add in the dates to the Up down difference column header
# TODO: Review value growth score brackets. Review Luke's style box output to see whether this couldbe more repliable
#  than the "value growth score long" datapoint.
# TODO: Collect dates from somewhere.
import output
from data_processing import DataProcessing
# Imports
from import_processing import ImportProcessing


def main():
    """

	"""
    import_document = ImportProcessing(filetype=".xlsx")
    data_processing = DataProcessing(import_document.DF)
    # pre_processed = output.OutputPreprocessing(data_processing.Output_DF)
    # output.OutputDocument(pre_processed, filename=import_document.Filename)
    # print("Successfully written")


if __name__ == '__main__':
    main()
