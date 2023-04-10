import pandas as pd


class Calculations:
    @staticmethod
    def updowndifference(df):
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
        self.classify_dataframes()

    # TODO: I could do this here, or I could break into small and large, and then into value, core, growth?
    def classify_dataframes(self):
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
        self.populate_sheets()

    def populate_sheets(self):
        writer = pd.ExcelWriter(self.Filename[:-4] + ' Output.xlsx')
        self._small_value_writer(writer)
        self._small_core_writer(writer)
        self._small_growth_writer(writer)
        self._large_value_writer(writer)
        self._large_core_writer(writer)
        self._large_growth_writer(writer)
        writer.save()

    def _small_value_writer(self, writer):
        self.ProcessedDoc.SmallValue.to_excel(writer, sheet_name=self.Sheets[0], index=False)

    def _small_core_writer(self, writer):
        self.ProcessedDoc.SmallCore.to_excel(writer, sheet_name=self.Sheets[1], index=False)

    def _small_growth_writer(self, writer):
        self.ProcessedDoc.SmallGrowth.to_excel(writer, sheet_name=self.Sheets[2], index=False)

    def _large_value_writer(self, writer):
        self.ProcessedDoc.LargeValue.to_excel(writer, sheet_name=self.Sheets[3], index=False)

    def _large_core_writer(self, writer):
        self.ProcessedDoc.LargeCore.to_excel(writer, sheet_name=self.Sheets[4], index=False)

    def _large_growth_writer(self, writer):
        self.ProcessedDoc.LargeGrowth.to_excel(writer, sheet_name=self.Sheets[5], index=False)
