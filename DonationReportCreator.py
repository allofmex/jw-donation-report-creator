import os
from Config import Config
import readchar

class DonationReportCreator:
    def __init__(self, config: Config):
        self.config = config
        self.targetPath = './out'
        self.testMode = False
        self.unattended = False
        
    def create(self, reader, donations, userList, pdfWriter, rangeStr):
        if not os.path.exists(self.targetPath):
            os.mkdir(self.targetPath, 0o700)

        cnt = 0;
        for userName in donations:
            userDonations = donations[userName]
            print(f"Creating pdf for {userName: <40}" + userDonations.getOverview())
            userData = userList.getUserData(userName)

            accountName = userName
            userListName = userData['firstName']+" "+userData['lastName']

            if self.__consistencyCheck(accountName, userListName, userDonations) is False:
                print(f"!!! Skipped report creation for {accountName}\n")
                continue
                
            resultFileName = self.targetPath +"/"+ userName.replace(" ", "_") + ".pdf"
            pdfWriter.fill(reader.pages, userDonations, userData, rangeStr)

            # pdfWriter.writeFile(resultFileName)
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
        print(notes)
        if (self.unattended):
            print("\n")
            return True
        return self.__requestUserConfirm("Is found data valid? (y/n)")

        
    def __requestUserConfirm(self, msg):
        print(msg)
        while True:
            key = readchar.readkey()
            if key == 'y':
                print("Accepted!\n")
                return True
            elif key == 'n':
                return False
    def setTestMode(self):
        self.testMode = True
        
    def setUnattended(self):
        self.unattended = True