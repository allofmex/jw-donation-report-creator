import os
from Config import Config
from User import User
from PdfOut import PdfOut
import readchar, readline # just import readline, it will make input() using arrow/back/.. keys correctly
from PyPDF2 import PdfWriter

class DonationReportCreator:
    def __init__(self, config: Config):
        self.config = config
        self.targetPath = './out'
        self.testMode = False
        self.unattended = False
        self.createDate = None
        
    def setCreateDate(self, createDate: str):
        self.createDate = createDate

    def create(self, reader, donations, userList: User, pdfWriter: PdfOut, rangeStr):
        if not os.path.exists(self.targetPath):
            os.mkdir(self.targetPath, 0o700)

        cnt = 0;
        for userName in donations:
            userDonations = donations[userName]
            print(f"Creating pdf for {userName: <40}" + userDonations.getOverview())
            userData = userList.getUserData(userName)
            if userData is None:
                userData = self.__requestManualUser(userName)
                if userData is None:
                    continue

            if self.__isNotNeeded(userData):
                print(f"Skipping {userName}. Not needed because in exclude list.")
                continue

            accountName = userName
            userListName = userData['firstName']+" "+userData['lastName']

            if self.__consistencyCheck(accountName, userListName, userDonations) is False:
                print(f"!!! Skipped report creation for {accountName}\n")
                continue

            accountName = accountName.replace(" Und ", " und ")
            userData['accountName'] = accountName
            resultFileName = self.targetPath +"/"+ userName.replace(" ", "_") + ".pdf"
            writer = PdfWriter()
            # need to copy some data from reader, else forms in result are not visible in some apps (or missing in printing)
            # https://github.com/py-pdf/pypdf/issues/355#issuecomment-786742322
            # clone_reader_document_root still not working properly
            writer._info = reader.trailer["/Info"]
            readerTrailer = reader.trailer["/Root"]
            writer._root_object.update({
                    key: readerTrailer[key]
                    for key in readerTrailer
                    if key in ("/AcroForm", "/Lang", "/MarkInfo")})

            # copy source pages to target
            writer.clone_document_from_reader(reader)
            pdfWriter.fill(writer, userDonations, userData, rangeStr, self.createDate)

            pdfWriter.writeFile(resultFileName)
            cnt +=1
            if self.testMode:
                # write only 1 item
                break
        print(f"Finished. {cnt} files created.")

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
        if (self.unattended):
            print("\n")
            return True
        return self.__requestUserConfirm("Is this correct? (y/n)")

    def __onNotesPresent(self, notes, accountName, userListName):
        print(f"Please check the following message(s). Is this acceptable? (report to create is for '{accountName}')")
        for note in notes:
            print(f" {note}")
        if (self.unattended):
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
        excludeList = self.config.get(Config.EXCLUDE_NAMES, False)
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
        self.testMode = True
        
    def setUnattended(self):
        self.unattended = True