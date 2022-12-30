#!/usr/bin/python3

from PyPDF2 import PdfReader
from PdfOut import PdfOut
from AccountReportReader import AccountReportReader
from Config import Config
from User import User

from PyPDF2.generic import BooleanObject, NameObject, IndirectObject, TextStringObject

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
