#!/usr/bin/python3

from PyPDF2 import PdfWriter
from UserDonations import UserDonations

class PdfOut:
    
    def __init__(self, config):
        self.config = config

    def fill(self, pages, donations: UserDonations):
        self.writer = PdfWriter()
        # copy source pages to target
        for page in pages:
            self.writer.add_page(page)

        # fill pages with data
        self.__fillOverview(donations)
        self.__fillList(donations)

    def __fillOverview(self, donations):
        overviewPage = self.writer.pages[0]
        total = donations.getTotal()
        self.writer.update_page_form_field_values(
            overviewPage, {"Text1": "abc",
                           "SummeB1": f'{total:.2f}'.replace('.',',')}
        )

    def __fillList(self, donations: UserDonations):
        listPage = self.writer.pages[1]
        fieldValueList = {}
        idx = 0
        print(donations)
        donationList = donations.getList()
        for idx in range(0, len(donationList)):
            if idx > 24:
                raise Exception('Not implemented for more than 24 donations per user!', len(donationList))
            value = donationList[idx].amount
            fieldValueList[f"Datum{idx+1}"] = donationList[idx].date
            fieldValueList[f"BetragZ{idx+1}"] = f'{value:.2f}'.replace('.',',') 

        self.writer.update_page_form_field_values(
            listPage, fieldValueList
        )

    def writeFile(self, targetFilePath):
        """ write "output" pdf file """
        with open(targetFilePath, "wb") as output_stream:
            self.writer.write(output_stream)