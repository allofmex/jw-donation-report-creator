import os
from Config import Config
from User import User
from PdfOut import PdfOut
import readchar, readline # just import readline, it will make input() using arrow/back/.. keys correctly
from datetime import datetime
from PyPDF2 import PdfWriter
from UserDonations import UserDonations

class DonationReportCreator:
    def __init__(self, config: Config):
        self.__config = config
        self.__targetPath = './out'
        self.__testMode = False
        self.__unattended = False
        self.__createDate = None
        self.__writer = None
        
    def setCreateDate(self, createDate: str):
        self.__createDate = createDate
        
    def setWriter(self, pdfWriter: PdfOut):
        self.__writer = pdfWriter

    def create(self, donations, userList: User, rangeStr: str) -> None:
        if not os.path.exists(self.__targetPath):
            os.mkdir(self.__targetPath, 0o700)

        cnt = 0;
        for userName in donations:
            userDonations = donations[userName]
            userData = userList.getUserData(userName)
            if userData is None:
                userData = self.__requestManualUser(userName)
                if userData is None:
                    return False
    
            if self.__isNotNeeded(userData):
                print(f"Skipping {userName}. Not needed because in exclude list.")
                break
            if self.__createForUser(userName, userDonations, userData, rangeStr):
                cnt +=1
                if self.__testMode:
                    print("Stopping because of test-mode")
                    # write only 1 item
                    break
        print(f"Finished. {cnt} files created.")
        
    def createSingleUser(self, userList: User, rangeStr: str) -> None:
        firstName = input(f"Firstname:").title() # first letter uppercase, rest lower
        userData = userList.getUserData(firstName+" *")
        nameSuggest = userData['lastName'] if userData is not None else ''
        lastName = input(f"Lastname [{nameSuggest}]").title() or nameSuggest

        userName = f"{firstName} {lastName}"
        if lastName != nameSuggest:
            userData = self.__requestManualUser(userName)
        else:
            print(f"Address found: {userData['firstName']}, {userData['lastName']}, {userData['street']}, {userData['place']}")

        if userData is None:
            print("Not enough data")
            return    

        donations = UserDonations()
        self.__requestDonationInfo(donations)

        print("Summary:")
        print(f"{donations.getReport()}")
        if self.__requestUserConfirm(f"Is this correct? (y/n)") == True:
            if self.__createForUser(userName, donations, userData, rangeStr):
                print("OK")
        else:
            print("Sorry")
            
        
    def __requestDonationInfo(self, donations: UserDonations) -> None:
        dateStr = ''
        amount = 0
        f = "%d.%m.%y"
        print("Enter donations")
        while True:
            date = None
            while date is None:
                dateStr = input(f"Date (day.month.year like 1.1.23) or c if complete [{dateStr}]:") or dateStr
                if dateStr == "c":
                    return
                try:
                    date = datetime.strptime(dateStr, f)
                except ValueError:
                    print("Invalid date")
                    date = ''

            amount = int(input(f"Amount [{amount}]:")) or amount
            if amount <= 0:
                print("Invalid amount")
                continue
            donations.addDonation(date, amount)

    def __createForUser(self, userName: str, userDonations: UserDonations, userData: dict, rangeStr: str) -> bool:
        print(f"Creating pdf for {userName: <40}" + userDonations.getOverview())

        accountName = userName
        userListName = userData['firstName']+" "+userData['lastName']

        if self.__consistencyCheck(accountName, userListName, userDonations) is False:
            print(f"!!! Skipped report creation for {accountName}\n")
            return False

        accountName = accountName.replace(" Und ", " und ")
        userData['accountName'] = accountName
        resultFileName = self.__targetPath +"/"+ userName.replace(" ", "_") + ".pdf"

        if (self.__writer is None):
            raise Exception('No __writer set!')
        self.__writer.fill(userDonations, userData, rangeStr, self.__createDate)
        self.__writer.writeFile(resultFileName)
        return True

    def __consistencyCheck(self, accountName, userListName, userDonations):
        if userListName != accountName:
            if not self.__onNameInconsistency(accountName, userListName):
                return False

        if (userDonations.getNotes() is not None):
            if not self.__onNotesPresent(userDonations.getNotes(), accountName, userListName):
                return False
        
    def __onNameInconsistency(self, accountName, userListName):
        print("\nPossible name inconsistency found:")
        print(f"Name in bank report: {accountName}")
        print(f"Name in user list: {userListName}")
        print(f"Address will be used from '{userListName}', Name on donation report will be '{accountName}'")
        if (self.__unattended):
            print("\n")
            return True
        return self.__requestUserConfirm("Is this correct? (y/n)")

    def __onNotesPresent(self, notes, accountName, userListName):
        print(f"Please check the following message(s). Is this acceptable? (report to create is for '{accountName}')")
        for note in notes:
            print(f" {note}")
        if (self.__unattended):
            print("\n")
            return True
        return self.__requestUserConfirm("Is found data valid? (y/n)")

        
    def __requestUserConfirm(self, msg):
        print(msg)
        while True:
            key = readchar.readkey()
            if key == 'y':
                return True
            elif key == 'n':
                return False

    def __isNotNeeded(self, userData):
        userName = f"{userData['firstName']} {userData['lastName']}"
        excludeList = self.__config.get(Config.EXCLUDE_NAMES, False)
        return excludeList != None and userName in excludeList.split(",")
    
    def __requestManualUser(self, userName: str):
        names = userName.split(", ") # "lastname, firstname"
        if len(names) == 1:
            names = userName.split(" ") # "firstname1 and firstname2 lastname"
            names.reverse()
        userData = {'firstName': names[len(names)-1],
                    'lastName': names[0],
                    'street': "",
                    'place': ""}
        print(f"No address data found for '{userName}'")

        while True:
            print("(s)kip report for user or enter address (m)anually?")
            key = readchar.readkey()
            if key == 's':
                print(f"Skipping report for {userName}\n")
                return None
            elif key == 'm':
                userData['firstName'] = input(f"Firstname [{userData['firstName']}]:") or userData['firstName']
                userData['lastName'] = input(f"Lastname [{userData['lastName']}]:") or userData['lastName']
                userData['street'] = input(f"Street and number [{userData['street']}]:") or userData['street']
                userData['place'] = input(f"Zip code and place: [{userData['place']}]") or userData['place']
                print(f"Summary\n {userData['firstName']} {userData['lastName']}\n {userData['street']}\n {userData['place']}")
                if self.__requestUserConfirm(f"Is this correct? (y/n)") == True:
                    print("OK")
                    return userData

    def setTestMode(self):
        self.__testMode = True
        
    def setUnattended(self):
        self.__unattended = True
