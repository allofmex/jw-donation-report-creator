#!/usr/bin/python3

import sys, getopt, locale
from datetime import datetime
from PyPDF2 import PdfReader
from PdfOut import PdfOut
from AccountReportReader import AccountReportReader
from Config import Config
from User import User

from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject

verbose = False
testMode = False

argumentList = sys.argv[1:]
options, remainder = getopt.getopt(argumentList, "r:vt", ["range=", "verbose", "test"])
for opt, arg in options:
    if opt in ('-r', '--range'):
        startEnd = arg.split("-")
        if len(startEnd) != 2:
            raise Exception("Invalid range, must be in format 01.2022-12.2022", arg)
        f = "%d.%m.%Y"
        start = datetime.strptime("01."+startEnd[0], f)
        end = datetime.strptime("31."+startEnd[1], f)
        print("WARNING: range is currently used for print in result file only. Not as filter for account-report input data!")
    if opt in ('-v', '--verbose'):
        verbose = True
    if opt in ('-t', '--test'):
        testMode = True

locale.setlocale(locale.LC_TIME,'de_DE.UTF-8')
print(f"Preparing file in range {start.strftime('%x')} to {end.strftime('%x')}")

configFilePath = './settings/config.yml';

csvReader = AccountReportReader();
print(f"Reading account report file(s)")
donations = csvReader.read('CSV 09#2022.CSV');

reader = PdfReader("source.pdf")
fields = reader.get_fields()

rangeStr = f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"
if verbose:
    print("\nFound field names in source pdf file:")
    for field in fields:
        print(field);
        # print(fields[field])
    print("\n")

config = Config(configFilePath)
userList = User("user.csv")

pdfWriter = PdfOut(config)

cnt = 0;
for userName in donations:
    print(f"Creating pdf for {userName}\n")
    userDonations = donations[userName]
    userData = userList.getUserData(userName)

    resultFileName = userName.replace(" ", "_") + ".pdf"
    pdfWriter.fill(reader.pages, userDonations, userData, rangeStr)

    pdfWriter.writeFile(resultFileName)
    cnt +=1
    if testMode:
        # write only 1 item
        break

print(f"Finished. {cnt} files created.")
