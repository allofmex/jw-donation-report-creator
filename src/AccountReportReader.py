#!/usr/bin/python3
import csv, re
from re import sub
from UserDonations import UserDonations
from Config import Config
from datetime import datetime
import readchar
from termcolor import colored

class AccountReportReader:

    DATE_COL = 1
    NAME_COL = 5
    PURPOSE_COL = 4
    AMOUNT_COL = 8

    def __init__(self, config: Config):
        self.config = config
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
                if (action.startswith("BARGELDEINZAHLUNG") or action == "FOLGELASTSCHRIFT"
                        or action == "DAUERAUFTRAG" or action == "EINZELUEBERWEISUNG"
                        or action == "ENTGELTABSCHLUSS"):
                    continue

                if action == "GUTSCHR. UEBERW. DAUERAUFTR" or action == "GUTSCHR. UEBERWEISUNG":
                    name = row[5]
                    if name.lower().replace(',', '').startswith("jehovas zeugen in deutschland k"): # variable names used "Jehovas Zeugen In Deutschland, Körperschaft Des Öffent", "... K.d.ö.R"...
                        continue
                    self.handleDonateRow(row)
                elif  row[self.AMOUNT_COL].startswith("-"):
                    continue
                else:
                    print(colored("This line cannot be handled by this tool:", 'red'), self.__getRowPrint(row))

        return self.result

    def handleDonateRow(self, row):
        date = datetime.strptime(row[self.DATE_COL], "%d.%m.%y")
        name = row[self.NAME_COL].title() # first letter uppercase, rest lower
        note = None
        regEx = re.search(r'^.*SVWZ\+([^+]+)(?:ABWA\+([^+]+))?$', row[self.PURPOSE_COL])
        if regEx is None:
            if self.__requestUserConfirm(f"Unclear purpose line found, is this a user-donation? (y/n)\n {date.strftime('%d.%m.%Y')}: '{row[self.PURPOSE_COL]}', {name}") == True:
                print("OK")
                purpose = ""
            else:
                print("Entry ignored")
                return
        else:
            purpose = regEx.group(1)
            if regEx.group(2) is not None:
                # ABWA, abweichender Auftraggeber
                otherName = regEx.group(2)
                note = f"{date.strftime('%d.%m.%Y')}: Transaction on different name! '{name}' => '{otherName}'! ({row[self.PURPOSE_COL]})"
    
            if "spende" not in purpose.lower() and self.__requestUserConfirm(f"Is this NOT a donation row and can be ignored? (y/n)\n {row[4]}, {name}") == False:
                raise Exception('Row cannot be handled!', self.__getRowPrint(row))

        amount = float(row[self.AMOUNT_COL].replace(",", "."))
        self.onDonation(date, name, amount, purpose, note)

    def onDonation(self, date, name, amount, purpose, note):
        # print(date + " "+name+" "+purpose+" "+str(amount));
        replaceNames = self.config.get(Config.REPLACE_NAMES, False)
        if name in replaceNames:
            print(f"Replacing bank report name '{name}' by '{replaceNames[name]}' (config file setting)")
            name = replaceNames[name]
            
        self.getForName(name).addDonation(date, amount, note)

    def getForName(self, name):
        userDonations = self.result.get(name)
        if userDonations is None:
            userDonations = UserDonations()
            self.result[name] = userDonations
        return userDonations

    def __requestUserConfirm(self, msg):
        print()
        print(msg)
        while True:
            key = readchar.readkey()
            if key == 'y':
                return True
            elif key == 'n':
                return False
            
    def __getRowPrint(self, row: list[str]) -> str:
        purpose = row[self.PURPOSE_COL]
        if len(purpose) > 50:
            purpose = purpose[0:50] + "..."
        return f"{row[self.DATE_COL]}, {row[self.AMOUNT_COL]}: {row[self.NAME_COL]}, {purpose}"
        