from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from UserDonations import UserDonations
from Config import Config
from StringTools import numberToFinanceStr
import locale, datetime

class PdfOut:
    
    def __init__(self, formFilePath: str, config: Config):
        self.__config = config
        self.__formFilePath = formFilePath
        self.__verbose = False

    def setVerbose(self, verbose: bool):
        self.__verbose = verbose

    def fill(self, donations: UserDonations, userData, rangeStr: str, createDate: str):
        self.__prepareTemplate()
        # fill pages with data
        self.__fillOverview(donations, userData, rangeStr, createDate)
        self.__fillList(donations)
        
    def __prepareTemplate(self):
        reader = PdfReader(self.__formFilePath)
        fields = reader.get_fields()
        
        if self.__verbose:
            print("\nFound field names in source pdf file:")
            for field in fields:
                print(field);
                # print(fields[field])
            print("\n")
    
        writer = PdfWriter()
        # need to copy some data from reader, else forms in result are not visible in some apps (or missing in printing)
        # https://github.com/py-pdf/pypdf/issues/355#issuecomment-786742322
        # clone_reader_document_root still not working properly
        writer._info = reader.trailer["/Info"]
        readerTrailer = reader.trailer["/Root"]
        writer._root_object.update({
                key: readerTrailer[key]
                for key in readerTrailer
                if key in ("/AcroForm", "/Lang", "/MarkInfo")})

        # copy source pages to target
        writer.clone_document_from_reader(reader)
        self.__writer = writer

    def __fillOverview(self, donations, userData, rangeStr: str, createDate: str) -> None:
        overviewPage = self.__writer.pages[0]
        nameAndAddress = f"\n{userData['accountName']}\n{userData['street']}\n{userData['place']}"
        total = donations.getTotal()
        numAsText = numberToFinanceStr(total)

        now = datetime.date.today()
        locale.setlocale(locale.LC_TIME,'de_DE.UTF-8')
        if createDate is None:
            createDate = now.strftime('%x')
        placeAndDate = f"{self.__config.get(Config.PLACE)}, {createDate}"

        fieldValueList = {"Text1": self.__config.get(Config.CONG_NAME),
                            "SummeB1": f"*{numAsText}*",
                            "Tag": rangeStr,
                            "Text2": self.__config.get(Config.COORDINATOR_TEXT),
                            "Text3": nameAndAddress,
                            "Text5": placeAndDate,
                            }
        # original Summe field is auto-calculated. Currently no way to trigger
        # this via PyPDF2.
        # Workarround is manually edited pdf form
        customSumFieldName = self.__config.get(Config.FIX_OVERVIEW_SUM_FIELD_NAME, False)
        sumValueStr = f'*{total:.2f}*'.replace('.',',')
        if customSumFieldName is not None:
            fieldValueList[customSumFieldName] = sumValueStr
        else:
            fieldValueList["Summe"] = sumValueStr
        
        self.__writer.update_page_form_field_values(overviewPage, fieldValueList)

    def __fillList(self, donations: UserDonations):
        listPage = self.__writer.pages[1]
        fieldValueList = {}
        idx = 0
        donationList = donations.getList()
        for idx in range(0, len(donationList)):
            if idx > 24:
                raise Exception('Not implemented for more than 24 donations per user!', len(donationList))
            date = donationList[idx].date
            value = donationList[idx].amount
            fieldValueList[f"Datum{idx+1}"] = f"{date.strftime('%d.%m.%Y')}"
            fieldValueList[f"BetragZ{idx+1}"] = f"*{value:.2f}*".replace('.',',')

        total = donations.getTotal()
        customSumFieldName = self.__config.get(Config.FIX_LIST_SUM_FIELD_NAME, False)
        sumValueStr = f"*{total:.2f}*".replace('.',',')
        if customSumFieldName is not None:
            fieldValueList[customSumFieldName] = sumValueStr
        else:
            fieldValueList["Summe"] = sumValueStr

        self.__writer.update_page_form_field_values(
            listPage, fieldValueList
        )

    def writeFile(self, targetFilePath):
        """ write "output" pdf file """
        with open(targetFilePath, "wb") as output_stream:
            self.__writer.write(output_stream)