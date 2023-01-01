#!/usr/bin/python3
import csv, re
from re import sub
from UserDonations import UserDonations
from datetime import datetime

class AccountReportReader:

    def __init__(self):
        self.result = {}

    def read(self, csvFilePath):
        with open(csvFilePath, mode='r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                # "Auftragskonto";"Buchungstag";"Valutadatum";"Buchungstext";"Verwendungszweck";"Beguenstigter/Zahlungspflichtiger";"Kontonummer";"BLZ";"Betrag";"Waehrung";"Info"
                action = row[3]
                if action == "Buchungstext":
                    # head line
                    continue
                if action.startswith("BARGELDEINZAHLUNG") or action == "FOLGELASTSCHRIFT" or action == "DAUERAUFTRAG" or action == "EINZELUEBERWEISUNG":
                    continue

                if action == "GUTSCHR. UEBERW. DAUERAUFTR" or action == "GUTSCHR. UEBERWEISUNG":
                    name = row[5]
                    if name == "Jehovas Zeugen in Deutschland, K. d. o. R.":
                        continue
                    self.handleDonateRow(row)
                else:
                    print("ToDo "+action)
                    print("unhandled ".join(row))

        return self.result

    def handleDonateRow(self, row):
        date = datetime.strptime(row[1], "%d.%m.%y")
        name = row[5].title() # first letter uppercase, rest lower
        note = None
        regEx = re.search(r'^.*SVWZ\+([^+]+)(?:ABWA\+([^+]+))?$', row[4])
        if regEx is None:
            raise Exception('Purpose line cannot be handled', row[4])
        purpose = regEx.group(1)
        if regEx.group(2) is not None:
            # ABWA, abweichender Auftraggeber
            otherName = regEx.group(2)
            note = f"Transaction on different name! '{otherName}'! ({row[4]})"

        if "spende" not in purpose.lower():
            raise Exception('Not a donation row??', row[4], purpose)

        amount = float(row[8].replace(",", "."))
        self.onDonation(date, name, amount, purpose, note)

    def onDonation(self, date, name, amount, purpose, note):
        # print(date + " "+name+" "+purpose+" "+str(amount));
        self.getForName(name).addDonation(date, amount, note)

    def getForName(self, name):
        userDonations = self.result.get(name)
        if userDonations is None:
            userDonations = UserDonations()
            self.result[name] = userDonations
        return userDonations
