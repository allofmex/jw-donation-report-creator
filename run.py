#!/usr/bin/python3

from DonationReportCreator import DonationReportCreator
import sys, getopt, locale
from datetime import datetime
from PyPDF2 import PdfReader
from PdfOut import PdfOut
from AccountReportReader import AccountReportReader
from Config import Config
from User import User

from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject
from apt_pkg import config

verbose = False
testMode = False

creator = DonationReportCreator(config)

argumentList = sys.argv[1:]
options, remainder = getopt.getopt(argumentList, "r:yvt", ["range=", "yes", "verbose", "test"])
for opt, arg in options:
    if opt in ('-r', '--range'):
        startEnd = arg.split("-")
        if len(startEnd) != 2:
            raise Exception("Invalid range, must be in format 01.2022-12.2022", arg)
        f = "%d.%m.%Y"
        start = datetime.strptime("01."+startEnd[0], f)
        end = datetime.strptime("31."+startEnd[1], f)
        print("WARNING: range is currently used for print in result file only. Not as filter for account-report input data!")
    if opt in ('-y', '--yes'):
        creator.setUnattended()
    if opt in ('-v', '--verbose'):
        verbose = True
    if opt in ('-t', '--test'):
        creator.setTestMode()

configFilePath = './settings/config.yml';
config = Config(configFilePath)

locale.setlocale(locale.LC_TIME,'de_DE.UTF-8')
print(f"Preparing file in range {start.strftime('%x')} to {end.strftime('%x')}")

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

userList = User("user.csv")

pdfWriter = PdfOut(config)

creator.create(reader, donations, userList, pdfWriter, rangeStr)
