#!/usr/bin/python3

from PyPDF2 import PdfReader
from PdfOut import PdfOut
from AccountReportReader import AccountReportReader
from Config import Config


configFilePath = './settings/config.yml';

csvReader = AccountReportReader();
donations = csvReader.read('CSV 09#2022.CSV');

reader = PdfReader("source.pdf")

page = reader.pages[0]
fields = reader.get_fields()

# for field in fields:
#     print(field+"\n");
config = Config(configFilePath)

pdfWriter = PdfOut(config)

for user in donations:
    # print(user+"\n")
    userDonations = donations[user]
    resultFileName = user.replace(" ", "_") + ".pdf"
    pdfWriter.fill(reader.pages, userDonations)

    pdfWriter.writeFile(resultFileName)
    break
