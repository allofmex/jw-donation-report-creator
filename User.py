import csv

class User:

    def __init__(self, csvFilePath):
        self.csvFilePath = csvFilePath
    
    def getUserData(self, nameStr: str) -> dict:
        """ Result: {firstName: x, lastName: x, street: x, place: x}"""
        row = self.__findRow(nameStr)
        rowNames = row[0].split(", ")
        return {
            "firstName": rowNames[1],
            "lastName": rowNames[0],
            "street": row[1],
            "place": row[2]+" "+row[3],
            }
    
    def __findRow(self, nameStr):
        names = nameStr.split(" ")
        with open(self.csvFilePath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in reader:
                rowNames = row[0].split(", ")
                if rowNames[0] == names[1] and rowNames[1] == names[0]:
                    return row
        raise Exception("No user found!", nameStr)