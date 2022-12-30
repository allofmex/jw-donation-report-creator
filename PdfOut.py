from PyPDF2 import PdfWriter
from UserDonations import UserDonations
from Config import Config
from StringTools import numberToFinanceStr
import locale, datetime

class PdfOut:
    
    def __init__(self, config: Config):
        self.config = config

    def fill(self, pages, donations: UserDonations, userData):
        self.writer = PdfWriter()
        # copy source pages to target
        for page in pages:
            self.writer.add_page(page)

        # fill pages with data
        self.__fillOverview(donations, userData)
        self.__fillList(donations)

    def __fillOverview(self, donations, userData) -> None:
        overviewPage = self.writer.pages[0]
        nameAndAddress = f"{userData['firstName']} {userData['lastName']}\n{userData['street']}\n{userData['place']}"
        total = donations.getTotal()
        numAsText = numberToFinanceStr(total)

        now = datetime.date.today()
        locale.setlocale(locale.LC_TIME,'de_DE.UTF-8')
        placeAndDate = f"{self.config.get(Config.PLACE)}, {now.strftime('%x')}"

        self.writer.update_page_form_field_values(
            overviewPage, {"Text1": self.config.get(Config.CONG_NAME),
                            "SummeB1": numAsText,
                            "dhFormfield-3975399766": f'{total:.2f}'.replace('.',','),
                            "Text2": self.config.get(Config.COORDINATOR_TEXT),
                            "Text3": nameAndAddress,
                            "Text5": placeAndDate,
                           }
        )

    def __fillList(self, donations: UserDonations):
        listPage = self.writer.pages[1]
        fieldValueList = {}
        idx = 0
        donationList = donations.getList()
        for idx in range(0, len(donationList)):
            if idx > 24:
                raise Exception('Not implemented for more than 24 donations per user!', len(donationList))
            value = donationList[idx].amount
            fieldValueList[f"Datum{idx+1}"] = donationList[idx].date
            fieldValueList[f"BetragZ{idx+1}"] = f'{value:.2f}'.replace('.',',')

        total = donations.getTotal()
        fieldValueList["dhFormfield-3975399824"] = f'{total:.2f}'.replace('.',',')
        fieldValueList["Summe"] = f'{total:.2f}'.replace('.',',')

        self.writer.update_page_form_field_values(
            listPage, fieldValueList
        )

    def writeFile(self, targetFilePath):
        """ write "output" pdf file """
        with open(targetFilePath, "wb") as output_stream:
            self.writer.write(output_stream)