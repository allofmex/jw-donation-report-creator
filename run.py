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

def helpMsg():
    print()
    print("Usage:")
    print("<run.py> --range=01.2022-12.2022 [--yes | --verbose | --test | --help]")
    print("r|range        Range string to print on output files")
    print("y|yes          Unattended mode, confirm all questions with yes")
    print("v|verbose      Print additional data like found form field names in input file")
    print("t|test         Stop after first report. May be used for initial setup/result test")
    print()
    print("Use MT940 csv format for bank account export")
    print()

print ("Donation report creator - Tool to fill TO-67b pdf form with data from bank account report files")

verbose = False
testMode = False
start, end = None, None

creator = DonationReportCreator(config)

try:
    argumentList = sys.argv[1:]
    options, remainder = getopt.getopt(argumentList, "r:yvth", ["range=", "yes", "verbose", "test", "help"])
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
        if opt in ('-h', '--help'):
            helpMsg()
            sys.exit()
except getopt.GetoptError:
  helpMsg()
  sys.exit(2)

if start is None:
    print("You must use --range option!")
    sys.exit(2)

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

