#!/usr/bin/python3

from PyPDF2 import PdfWriter

class PdfOut:
    writer = PdfWriter()

    def write(self, pages, targetFilePath):
        # copy source pages to target
        for page in pages:
            self.writer.add_page(page)

        # fill pages with data
        self.fillOverview()
        self.fillList()

        # create result file
        self.toFile(targetFilePath)

    def fillOverview(self):
        overviewPage = self.writer.pages[0]
        self.writer.update_page_form_field_values(
            overviewPage, {"Text1": "abc",
                           "SummeB1": "some filled in text4"}
        )

    def fillList(self):
        listPage = self.writer.pages[1]
        self.writer.update_page_form_field_values(
            listPage, {"Datum24" : "1.1.11",
                           "BetragZ24" : "1234,12"}
        )

    def toFile(self, targetFilePath):
        # write "output" pdf file
        with open(targetFilePath, "wb") as output_stream:
            self.writer.write(output_stream)