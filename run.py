#!/usr/bin/python3

import sys, getopt, locale
from datetime import datetime
from PyPDF2 import PdfReader
from PdfOut import PdfOut
from AccountReportReader import AccountReportReader
from Config import Config
from User import User

from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject

# fullCmdArguments = sys.argv
argumentList = sys.argv[1:]
options, remainder = getopt.getopt(argumentList, "r:", "range=")
for opt, arg in options:
    if opt in ('-r', '--range'):
        startEnd = arg.split("-")
        if len(startEnd) != 2:
            raise Exception("Invalid range, must be in format 01.2022-12.2022", arg)
        f = "%d.%m.%Y"
        start = datetime.strptime("01."+startEnd[0], f)
        end = datetime.strptime("31."+startEnd[1], f)

locale.setlocale(locale.LC_TIME,'de_DE.UTF-8')
print(f"Preparing file in range {start.strftime('%x')} to {end.strftime('%x')}")

configFilePath = './settings/config.yml';

csvReader = AccountReportReader();
print(f"Reading account report file(s)")
donations = csvReader.read('CSV 09#2022.CSV');

reader = PdfReader("source.pdf")

page = reader.pages[0]
fields = reader.get_fields()

# for field in fields:
    # print(field+"\n");
    # print(fields[field])

config = Config(configFilePath)
userList = User("user.csv")

pdfWriter = PdfOut(config)

cnt = 0;
for userName in donations:
    print(f"Creating pdf for {userName}\n")
    userDonations = donations[userName]
    userData = userList.getUserData(userName)

    resultFileName = userName.replace(" ", "_") + ".pdf"
    pdfWriter.fill(reader.pages, userDonations, userData)

    pdfWriter.writeFile(resultFileName)
    cnt +=1
    break

print(f"Finished. {cnt} files created.")
