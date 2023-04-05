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

"""
Add labels for size and style.

MSCI Europe Large Growth for example for performance on the Large Growth indices rather than IA sector

Trackers should form their separate list

Basically what funds are generating Alpha

Move through the process considering validating our methodology as we go rather than blindly following.

take 3 groups, top six, middle 6, bottom six.

Look at top 18 by groups of 6. Is the top 6 better than second 6 etc.
"""
# Imports
from import_processing import ImportProcessing
from data_processing import DataProcessing
import output


def main():
    import_document = ImportProcessing()
    data_processing = DataProcessing(import_document.DF)
    pre_processed = output.OutputPreprocessing(data_processing.Output_DF)
    output.OutputDocument(pre_processed, filename=import_document.Filename)
    print("Successfully written")


if __name__ == '__main__':
    main()
