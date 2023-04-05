import pandas as pd


class Calculations:
    @staticmethod
    def UpDownDifference(df):
        df['Up Down difference'] = df['Up Capture Ratio'] - df['Down Capture Ratio']


class OutputPreprocessing:
    def __init__(self, input_dataframe):
        self.DF = input_dataframe
        self.SmallValue = None
        self.SmallCore = None
        self.SmallGrowth = None
        self.LargeValue = None
        self.LargeCore = None
        self.LargeGrowth = None
        self.GrowthValueBrackets = [100, 200]
        self.SmallLargeBarrier = 6000
        self.ClassifyDataframes()

    # TODO: I could do this here, or I could break into small and large, and then into value, core, growth?
    def ClassifyDataframes(self):
        vgs = 'Value-Growth Score (Long)'
        amc = 'Average Market Cap (mil) (Long)'
        self.SmallValue = self.DF.loc[(self.DF[vgs].astype(float) <= self.GrowthValueBrackets[0])
                                      & (self.DF[amc].astype(float) <= self.SmallLargeBarrier)]

        self.SmallCore = self.DF.loc[(self.GrowthValueBrackets[1] >= self.DF[vgs].astype(float))
                                     & (self.DF[vgs].astype(float) >= self.GrowthValueBrackets[0])
                                     & (self.DF[amc].astype(float) <= self.SmallLargeBarrier)]

        self.SmallGrowth = self.DF.loc[(self.DF[vgs].astype(float) >= self.GrowthValueBrackets[1])
                                       & (self.DF[amc].astype(float) <= self.SmallLargeBarrier)]

        self.LargeValue = self.DF.loc[(self.DF[vgs].astype(float) <= self.GrowthValueBrackets[0])
                                      & (self.DF[amc].astype(float) > self.SmallLargeBarrier)]

        self.LargeCore = self.DF.loc[(self.GrowthValueBrackets[1] >= self.DF[vgs].astype(float))
                                     & (self.DF[vgs].astype(float) >= self.GrowthValueBrackets[0])
                                     & (self.DF[amc].astype(float) > self.SmallLargeBarrier)]

        self.LargeGrowth = self.DF.loc[(self.DF[vgs].astype(float) >= self.GrowthValueBrackets[1])
                                       & (self.DF[amc].astype(float) > self.SmallLargeBarrier)]


class OutputDocument:
    def __init__(self, processed_document, filename: str = "PlaceholderName"):
        self.Filename = filename
        self.Sheets = ['Small Value', 'Small Core', 'Small Growth', 'Large Value', 'Large Core', 'Large Growth']
        self.ProcessedDoc = processed_document
        self.PopulateSheets()

    def PopulateSheets(self):
        writer = pd.ExcelWriter(self.Filename[:-4] + ' Output.xlsx')
        self.SmallValueWriter(writer)
        self.SmallCoreWriter(writer)
        self.SmallGrowthWriter(writer)
        self.LargeValueWriter(writer)
        self.LargeCoreWriter(writer)
        self.LargeGrowthWriter(writer)
        writer.save()

    def SmallValueWriter(self, writer):
        self.ProcessedDoc.SmallValue.to_excel(writer, sheet_name=self.Sheets[0], index=False)

    def SmallCoreWriter(self, writer):
        self.ProcessedDoc.SmallCore.to_excel(writer, sheet_name=self.Sheets[1], index=False)

    def SmallGrowthWriter(self, writer):
        self.ProcessedDoc.SmallGrowth.to_excel(writer, sheet_name=self.Sheets[2], index=False)

    def LargeValueWriter(self, writer):
        self.ProcessedDoc.LargeValue.to_excel(writer, sheet_name=self.Sheets[3], index=False)

    def LargeCoreWriter(self, writer):
        self.ProcessedDoc.LargeCore.to_excel(writer, sheet_name=self.Sheets[4], index=False)

    def LargeGrowthWriter(self, writer):
        self.ProcessedDoc.LargeGrowth.to_excel(writer, sheet_name=self.Sheets[5], index=False)
