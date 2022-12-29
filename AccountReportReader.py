#!/usr/bin/python3
import csv, re

class AccountReportReader:

    def read(self, csvFilePath):
         with open(csvFilePath, mode='r', encoding='latin-1') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in spamreader:
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

    def handleDonateRow(self, row):
        date = row[1]
        name = row[5]
        purpose = row[4]

        regEx = re.search(r'^.*SVWZ\+([^+]+)(?:ABWA\+([^+]+))?$', row[4])
        if regEx is None:
            raise Exception('Purpose line cannot be handled', row[4])

        purpose = regEx.group(1)
        if regEx.group(2) is not None:
            # ABWA, abweichender Auftraggeber
            otherName = regEx.group(2)
            print(f"Diff name '{otherName}'! ({row[4]})")

        if "spende" not in purpose.lower():
            raise Exception('Not a donation row??', row[4], purpose)

        amount = row[8]
        self.onDonation(date, name, amount, purpose)
        
    def onDonation(self, date, name, amount, purpose):
        print(date + " "+name+" "+purpose+" "+amount);