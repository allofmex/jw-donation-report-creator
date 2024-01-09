import csv
from StringTools import specialCharToAscii

class User:

    def __init__(self, csvFilePath):
        self.csvFilePath = csvFilePath
    
    def getUserData(self, nameStr: str) -> dict:
        """ Result: {firstName: x, lastName: x, street: x, place: x}"""
        row = self.__findInFile(nameStr)
        if row is None:
            return None
        rowNames = row[0].split(", ")
        return {
            "firstName": rowNames[1],
            "lastName": rowNames[0],
            "street": row[1],
            "place": row[2]+" "+row[3],
            }
    
    def __findInFile(self, nameStr):
        names = specialCharToAscii(nameStr).split(" ")
        lastName = names[len(names)-1]
        firstName = names[0]
        with open(self.csvFilePath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            row = self.__findRow(reader, firstName, lastName)
            if row is None:
                firstNames = firstName.split("-")
                searchFirstName = firstNames[len(firstNames)-1] # last first-name (peter for hans-peter)
                csvfile.seek(0) # reset file to read again
                row = self.__findRow(reader, searchFirstName, lastName)
            return row
        return None

    def __findRow(self, reader, searchFirstName, lastName):
        for row in reader:
            rowNames = specialCharToAscii(row[0]).split(", ")
            if len(rowNames) >= 2 and rowNames[0] == lastName and rowNames[1] == searchFirstName:
                return row
        return None