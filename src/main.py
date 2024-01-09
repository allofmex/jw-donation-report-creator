#!/usr/bin/python3

from DonationReportCreator import DonationReportCreator
import os, sys, getopt, locale
from datetime import datetime
from PyPDF2 import PdfReader
from PdfOut import PdfOut
from AccountReportReader import AccountReportReader
from Config import Config
from User import User

from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject
# from apt_pkg import config

def helpMsg():
    print()
    print("Usage:")
    print("<run.py> --source=mt940.csv --addressFile=user.csv --form=TO-67b.pdf --range=01.2022-12.2022 [--date=1.1.2023 | --yes | --verbose | --test | --help]")
    print("s|source       Bank report source file to read donations from")
    print("a|addressFile  Csv file containing \"Lastname, Fistname\";\"Street + nr\";zip;\"Place\" rows")
    print("f|form         TO-67b pdf file (see README.md)")
    print("r|range        Range string to print on output files")
    print("d|date         Date string to print in signature line. Current date is used if not provided.")
    print("y|yes          Unattended mode, confirm most questions with yes. Useful for testing, Do not use for final run!")
    print("v|verbose      Print additional data like found form field names in input file")
    print("t|test         Stop after first report. May be used for initial setup/result test")
    print()
    print("Use MT940 csv format for bank account export")
    print()

print()
print ("Donation report creator - Tool to fill TO-67b pdf form with data from bank account report files")
print()

verbose = False
testMode = False
start, end = None, None
createDate = None

sourceFilePath = "./mt940.csv"
addressFilePath = "./user.csv"
formFilePath = "./TO-67b.pdf"

configFilePath = './settings/config.yml';
config = Config(configFilePath)
creator = DonationReportCreator(config)

try:
    argumentList = sys.argv[1:]
    options, remainder = getopt.getopt(argumentList, "rsafd:yvth", ["range=", "source=", "form=", "addressFile=", "date=", "yes", "verbose", "test", "help"])
    for opt, arg in options:
        if opt in ('-r', '--range'):
            startEnd = arg.split("-")
            if len(startEnd) != 2:
                raise Exception("Invalid range, must be in format 01.2022-12.2022", arg)
            f = "%d.%m.%Y"
            start = datetime.strptime("01."+startEnd[0], f)
            end = datetime.strptime("31."+startEnd[1], f)
            print("WARNING: range is currently used for print in result file only. Not as filter for account-report input data!")
        if opt in ('-s', '--source'):
            sourceFilePath = arg
        if opt in ('-a', '--addressFile'):
            addressFilePath = arg
        if opt in ('-f', '--form'):
            formFilePath = arg
        if opt in ('-d', '--date'):
            createDate = arg
        if opt in ('-y', '--yes'):
            creator.setUnattended()
        if opt in ('-v', '--verbose'):
            verbose = True
        if opt in ('-t', '--test'):
            creator.setTestMode()
        if opt in ('-h', '--help'):
            helpMsg()
            sys.exit()
except getopt.GetoptError as e:
    print(e)
    helpMsg()
    sys.exit(2)

if not os.path.exists(sourceFilePath):
    print(f"Bank report source file '{sourceFilePath}' not found!")
    sys.exit(2)
if not os.path.exists(addressFilePath):
    print(f"Address data file '{addressFilePath}' not found!")
    sys.exit(2)
if not os.path.exists(formFilePath):
    print(f"TO-67b pdf file '{formFilePath}' not found!")
    sys.exit(2)
if start is None:
    print("You must use --range option!")
    sys.exit(2)

locale.setlocale(locale.LC_TIME,'de_DE.UTF-8')
print(f"Preparing file in range {start.strftime('%x')} to {end.strftime('%x')}")

csvReader = AccountReportReader();
print(f"Reading account report file(s)")
donations = csvReader.read(sourceFilePath);

reader = PdfReader(formFilePath)
fields = reader.get_fields()

rangeStr = f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}"
if verbose:
    print("\nFound field names in source pdf file:")
    for field in fields:
        print(field);
        # print(fields[field])
    print("\n")

userList = User(addressFilePath)

pdfWriter = PdfOut(config)
creator.setCreateDate(createDate)
creator.create(reader, donations, userList, pdfWriter, rangeStr)

